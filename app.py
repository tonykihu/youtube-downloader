import requests
from flask import Flask, request, jsonify, render_template
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError


app = Flask(__name__, template_folder='.')
app.config['TEMPLATES_AUTO_RELOAD'] = True


def fetch_with_user_agent(url):
   USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
   headers = {'User-Agent': USER_AGENT}
   response = requests.get(url, headers=headers)
   response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
   return response.url


def get_download_options(url):
   try:
       url_with_user_agent = fetch_with_user_agent(url)
       yt = YouTube(url_with_user_agent)
       formats = []
       # Get Video and Audio Streams
       for stream in yt.streams.filter(progressive=True):
           formats.append({
               'format': stream.mime_type,
               'resolution': stream.resolution,
               'download_url': stream.url
           })

       # Get Audio-Only Streams
       for stream in yt.streams.filter(only_audio=True):
           formats.append({
               'format': stream.mime_type,
               'download_url': stream.url
           })
       # Return Formats or Error
       return formats
   except VideoUnavailable:
       return {"error": "Video Unavailable"}
   except RegexMatchError:
       return {"error": "Invalid YouTube URL"}
   except requests.exceptions.RequestException as e:
       return {"error": f"HTTP Request Error: {e}"}
   except Exception as e:
       return {"error": str(e)}


# 7. Define API Endpoint for Downloads
@app.route('/download', methods=['POST'])
def download():
   # 8. Get URL from Request Body
   data = request.get_json()
   youtube_url = data.get('url')

   # 9. Basic Validation - check if URL was in the body of the request
   if not youtube_url:
       return jsonify({"error": "URL is required"}), 400

   # 10. Get Download Options
   formats = get_download_options(youtube_url)

   # 11. Return JSON Response
   if 'error' in formats:
       return jsonify(formats), 400
   return jsonify({"formats": formats})


# Add route to serve index.html file
@app.route('/')
def index():
   return render_template('index.html')


# 12. Run the Flask Application
if __name__ == '__main__':
   app.run(debug=True)