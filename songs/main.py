# This program takes data from the Spotify API and generate song pages for them
# ----------Getting Started----------
# Run "main.py" and update "auth.json". Then, run "json" when prompted.
#   - If "songData.json" doesn't exist, it will generate a new .json file
#   - If "songData.json" DOES exist, it will compare "spotifyReleases.json" to it, and if
#   a release isn't in "songData.json", it will auto-add the entry
#       - Manually update fields from "songData.json"
#   - If it is up-to-date, it will do nothing
# Then, type in "generate" to generate song pages.
#   - Uses data from both "spotifyReleases.json" and "songData.json"
#       - If "songData.json" isnt updated, will prompt user to run the command "json" first
#       - If "songData.json" is updated, wil generate .html pages based on data in
#       "songData.json"
# Verify the new .html file have correct information
# Push to Github to see changes
#
# ----------Updating After a New Release----------
# After a new release is posted on Spotify, type in 'update' and follow the prompts.
#
# ----------Regenerating Pages----------
# After updating the template, type in "regenerate", when prompted, to re-create all the song pages.
#
# ----------Deleting Generated Pages----------
# To delete all generated song pages, type in "deleteAll" when prompted
#
# ----------Listing Pages----------
# To view song list, type in "list"
#   - To list all songs that have a generated .html page, type in "1" when prompted
#   - To list all songs within "spotifyReleases.json", type in "2" when prompted
#   - To list all songs within "songData.json", type in "3" when prompted
# ------------------------------------------
import json
import os
import spotipy as s
from spotipy.oauth2 import SpotifyClientCredentials


debugMode = False
ARTIST_ID = "7ibBcoqSGVKT1sBynZvy5e"  # beanloaf


def main():
    if not hasAuth():
        return

    print('\033[95m' + "Program made by @beanloaf to help make updating https://beanloaf.github.io/ easier to update." + '\033[0m')
    print('\033[95m' + "To list all commands, type in, 'help'." + '\033[0m')

    hasNext = True

    while hasNext:
        d = input('\033[96m' + "Enter a command: " + '\033[0m')
        if d == "help":
            doc()
        elif d == "generate":
            generateSongs(True)
        elif d == "regenerate":
            deleteAllSongs()
            generateSongs()
        elif d == "deleteAll":
            deleteAllSongs()
        elif d == "list":
            listSongs()
        elif d == "json":
            modifyJson()
        elif d == "update":
            update()
        elif d == "exit":
            return

        else:
            ERROR("Invalid command.")


def doc() -> None:
    """
    Shows user all possible commands.
    """
    OPTION("To generate the song list, type in, 'generate'.")
    OPTION("To regenerate the song list, type in, 'regenerate'.")
    OPTION("To delete the song list, type in, 'deleteAll'.")
    OPTION("To list all the songs, type in, 'list'")
    OPTION("To generate the song json, type in, 'json'.")
    OPTION("To update for a new release, do 'update'.")
    OPTION("To exit, type in, 'exit'")


def update() -> None:
    """
    When a new song releases on Spotify, updates songData.json and generates page.
    """
    modifyJson()
    WARN("Manually update and verify that all fields in songData.json is correct, then type in 'continue' to generate the pages.")
    hasNext = True

    while hasNext:
        d = input(
            '\033[96m' + "Enter 'continue' to proceed, or 'exit' to return to main menu: " + '\033[0m')

        if d == "continue":
            generateSongs(False)
        elif d == "exit":
            return
        else:
            ERROR("Invalid input.")


def hasAuth() -> bool:
    """
    Checks whether the user has auth.json. 
    If file not found, generates a empty auth.json and returns False. Else, returns true.
    """
    if not os.path.exists("auth.json"):
        WARN("WARNING: auth.json not found. Generating file; please update auth.json with the proper credentials, then re-run the program.")
        with open("auth.json", "a+") as d:
            d.write('[\n{\n"cid": "CLIENT_ID",\n"cs": "CLIENT_SECRET"\n}\n]')
        return False
    return True


