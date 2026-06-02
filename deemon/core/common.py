import re
import logging
from deezer.utils import DefaultDict, is_explicit, RoleID
from deemon.core.config import Config as config

logger = logging.getLogger(__name__)


def exclude_filtered_versions(albums: list) -> list:
    """ Remove album versions containing specified text """
    exclusion_patterns = config.exclusion_patterns()
    exclusion_keywords = config.exclusion_keywords()
    allowed = []

    if exclusion_keywords or exclusion_patterns:
        for album in albums:
            album_title = album['title']
            exclusion_pattern_match = [p for p in exclusion_patterns if re.search(p, album_title)]
            keyword_search = re.search(r'\(([^)]+)\)|\[([^)]+)]', album_title.lower())
            exclusion_keyword_match = [e for e in exclusion_keywords if keyword_search and e in keyword_search.group()]
            result = exclusion_pattern_match + exclusion_keyword_match
            result = '", "'.join(result)

            if exclusion_keyword_match or exclusion_pattern_match:
                logger.info(f"    Album \"{album_title}\" excluded by filter: \"{result}\"")
                continue
            else:
                allowed.append(album)
        return allowed
    else:
        return albums

def map_track(track):
    """maps gw-light api tracks to standard api (mock of deezer.utils.map_track)"""
    track = DefaultDict(track)
    result = {
        'id': track['SNG_ID'],
        'readable': True, # not provided
        'title': track['SNG_TITLE'],
        'title_short': track['SNG_TITLE'],
        'isrc': track['ISRC'],
        'link': f"https://www.deezer.com/track/{track['SNG_ID']}",
        'share': f"https://www.deezer.com/track/{track['SNG_ID']}",
        'duration': track['DURATION'],
        'bpm': None, # not provided
        'available_countries': [], # not provided
        'contributors': [],
        'md5_image': track['ALB_PICTURE'],
        'artist': {
            'id': track['ART_ID'],
            'name': track['ART_NAME'],
            'link': f"https://www.deezer.com/artist/{track['ART_ID']}",
            'share': f"https://www.deezer.com/artist/{track['ART_ID']}",
            'picture': f"https://www.deezer.com/artist/{track['ART_ID']}/image",
            'radio': None, # not provided
            'tracklist': f"https://api.deezer.com/artist/{track['ART_ID']}/top?limit=50",
            'type': "artist"
        },
        'album': {
            'id': track['ALB_ID'],
            'title': track['ALB_TITLE'],
            'link': f"https://www.deezer.com/album/{track['ALB_ID']}",
            'cover': f"https://api.deezer.com/album/{track['ALB_ID']}/image",
            'cover_small': f"https://e-cdns-images.dzcdn.net/images/cover/{track['ALB_PICTURE']}/56x56-000000-80-0-0.jpg",
            'cover_medium': f"https://e-cdns-images.dzcdn.net/images/cover/{track['ALB_PICTURE']}/250x250-000000-80-0-0.jpg",
            'cover_big': f"https://e-cdns-images.dzcdn.net/images/cover/{track['ALB_PICTURE']}/500x500-000000-80-0-0.jpg",
            'cover_xl': f"https://e-cdns-images.dzcdn.net/images/cover/{track['ALB_PICTURE']}/1000x1000-000000-80-0-0.jpg",
            'md5_image': track['ALB_PICTURE'],
            'release_date': None, # not provided
            'tracklist': f"https://api.deezer.com/album/{track['ALB_ID']}/tracks",
            'type': "album"
        },
        'type': "track",
        # Extras
        'md5_origin': track['MD5_ORIGIN'],
        'filesizes': {
            'default': track['FILESIZE']
        },
        'media_version': track['MEDIA_VERSION'],
        'track_token': track['TRACK_TOKEN'],
        'track_token_expire': track['TRACK_TOKEN_EXPIRE']
      }
    if int(track['SNG_ID']) > 0:
        result['title_version'] = track.get('VERSION', "").strip()
        if result['title_version'] != "" and result['title_version'] in result['title_short']:
            result['title_short'] = result['title_short'].replace(result['title_version'], "").strip()
        result['title'] = f"{result['title_short']} {result['title_version']}".strip()
        result['track_position'] = track.get('TRACK_NUMBER', 0)
        result['disk_number'] = track.get('DISK_NUMBER', 0)
        result['rank'] = track.get('RANK') or track.get('RANK_SNG')
        result['release_date'] = track.get('PHYSICAL_RELEASE_DATE')
        result['explicit_lyrics'] = is_explicit(track['EXPLICIT_LYRICS'])
        result['explicit_content_lyrics'] = track.get('EXPLICIT_TRACK_CONTENT', {}).get('EXPLICIT_LYRICS_STATUS')
        result['explicit_content_cover'] = track.get('EXPLICIT_TRACK_CONTENT', {}).get('EXPLICIT_COVER_STATUS')
        result['preview'] = None
        if track.get('MEDIA', []):
            result['preview'] = track['MEDIA'][0].get('HREF')
        result['gain'] = track.get('GAIN')
        if 'ARTISTS' in track:
            for contributor in track['ARTISTS']:
                contributor = DefaultDict(contributor)
                if contributor['ART_ID'] == result['artist']['id']:
                    result['artist']['picture_small'] = f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/56x56-000000-80-0-0.jpg"
                    result['artist']['picture_medium'] = f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/250x250-000000-80-0-0.jpg"
                    result['artist']['picture_big'] = f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/500x500-000000-80-0-0.jpg"
                    result['artist']['picture_xl'] = f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/1000x1000-000000-80-0-0.jpg"
                    result['artist']['md5_image'] = contributor['ART_PICTURE']
                result['contributors'].append({
                    'id': contributor['ART_ID'],
                    'name': contributor['ART_NAME'],
                    'link': f"https://www.deezer.com/artist/{contributor['ART_ID']}",
                    'share': f"https://www.deezer.com/artist/{contributor['ART_ID']}",
                    'picture': f"https://www.deezer.com/artist/{contributor['ART_ID']}/image",
                    'picture_small': f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/56x56-000000-80-0-0.jpg",
                    'picture_medium': f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/250x250-000000-80-0-0.jpg",
                    'picture_big': f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/500x500-000000-80-0-0.jpg",
                    'picture_xl': f"https://e-cdns-images.dzcdn.net/images/artist/{contributor['ART_PICTURE']}/1000x1000-000000-80-0-0.jpg",
                    'md5_image': contributor['ART_PICTURE'],
                    'tracklist': f"https://api.deezer.com/artist/{contributor['ART_ID']}/top?limit=50",
                    'type': "artist",
                    'role': RoleID[contributor['ROLE_ID']],
                    # Extras
                    'order': contributor['ARTISTS_SONGS_ORDER'],
                    'rank': contributor['RANK']
                })
        # Extras
        result['lyrics_id'] = track['LYRICS_ID']
        result['physical_release_date'] = track['PHYSICAL_RELEASE_DATE']
        result['song_contributors'] = track['SNG_CONTRIBUTORS']
        if 'FALLBACK' in track: result['fallback_id'] = track.get('FALLBACK').get('SNG_ID')
        if 'DIGITAL_RELEASE_DATE' in track: result['digital_release_date'] = track['DIGITAL_RELEASE_DATE']
        if 'GENRE_ID' in track: result['genre_id'] = track['GENRE_ID']
        if 'COPYRIGHT' in track: result['copyright'] = track['COPYRIGHT']
        if 'LYRICS' in track: result['lyrics'] = track['LYRICS']
        if 'ALBUM_FALLBACK' in track: result['alternative_albums'] = track['ALBUM_FALLBACK']
        result['filesizes']['aac_64'] = track['FILESIZE_AAC_64']
        result['filesizes']['mp3_64'] = track['FILESIZE_MP3_64']
        result['filesizes']['mp3_128'] = track['FILESIZE_MP3_128']
        result['filesizes']['mp3_256'] = track['FILESIZE_MP3_256']
        result['filesizes']['mp3_320'] = track['FILESIZE_MP3_320']
        result['filesizes']['mp4_ra1'] = track.get('FILESIZE_MP4_RA1')
        result['filesizes']['mp4_ra2'] = track.get('FILESIZE_MP4_RA2')
        result['filesizes']['mp4_ra3'] = track.get('FILESIZE_MP4_RA3')
        result['filesizes']['flac'] = track['FILESIZE_FLAC']
    else:
        result['token'] = track['TOKEN']
        result['user_id'] = track['USER_ID']
        result['filesizes']['mp3_misc'] = track['FILESIZE_MP3_MISC']
    return result
