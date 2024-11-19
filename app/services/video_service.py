import atexit
import os
import re
import threading
import time
from typing import Dict
from flask import Response, after_this_request, jsonify, send_file
from yt_dlp import YoutubeDL
from langchain_community.document_loaders import YoutubeLoader

# Utils
from app.utils.errors import Errors
from app.utils.langchain import Langchain
from app.utils.logger import Logger

# Constants
OUTPUT_FOLDER = os.path.join("app", "temp_audios")
DEFAULT_CODEC = "mp3"
DEFAULT_QUALITY = "192"
MAX_VIDEO_DURATION = 1800

# Custom Exceptions
class InvalidURLException(Exception):
    pass

class FetchVideoInfoException(Exception):
    pass

class GenerateSummaryException(Exception):
    pass

class AudioDownloadException(Exception):
    pass

class FileNotFoundError(Exception):
    pass

class VideoService:
    def __init__(self, output_folder: str = OUTPUT_FOLDER, codec: str = DEFAULT_CODEC, quality: str = DEFAULT_QUALITY, max_video_duration: int = MAX_VIDEO_DURATION):
        self.output_folder = output_folder
        self.codec = codec
        self.quality = quality
        self.max_video_duration = max_video_duration
        self.logger = Logger()
        self.errors = Errors()
        self.langchain = Langchain()
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_video_summary(self, video_url: str):
        """
        Generates a summary for a given video URL.
        """
        try:
            self._validate_url(video_url)
            video_info = self._fetch_video_info(video_url)
            transcription = video_info.get("transcription", "").lower()

            prompt = self.langchain.generate_prompt_template_video_analysis(transcription)
            summary = self.langchain.generate_summary(prompt)

            response_data = {
                "channel": video_info.get("channel", ""),
                "title": video_info.get("title", ""),
                "thumbnail": video_info.get("thumbnail", ""),
                "transcription": transcription,
                "summary": summary,
                "audio_download_link": f"download_audio?url={video_url}"
            }
            return jsonify(response_data), 200

        except (InvalidURLException, FetchVideoInfoException) as ex:
            return self.errors.handle_errors(str(ex), ex, 422)
        except GenerateSummaryException as ex:
            return self.errors.handle_errors("An error occurred while generating the summary.", ex, 500)
        except Exception as ex:
            return self.errors.handle_errors("An unexpected error occurred while generating the summary.", ex, 500)

    def download_audio(self, video_url: str) -> Response:
        """
        Downloads audio from the video URL.
        """
        try:
            self._validate_url(video_url)
            file_path = self._download_audio_file(video_url)
            return self._serve_file(file_path)
        except (InvalidURLException, AudioDownloadException) as ex:
            return self.errors.handle_errors(str(ex), ex, 422)
        except FileNotFoundError as ex:
            return self.errors.handle_errors("File not found.", ex, 404)
        except Exception as ex:
            return self.errors.handle_errors("An error occurred while downloading the audio.", ex, 500)

    # Private helper methods
    def _validate_url(self, video_url: str) -> None:
        """
        Validates the YouTube URL format.
        """
        youtube_url_pattern = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$")
        if not video_url or not youtube_url_pattern.match(video_url):
            raise InvalidURLException("The provided URL is invalid or empty.")

    def _fetch_video_info(self, video_url: str) -> Dict[str, str]:
        """
        Fetches video information and transcription, and validates duration.
        """
        info = self._extract_video_info(video_url)
        self._validate_video_duration(info)
        transcription = self._generate_transcription(video_url)

        return {
            "title": info.get("title", "Unknown"),
            "channel": info.get("uploader", "Unknown"),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail", None),
            "transcription": transcription,
        }

    def _extract_video_info(self, video_url: str) -> Dict:
        """
        Extracts video metadata using YoutubeDL.
        """
        try:
            with YoutubeDL(self._ydl_options()) as ydl:
                info = ydl.extract_info(video_url, download=False)
                if not info:
                    raise FetchVideoInfoException("Failed to extract video information.")
                return info
        except Exception as e:
            raise FetchVideoInfoException(f"Error extracting video information: {e}")

    def _validate_video_duration(self, info: Dict) -> None:
        """
        Ensures the video duration is within allowed limits.
        """
        duration = info.get("duration", 0)
        if duration > self.max_video_duration:
            raise FetchVideoInfoException(
                f"Video duration {duration} seconds exceeds the allowed limit of {self.max_video_duration} seconds."
            )

    def _generate_transcription(self, video_url: str) -> str:
        """
        Generates a transcription using YoutubeLoader.
        """
        try:
            loader = YoutubeLoader.from_youtube_url(video_url, language=["es", "pt", "en"])
            transcription = ''.join(doc.page_content for doc in loader.load())
            if not transcription:
                raise FetchVideoInfoException("Transcription is empty.")
            return transcription
        except Exception as e:
            raise FetchVideoInfoException(f"Error generating transcription: {e}")

    def _download_audio_file(self, video_url: str) -> str:
        """
        Downloads audio from the video URL.
        """
        try:
            with YoutubeDL(self._ydl_options()) as ydl:
                info = ydl.extract_info(video_url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            raise AudioDownloadException(f"Error downloading audio: {e}")

    def _serve_file(self, file_path: str):
        sanitized_path = os.path.abspath(file_path.replace(".webm", f".{self.codec}") if file_path.endswith(".webm") else file_path)
        if not os.path.exists(sanitized_path):
            print(f"ERROR: File not found: {sanitized_path}")
            raise FileNotFoundError(f"File not found: {sanitized_path}")

        def delete_file_later():
            try:
                time.sleep(2)
                if os.path.exists(sanitized_path):
                    os.remove(sanitized_path)
                    print(f"INFO: File {sanitized_path} deleted after serving.")
                else:
                    print(f"INFO: File {sanitized_path} not found during cleanup.")
            except Exception as e:
                print(f"ERROR: Failed to delete file {sanitized_path}: {str(e)}")

        try:
            threading.Thread(target=delete_file_later).start()
            return send_file(
                sanitized_path,
                as_attachment=True,
                download_name=os.path.basename(sanitized_path),
                mimetype=f"audio/{self.codec}"
            )
        
        except Exception as e:
            print(f"ERROR: Failed to serve file {sanitized_path}: {str(e)}")
            raise e

    def _ydl_options(self) -> Dict:
        """
        Options for YoutubeDL.
        """
        return {
            "quiet": True,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self.output_folder, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.codec,
                    "preferredquality": self.quality,
                }
            ],
        }