def generateSongs(debug: bool) -> None:
    """
    Generates song pages based on data in songData.json
    """
    content = ""

    if not os.path.exists("songs/spotifyReleases.json"):
        ERROR("'spotifyReleases.json' not found inside directory 'songs'. Exiting...")
        return

    if not os.path.exists("songs/songData.json"):
        ERROR("'songData.json' not found inside directory 'songs'. Exiting...")
        return

    with open('songs/spotifyReleases.json', 'r') as f:
        spotifyData = json.load(f)
    with open('songs/songData.json', 'r') as f:
        songData = json.load(f)

    numGeneratedPages = len(spotifyData["items"])

    if len(spotifyData["items"]) != len(songData):
        ERROR("songData.json isn't updated. Run the command 'json' to update it.")
        return
    else:
        for i in range(len(spotifyData["items"])):
            # --------------
            # Fallback values
            songName = spotifyData["items"][i]["name"]
            songImg = ""
            spotifyLink = "https://open.spotify.com/artist/7ibBcoqSGVKT1sBynZvy5e?si=3PvUSUKOQGCp6DqHbSrVkQ"
            youtubeLink = "https://youtube.com/@beanloaf"
            appleLink = "https://music.apple.com/us/artist/beanloaf/1579680943"
            albumType = "Album"
            albumID = "N/A"
            releaseDate = "N/A"
            # --------------

            with open("songs/templateSong.html") as h:
                content = h.read()

            for j in range(len(spotifyData["items"])):
                if spotifyData["items"][i]["name"] == songData[j]["name"]:
                    songName = songData[j]["name"]
                    songImg = songData[j]["songImg"]
                    spotifyLink = songData[j]["spotifyURL"]
                    youtubeLink = songData[j]["youtubeURL"]
                    appleLink = songData[j]["appleURL"]

            try:
                newPage = open("songs/-" + songName + ".html", "x")

            except:
                if debug:
                    WARN("Skipping " + songName +
                         ", since a page for it already exists.")
                numGeneratedPages -= 1
                continue

            if spotifyData["items"][i]["total_tracks"] > 4:
                albumType = "Album"
            elif spotifyData["items"][i]["total_tracks"] > 1:
                albumType = "EP"
            elif spotifyData["items"][i]["total_tracks"] == 1:
                albumType = "Single"

            _s = spotifyData["items"][i]["release_date"].split("-")
            releaseDate = _s[1] + "/" + _s[2] + "/" + _s[0]

            albumID = spotifyData["items"][i]["id"]

            content = content.format(
                songName=songName,
                songImg=songImg,
                spotifyLink=spotifyLink,
                youtubeLink=youtubeLink,
                appleLink=appleLink,
                albumType=albumType,
                releaseDate=releaseDate,
                albumID=albumID
            )

            try:
                newPage.write(content)
                newPage.close()
            except:
                pass
        print('\033[4m' + "Generated " +
              str(numGeneratedPages) + " pages." + '\033[0m')
        SUCCESS("Finished creating song pages.")


def deleteAllSongs() -> None:
    """
    Deletes all auto-generated .html pages, denoted with a '-' before the song name in the 'songs/' directory.
    """
    WARN("Are you sure you want to delete song htmls? All manually inputed song data will be lost.")
    d = input(
        '\033[96m' + "Type in 'deleteAll confirm' to proceed: " + '\033[0m')

    if d == "deleteAll confirm":
        for filename in os.listdir('songs'):
            path = os.path.join('songs', filename)
            if filename[0] == "-":
                print("Deleting", filename)
                os.remove(path)
        SUCCESS("Finished deleting.")
    else:
        ERROR("Invalid input; returning to main menu.")


def listSongs() -> None:
    """
    Displays all songs listed under the 'songs/' directory, inside 'songData.json', or inside 'spotifyReleases.json'.
    """
    OPTION("To list all songs that have a .html page, type in '1'.")
    OPTION("To list all songs listed in the Spotify .json, type in '2'.")
    OPTION("To list all songs listed in songData.json, type in '3'.")

    d = input("Enter a number: ")

    if d == "1":
        for filename in os.listdir('songs'):
            if filename[0] == "-":
                print(filename)
    elif d == "2":
        with open('songs/spotifyReleases.json', 'r') as d:
            _data = json.load(d)

        for i in range(len(_data["items"])):
            print(_data["items"][i]["name"])
    elif d == "3":
        with open('songs/songData.json', 'r') as f:
            data = json.load(f)
        for i in range(len(data)):
            print(data[i]["name"])
    else:
        ERROR("Invalid input.")

    SUCCESS("Finished listing.")


