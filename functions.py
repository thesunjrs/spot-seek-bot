import subprocess
import os
from variables import directory, bot_api, warp_mode
from spotify import get_track_image
import requests

def download(track_link):
    # download track
    print(f"start downloading: {track_link}")
    normal_download_command = ['../spotdl', "--bitrate", "320k", track_link] # nomal download
    warp_download_command = ['proxychains', '-f', '../proxychains.conf', '../spotdl', "--bitrate", "320k", track_link] # download with warp
    command = warp_download_command if warp_mode else normal_download_command
    subprocess.run(command, cwd=directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"end downloading: {track_link}")

    # download cover image
    image_url = get_track_image(track_link)
    print(f"start downloading cover image: {image_url}")
    subprocess.run(f"wget -O cover.jpg -o /dev/null \"{image_url}\"", shell=True, cwd=directory)
    print(f"end downloading cover image: {image_url}")

def file_list(directory):
    return [file for file in os.listdir(directory) if file.endswith(".mp3")]

def clear_files(folder_path):
    directory = folder_path
    # note: there is a .gitkeep file in output folder

    for filename in os.listdir(directory):
        if filename != ".gitkeep":
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")

def check_membership(channel, user):
    # Send a request to the Telegram Bot API
    response = requests.get(f'https://api.telegram.org/bot{bot_api}/getChatMember', params={'chat_id': channel, 'user_id': user})

    # Parse the response
    data = response.json()
    if data['ok']:
        member_status = data['result']['status']
        if member_status in ['member', 'creator', 'administrator']:
            print('The user is a member of the channel.')
            return True
        else:
            print('The user is not a member of the channel.')
            return False
    else:
        print('Failed to retrieve chat member information.')
        return False

