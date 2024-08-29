from flask import Flask, request, jsonify
import requests
import random
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# Replace with your actual YouTube Data API key
YOUTUBE_API_KEY = 'AIzaSyCjVtYUp9Y3DEM2DFqex3osNIrPO0N6unQ'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

def search_videos(duration_category):
    """Search for videos on YouTube based on duration category."""
    params = {
        'part': 'snippet',
        'maxResults': 50,
        'type': 'video',
        'videoDuration': duration_category,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    return response.json()

def get_video_duration(video_id):
    """Get the duration of a specific video."""
    video_details_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'contentDetails',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(video_details_url, params=params)
    duration = response.json()['items'][0]['contentDetails']['duration']
    # Convert ISO 8601 duration to minutes (implement conversion logic)
    return convert_duration_to_minutes(duration)

def convert_duration_to_minutes(duration):
    """Convert YouTube duration format (ISO 8601) to minutes."""
    # For example, "PT15M33S" should be converted to 15.55 minutes.
    minutes = 0
    # Parse and calculate total minutes
    if 'M' in duration:
        minutes += int(duration.split('M')[0].replace('PT', ''))
    if 'H' in duration:
        minutes += int(duration.split('H')[0].replace('PT', '')) * 60
    return minutes

@app.route('/curate_videos', methods=['GET'])
def curate_videos():
    """Curate videos to match the desired length."""
    target_length = int(request.args.get('n'))
    videos = []
    total_length = 0

    # Search for videos in different duration categories
    for duration_category in ['short', 'medium', 'long']:
        results = search_videos(duration_category)
        video_list = results.get('items', [])
        random.shuffle(video_list)

        for video in video_list:
            video_id = video['id']['videoId']
            video_duration = get_video_duration(video_id)
            if total_length + video_duration <= target_length:
                videos.append({
                    'id': video_id,
                    'title': video['snippet']['title'],
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })
                total_length += video_duration

            if total_length >= target_length:
                break

        if total_length >= target_length:
            break

    return jsonify(videos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