def modifyJson() -> None:
    """
    Creates/updates both 'spotifyReleases.json' and 'songData.json' in stages:
        - Updates 'spotifyReleases.json' to latest, then:
        - Updates 'songData.json' based on 'spotifyReleases.json'
    """
    try:
        with open('auth.json', 'r') as f:
            auth = json.load(f)
    except:
        ERROR("ERROR: auth.json couldn't be found. Exiting...")
        return

    # Uses Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=auth[0]["cid"], client_secret=auth[0]["cs"])
    sp = s.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.artist_albums(
        'spotify:artist:' + ARTIST_ID)

    if not os.path.exists("songs/spotifyReleases.json"):
        WARN("spotifyReleases.json doesn't exist; creating new file...")
        with open("songs/spotifyReleases.json", "a+") as a:
            a.write(json.dumps(results))
    elif os.path.exists("songs/spotifyReleases.json"):
        WARN("Found spotifyReleases.json. Updating the file...")
        os.remove("songs/spotifyReleases.json")
        with open("songs/spotifyReleases.json", "a+") as a:
            a.write(json.dumps(results))

    if not os.path.exists("songs/songData.json"):
        WARN("songData.json doesn't exist; creating new file...")
        d = open("songs/songData.json", "a+")
        d.write("[")
        song = {
            "name": results["items"][0]["name"],
            "songImg": results["items"][0]["images"][0]["url"],
            "spotifyURL": results["items"][0]["uri"],
            "youtubeURL": "",
            "appleURL": ""
        }
        d.write(json.dumps(song))
        for i in range(1, len(results["items"])):
            d.write(",")
            song = {
                "name": results["items"][i]["name"],
                "songImg": results["items"][i]["images"][0]["url"],
                "spotifyURL": results["items"][i]["uri"],
                "youtubeURL": "",
                "appleURL": ""
            }
            d.write(json.dumps(song))
        d.write("]")
        d.close()
        SUCCESS("Finished creating songData.json")

    elif os.path.exists("songs/songData.json"):
        numAddedEntries = 0
        WARN("songData.json exists; reading file...")
        try:
            with open('songs/songData.json', 'r') as g:
                _data = json.load(g)
        except:
            ERROR("ERROR: songData.json has invald formatting. Fix formatting error, \
or delete songData.json and run 'json' to regenerate file.")
            return

        for i in range(len(results["items"])):
            foundMatch = False

            for j in range(len(_data)):
                if debugMode:
                    print("Comparing", results["items"][i]
                          ["name"], "and", _data[j]["name"])

                if results["items"][i]["name"] == _data[j]["name"]:
                    foundMatch = True

            if not foundMatch:
                WARN(results["items"][i]["name"] +
                     " not found in songData.json. Attempting to add entry...")
                numAddedEntries += 1
                _song = {
                    "name": results["items"][i]["name"],
                    "songImg": results["items"][i]["images"][0]["url"],
                    "spotifyURL": results["items"][i]["uri"],
                    "youtubeURL": "",
                    "appleURL": ""
                }

                songDatab = open("songs/songData.json", "ab+")
                songDatab.seek(-1, os.SEEK_END)
                songDatab.truncate()  # removes the last character of the .json file; should be a ']'
                songDatab.close()

                songData = open("songs/songData.json", "a+")
                songData.write("," + json.dumps(_song))
        try:
            songData.write("]")
            songData.close()
        except:
            pass
        if numAddedEntries == 0:
            SUCCESS("songData.json up-to-date; no changes made.")
        elif numAddedEntries > 0:
            SUCCESS("Finished updating songData.json; added " +
                    str(numAddedEntries) + " entries.")


"""
These functions are for color-coding messages in the terminal for clarity.
"""


def WARN(s: str) -> None:
    print('\033[93m' + s + '\033[0m')


def SUCCESS(s: str) -> None:
    print('\033[92m' + s + '\033[0m')


def OPTION(s: str) -> None:
    print('\033[94m' + s + '\033[0m')


def ERROR(s: str) -> None:
    print('\033[91m' + s + '\033[0m')


"""
Console color guide:
'\033[95m' = Purple ish
'\033[94m' = Blue
'\033[96m' = Cyan/Light Blue
'\033[92m' = Green
'\033[93m' = Yellow
'\033[91m' = Red

'\033[1m' = Bold
'\033[4m' = Underline

'\033[0m' = Reset
"""

if __name__ == "__main__":
    main()
