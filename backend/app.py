from flask import Flask, request, jsonify
import requests
import random
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# Replace with your actual YouTube Data API key
YOUTUBE_API_KEY = 'AIzaSyCjVtYUp9Y3DEM2DFqex3osNIrPO0N6unQ'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

def search_videos(topic, duration_category):
    """Search for videos on YouTube based on topic and duration category."""
    params = {
        'part': 'snippet',
        'q': topic,  # Search query to filter videos by topic or hashtag
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
    return convert_duration_to_minutes(duration)

def convert_duration_to_minutes(duration):
    """Convert YouTube duration format (ISO 8601) to minutes."""
    minutes = 0
    seconds = 0

    if 'H' in duration:
        hours = int(duration.split('H')[0].replace('PT', ''))
        minutes += hours * 60
        duration = duration.split('H')[1]

    if 'M' in duration:
        minutes += int(duration.split('M')[0].replace('PT', ''))
        duration = duration.split('M')[1]

    if 'S' in duration:
        seconds = int(duration.split('S')[0].replace('PT', ''))

    minutes += seconds / 60
    return minutes

@app.route('/curate_videos', methods=['GET'])
def curate_videos():
    """Curate videos to match the desired length and topic within 30 seconds."""
    n = request.args.get('n')
    topic = request.args.get('topic')
    if not n:
        return jsonify({'error': 'Missing "n" parameter'}), 400
    if not topic:
        return jsonify({'error': 'Missing "topic" parameter'}), 400

    try:
        target_length = int(n)
    except ValueError:
        return jsonify({'error': '"n" must be an integer'}), 400

    videos = []
    total_length = 0

    # Define the allowable range within 30 seconds (0.5 minutes) of the target length
    min_length = target_length - 0.5
    max_length = target_length + 0.5

    # Search for videos in different duration categories
    for duration_category in ['short', 'medium', 'long']:
        results = search_videos(topic, duration_category)
        video_list = results.get('items', [])
        random.shuffle(video_list)

        for video in video_list:
            video_id = video['id']['videoId']
            video_duration = get_video_duration(video_id)
            if total_length + video_duration <= max_length:
                videos.append({
                    'id': video_id,
                    'title': video['snippet']['title'],
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                })
                total_length += video_duration

            # Check if the total length is within 30 seconds (0.5 minutes) of the target
            if min_length <= total_length <= max_length:
                return jsonify(videos)

    # If no suitable combination is found, return the best effort
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)