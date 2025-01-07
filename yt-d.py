from flask import Flask, request, jsonify
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

# 1. Initialize Flask Application
app = Flask(__name__)

# 2. Define Helper Function to Get Download Options
def get_download_options(url):
    try:
        # 3. Create YouTube Object
        yt = YouTube(url)
        formats = []

        # 4. Get Video and Audio Streams
        for stream in yt.streams.filter(progressive=True):
          formats.append({
          'format': stream.mime_type,
            'resolution': stream.resolution,
            'download_url': stream.url
        })

        # 5. Get Audio-Only Streams
        for stream in yt.streams.filter(only_audio=True):
            formats.append({
              'format':stream.mime_type,
              'download_url': stream.url
            })
        # 6. Return Formats or Error
        return formats
    except VideoUnavailable:
        return {"error":"Video Unavailable"}
    except RegexMatchError:
        return {"error":"Invalid YouTube URL"}
    except Exception as e:
        return {"error":str(e)}


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

# 12. Run the Flask Application
if __name__ == '__main__':
    app.run(debug=True) # use debug=False for production