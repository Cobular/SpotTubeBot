import urllib.request
from dataclasses import dataclass
from os import environ
from typing import Optional, List
from urllib import parse as urlparse
from urllib.parse import parse_qs

import pyyoutube
from pyyoutube import Video
from spotdl.search.songObj import SongObj


def get_thumbnail(id: str):
    return f"https://img.youtube.com/vi/{id}/0.jpg"


def get_data(id: str):
    data = urllib.request.urlopen(f"http://youtube.com/get_video_info?video_id={id}")
    for line in data:  # files are iterable
        print(line)


# https://stackoverflow.com/a/19839257/5623598
def pretty_join(lst, cutoff=3):
    if not lst:
        return ""
    # One item form
    elif len(lst) == 1:
        return str(lst[0])
    # Two through `cutoff` artists use the long form
    elif 1 < len(lst) <= cutoff:
        return "{} and {}".format(", ".join(lst[:-1]), lst[-1])
    # More than `cutoff` artists and we cut it off
    return "{} and others".format(", ".join(lst))


youtube_api = pyyoutube.Api(api_key=environ.get("GOOGLE_API_KEY"))


@dataclass
class YoutubeData:
    title: str
    thumbnail: str
    yt_url: str
    artists_5: str
    artists_3: str
    sp_url: str


def get_youtube_data(spotify_url: str) -> Optional[YoutubeData]:
    song = None
    # Catch spotify failing to find song
    try:
        song = SongObj.from_url(spotify_url)
    except Exception:
        return None

    # Catch no youtube url
    if song.get_youtube_link() is None:
        return None

    # Parse for youtube info
    parsed = urlparse.urlparse(song.get_youtube_link())
    vid_id = parse_qs(parsed.query)['v'][0]
    videos: Optional[List[Video]] = youtube_api.get_video_by_id(video_id=vid_id).items

    # Catch when video ID fails
    if len(videos) == 0:
        return None

    # If all that passes, return the found information
    return YoutubeData(
        **{
            "title": videos[0].snippet.title,
            "thumbnail": videos[0].snippet.thumbnails.maxres.url,
            "yt_url": song.get_youtube_link(),
            "artists_5": pretty_join(song.get_contributing_artists(), cutoff=5),
            "artists_3": pretty_join(song.get_contributing_artists()),
            "sp_url": spotify_url
        }
    )
