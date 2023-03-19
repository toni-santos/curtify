import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import subprocess
import datetime
import time
from tqdm import tqdm
import os
import cursor
import requests

load_dotenv()
cursor.hide()

def fetch_song(sp):
    results = sp.current_playback()

    if not results:
        print("Not playing anything...")
        exit(0)
        return None
        
        
    return results

def display_song(sp, song):
    os.system('clear')
    magenta = "\u001b[35m"
    end = "\u001b[0m"

    url = song['item']['album']['images'][1]['url']
    artists = [x['name'] for x in song['item']['album']["artists"]]
    title = song['item']['name']
    album = song['item']['album']['name']
    progress_val = song['progress_ms']/1000
    duration_val = song['item']['duration_ms']/1000
    id_ = song['item']['id']
    progress = datetime.datetime.fromtimestamp(progress_val).strftime('%M:%S')
    duration = datetime.datetime.fromtimestamp(duration_val).strftime('%M:%S')

    subprocess.run(["/usr/bin/kitty", "+kitten", "icat", "--align", "left", url])
    print(','.join(artists))
    print(album)
    print(title)

    progress_str = progress + ' - ' + duration
    print(progress_str)

    with tqdm(initial=int(progress_val), total=int(duration_val), ncols=34, bar_format='{bar}', colour="MAGENTA") as bar:
        for x in range(int(progress_val), int(duration_val)):
            new_song = fetch_song(sp)
            if new_song['item']['id'] != id_:
                return
            progress = datetime.datetime.fromtimestamp(x).strftime('%M:%S')
            progress_str = progress + ' - ' + duration
            print("\033[F", end="")
            print(progress_str)

            time.sleep(1)
            bar.update(1)

def main():
    scope = "user-read-playback-state"
    username = os.environ.get("USERNAME")
    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)

    while True:
        song = fetch_song(sp)

        if (song):
            display_song(sp, song)
    
if __name__ == '__main__':
    main()
