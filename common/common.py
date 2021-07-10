import urllib.request
from dataclasses import dataclass
from os import environ
from typing import Optional, List
from urllib import parse as urlparse
from urllib.parse import parse_qs

import pyyoutube
from pyyoutube import Video
from spotdl.search import audioProvider
from spotdl.search.metadataProvider import from_url


def get_thumbnail(id: str):
    return f"https://img.youtube.com/vi/{id}/0.jpg"


def get_data(id: str):
    data = urllib.request.urlopen(f"https://youtube.com/get_video_info?video_id={id}")
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


@dataclass(frozen=True)
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
        trackMetadata, artistMetadata, albumMetadata = from_url(spotify_url)
    except Exception:
        return None

    songName = trackMetadata["name"]
    albumName = trackMetadata["album"]["name"]
    isrc = trackMetadata["external_ids"].get("isrc")
    contributingArtists = []
    for artist in trackMetadata["artists"]:
        contributingArtists.append(artist["name"])
    duration = round(trackMetadata["duration_ms"] / 1000, ndigits=3)

    youtubeLink = audioProvider.search_and_get_best_match(
        songName, contributingArtists, albumName, duration
    )

    if youtubeLink is None:
        return None

    # Parse for youtube info
    parsed = urlparse.urlparse(youtubeLink)
    vid_id = parse_qs(parsed.query)['v'][0]
    videos: Optional[List[Video]] = youtube_api.get_video_by_id(video_id=vid_id).items

    # Catch when video ID fails
    if len(videos) == 0:
        return None

    thumbnail = "https://cdn.pixabay.com/photo/2013/07/12/17/47/test-pattern-152459_960_720.png"
    try:
        thumbnail = videos[0].snippet.thumbnails.maxres.url
    except AttributeError:
        try:
            thumbnail = videos[0].snippet.thumbnails.default.url
        except AttributeError:
            pass

    # If all that passes, return the found information
    return YoutubeData(
        **{
            "title": videos[0].snippet.title,
            "thumbnail": thumbnail,
            "yt_url": youtubeLink,
            "artists_5": pretty_join(contributingArtists, cutoff=5),
            "artists_3": pretty_join(contributingArtists),
            "sp_url": spotify_url
        }
    )
