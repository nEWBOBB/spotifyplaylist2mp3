import os
import logging
from youtubesearchpython import VideosSearch
from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up Spotify credentials
client_id = 'c15970bcd75a4ec2bb4492b2f02ae0e3'
client_secret = '20f26dbd28eb448f84f6a99625d2e01f'

# Playlist ID to retrieve
playlist_id = '4Sti4HqaSlWbWJiiHhCmIT'

# Set up PyTube download directory
DOWNLOAD_DIR = 'downloads'


def search_youtube_videos(search_terms):
    """Searches for YouTube videos given a list of search terms."""
    youtube_links = []

    for term in search_terms:
        # Remove leading/trailing whitespaces and newlines from the search term
        term = term.strip()

        try:
            # Search for videos on YouTube
            search = VideosSearch(term, limit=1)
            results = search.result()
            link = results['result'][0]['link']
            youtube_links.append(link)
            logging.info(f"Found YouTube link for '{term}': {link}")
        except Exception as e:
            # Log any exceptions that occur during the search process
            logging.error(f"Error occurred while searching YouTube for '{term}': {str(e)}")
            raise

    return youtube_links


def download_youtube_video_as_mp3(link):
    """Downloads a YouTube video as an MP3."""
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        mp3_filename = f"{stream.default_filename.replace('.mp4', '')}.mp3"
        logging.info(f"Downloading MP3: {link}")
        return stream.download(output_path=DOWNLOAD_DIR, filename=mp3_filename)
    except Exception as e:
        logging.warning(f"Download failed for link {link}: {str(e)}")
        return None


def main():
    try:
        # Set up Spotify authentication
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        # Retrieve playlist data from Spotify
        playlist = sp.playlist(playlist_id)
        tracks = playlist['tracks']['items']

        # Extract track names and artists from the playlist
        search_terms = [f"{track['track']['name']} {', '.join([artist['name'] for artist in track['track']['artists']])}" for
                        track in tracks]

        # Search for YouTube links
        youtube_links = search_youtube_videos(search_terms)

        # Filter out any None values from the search results
        youtube_links = list(filter(None, youtube_links))

        # Download YouTube videos as MP3
        downloaded_mp3_files = []
        for link in youtube_links:
            mp3_path = download_youtube_video_as_mp3(link)
            if mp3_path is not None:
                downloaded_mp3_files.append(mp3_path)
                logging.info(f"Downloaded MP3: {mp3_path}")

        logging.info("YouTube video download as MP3 completed successfully.")

        # Rename the MP3 files to have the artist and track name from Spotify
        for mp3_file_path in downloaded_mp3_files:
            track = sp.track(os.path.basename(mp3_file_path))
            artist = track['artists'][0]['name']
            track_name = track['name']
            os.rename(mp3_file_path, f"{artist}_{track_name}.mp3")

        # Create a subfolder in the downloads directory with the name of the Spotify playlist
        playlist_name = sp.playlist(playlist_id)['name']
        download_dir = os.path.join(DOWNLOAD_DIR, playlist_name)
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        # Move the MP3 files to the subfolder
        for mp3_file_path in downloaded_mp3_files:
            os.rename(mp3_file_path, os.path.join(download_dir, os.path.basename(mp3_file_path)))

        logging.info("MP3 files downloaded and moved to subfolder successfully.")

        # Print the paths to the downloaded MP3 files
        for mp3_file_path in downloaded_mp3_files:
            logging.info(f"Download successful. The MP3 file is located at: {mp3_file_path}")

    except Exception as e:
        # Log any exceptions that occur during the main process
        logging.error(f"An error occurred during playlist retrieval and downloading MP3s: {str(e)}")
        raise


if __name__ == "__main__":
    main()

