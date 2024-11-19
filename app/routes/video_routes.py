from flask import Blueprint, request
from app.services.video_service import VideoService

main = Blueprint('video_routes', __name__)
video_service = VideoService()

@main.route('/generate_video_summary', methods=['POST'])
def generate_video_summary():
    video_url: str = request.json['url']
    return video_service.generate_video_summary(video_url)

@main.route('/download_audio', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    return video_service.download_audio(video_url)

