from typing import Any
from yt_dlp import YoutubeDL
import asyncio

RESULT_SIZE = 5


async def search_youtube_audio_by_name(
    title: str
) -> (Any | dict[str, Any] | None):
    search_url = f"ytsearch{RESULT_SIZE}:{title}"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'write-thumbnail': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def run_ytdlp():
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(search_url, download=False)

    info = await asyncio.to_thread(run_ytdlp)
    results = []
    for entry in info.get('entries', []):
        results.append({
            'title': entry.get('title'),
            'url': entry.get('url') if entry.get('url')
            else entry.get('webpage_url'),
            'duration': entry.get('duration'),
            'id': entry.get('id'),
            'uploader': entry.get('uploader'),
        })

    return results
