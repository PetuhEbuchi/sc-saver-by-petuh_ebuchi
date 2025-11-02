import requests
import time
from os import system as sys

sys("cls")
print()
print(
"""
          
     ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀█▀▀▄  ▄▀▀▄ ▄▀▀▄  ▄▀▀▄ ▄▄ 
    █   █   █ ▐  ▄▀   ▐ █    █  ▐ █   █    █ █  █   ▄▀
    ▐   █▀▀▀▀    █▄▄▄▄▄  ▐   █     ▐  █    █  ▐  █▄▄▄█ 
        █        █    ▌     █        █    █      █   █ 
      ▄▀        ▄▀▄▄▄▄    ▄▀          ▀▄▄▄▄▀    ▄▀  ▄▀ 
     █          █    ▐    █                     █   █   
    ▐          ▐         ▐                     ▐   ▐ 

      
""")

print()

def track():
    client_id = input("client_id=")
    track_url = input("track url: ")

    if "client_id=" in client_id:
        client_id = client_id.replace("client_id=", "")
    if "client_id" in client_id:
        client_id = client_id.replace("client_id", "")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }

    response = requests.get(f"https://api-v2.soundcloud.com/resolve?url={track_url}&client_id={client_id}", headers=headers)

    if response.status_code == 200:
        track_data = response.json()

  
        progressive_url = None
        for target in track_data['media']['transcodings']:
            if "progressive" in target['url']:
                progressive_url = target['url']
                break



        track_file_link = requests.get(f"{progressive_url}?client_id={client_id}", headers=headers)
        download_url = track_file_link.json()['url']
            
        print(f"Track name: {track_data['title']}")
        print(f"Download URL: {download_url}")
        print()


        clean_title = (track_data['title']
            .replace("/", " ")
            .replace("\\", " ") 
            .replace(":", " - ")
            .replace("*", " ")
            .replace("?", " ")
            .replace("\"", " ")
            .replace("<", " ")
            .replace(">", " ")
            .replace("|", " "))

        save = input("Do you want to save this track? [Y/N] ")

        if save.lower() == "y":

            download = requests.get(download_url, stream=True)
            filename = f"{clean_title}.mp3"
                
            print(f"Downloading: {clean_title}")
            with open(filename, "wb") as file:
                for chunk in download.iter_content(8192):
                    file.write(chunk)
            print("Done!")


def playlist():
    client_id = input("client_id=")

    track_names =[]
    track_links = []

    if "client_id=" in client_id:
        client_id = client_id.replace("client_id=", "")
    if "client_id" in client_id:
        client_id = client_id.replace("client_id", "")
    playlist_url = input("Playlist link: ")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }


    response = requests.get(f"https://api-v2.soundcloud.com/resolve?url={playlist_url}&client_id={client_id}", headers=headers)

    if response.status_code == 200:
        playlist_data = response.json()

        sys("cls")


        print(f"{"=" * 20} STATUS CODE {"=" * 20}\n")
        print(f"connected to soundcloud api")
        print()


        print(f"{"=" * 19} PLAYLSIT INFO {"=" * 19}\n")
        print(f"Playlist id = {playlist_data['id']}")
        print(f"Playlist avatar = {playlist_data['artwork_url']}")
        print(f"Playlist name = {playlist_data['title']}")
        print(f"Made by {playlist_data['user']['username']} | {playlist_data['user']['permalink']} | {playlist_data['user']['id']}")
        print(f"Track count = {playlist_data['track_count']}")
        print()


        print(f"{"=" * 22} TRACKS INFO {"=" * 21}\n")
        tracks = playlist_data['tracks']
        for track in tracks:
            track_id = str(track['id'])
            print(track_id)
        print()


        print(f"{"=" * 22} TRACKS LINKS {"=" * 21}\n")
        tracks = playlist_data['tracks']
        count = 0
        for track in tracks:
            
            track_id = str(track['id'])
            track_response = requests.get(f"https://api-v2.soundcloud.com/tracks/{track_id}?client_id={client_id}", headers=headers)
            track_data = track_response.json()
            

            for targets in track_data['media']['transcodings']:
                
                for url in targets.values():
                    if "progressive" in str(url):
                        count += 1

                        track_file_link = requests.get(f"{str(url)}?client_id={client_id}", headers=headers)
                        
                        print(f"track name = {track_data['title']} | {count} / {playlist_data['track_count']}")
                        
                        print(track_file_link.json()['url'])


                        track_names.append(track_data['title'])
                        track_links.append(track_file_link.json()['url'])
                        
                        


                        print()
                        
                        break



        for i in range(len(track_names)):
            invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
            for char in invalid_chars:
                if char in track_names[i]:
                    track_names[i] = track_names[i].replace(char, " ")



        def save_or_not(link, trackname, playlistname):
            download = requests.get(link, stream = True)
            with open(f"{playlistname}/{trackname}.mp3", "wb") as file:
                for chunk in download.iter_content(8192):
                    file.write(chunk)


        save = input("Do you want to save tracks? [Y/N] ")


        
        if save == "Y" or save == "y":
            sys(f"mkdir {playlist_data['title']}")
            for i in range(len(track_links)):
                print(f"Downloading: {track_names[i]}")
                save_or_not(track_links[i], track_names[i], playlist_data['title'])
                print("Done!")
                print()

        elif save == "N" or save == "n":
            pass

        else:
            print("Incorrect input")
            pass


    else:
        print("eror")


print()
x = input("1 - track\n2 - playlist\n")
if x == "1":
    track()
elif x == "2":
    playlist()
else:
    pass



print("\n\n\n\n\n\n")
print(
"""
          
     ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀█▀▀▄  ▄▀▀▄ ▄▀▀▄  ▄▀▀▄ ▄▄ 
    █   █   █ ▐  ▄▀   ▐ █    █  ▐ █   █    █ █  █   ▄▀
    ▐   █▀▀▀▀    █▄▄▄▄▄  ▐   █     ▐  █    █  ▐  █▄▄▄█ 
        █        █    ▌     █        █    █      █   █ 
      ▄▀        ▄▀▄▄▄▄    ▄▀          ▀▄▄▄▄▀    ▄▀  ▄▀ 
     █          █    ▐    █                     █   █   
    ▐          ▐         ▐                     ▐   ▐ 

    
""")


sys("pause")