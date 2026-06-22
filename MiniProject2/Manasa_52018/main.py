# Vehicle Infotainment System


import json
import os
from datetime import datetime

# the file where all data gets saved
DATA_FILE = "infotainment_data.json"

# the pre-loaded song/podcast/audiobook library
LIBRARY_FILE = "songs_library.json"


# -------------------------------------------------------------------
# MediaItem class - stores info about a single song or audio file
# -------------------------------------------------------------------

class MediaItem:

    def __init__(self, title, artist, media_type="song"):
        self.title = title
        self.artist = artist
        self.media_type = media_type  # song, podcast, or audiobook

    # converts the object into a plain dictionary for saving to file
    def to_dict(self):
        data = {}
        data["title"] = self.title
        data["artist"] = self.artist
        data["media_type"] = self.media_type
        return data

    def display(self):
        print(f"  {self.title} by {self.artist} [{self.media_type}]")


# -------------------------------------------------------------------
# Playlist class - a named collection of songs
# -------------------------------------------------------------------

class Playlist:

    def __init__(self, name):
        self.name = name
        self.songs = []  # list that holds MediaItem objects

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, title):
        new_list = []
        found = False
        for song in self.songs:
            if song.title.lower() == title.lower():
                found = True  # don't add this one back
            else:
                new_list.append(song)
        self.songs = new_list
        return found

    # returns the songs sorted by title, artist, or type
    def show_songs(self, sort_by="title"):
        if sort_by == "title":
            sorted_list = sorted(self.songs, key=lambda s: s.title.lower())
        elif sort_by == "artist":
            sorted_list = sorted(self.songs, key=lambda s: s.artist.lower())
        else:
            sorted_list = sorted(self.songs, key=lambda s: s.media_type.lower())
        return sorted_list

    def to_dict(self):
        song_list = []
        for song in self.songs:
            song_list.append(song.to_dict())
        return {"name": self.name, "songs": song_list}


# -------------------------------------------------------------------
# RadioStation class - stores a saved FM station
# -------------------------------------------------------------------

class RadioStation:

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency  # MHz value like 98.5

    def to_dict(self):
        return {"name": self.name, "frequency": self.frequency}

    def display(self):
        print(f"  {self.name} - {self.frequency:.1f} MHz")


# -------------------------------------------------------------------
# User class - one profile in the system
# uses a dictionary for playlists and lists for stations/history
# -------------------------------------------------------------------

class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "User"
        self.playlists = {}       # key = playlist name, value = Playlist object
        self.stations = []        # list of RadioStation objects
        self.recently_played = [] # list of dicts with song info + timestamp

    def add_playlist(self, name):
        if name in self.playlists:
            print(f"  A playlist called '{name}' already exists.")
            return False
        self.playlists[name] = Playlist(name)
        return True

    def remove_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]
            return True
        return False

    def add_station(self, station):
        self.stations.append(station)

    def remove_station(self, name):
        new_list = []
        found = False
        for s in self.stations:
            if s.name.lower() == name.lower():
                found = True
            else:
                new_list.append(s)
        self.stations = new_list
        return found

    # filter stations using lambda - only keep ones within the given range
    def filter_stations(self, min_freq, max_freq):
        result = list(filter(lambda s: min_freq <= s.frequency <= max_freq, self.stations))
        return result

    def get_stations_sorted(self):
        return sorted(self.stations, key=lambda s: s.frequency)

    def play_song(self, song):
        entry = {
            "title": song.title,
            "artist": song.artist,
            "media_type": song.media_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # newest song goes to the front of the list
        self.recently_played.insert(0, entry)
        # only keep the last 10 songs in history
        if len(self.recently_played) > 10:
            self.recently_played = self.recently_played[:10]

    def get_recent_sorted(self, newest_first=True):
        return sorted(self.recently_played, key=lambda e: e["timestamp"], reverse=newest_first)

    def to_dict(self):
        playlists_data = {}
        for name, pl in self.playlists.items():
            playlists_data[name] = pl.to_dict()

        stations_data = []
        for s in self.stations:
            stations_data.append(s.to_dict())

        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "playlists": playlists_data,
            "stations": stations_data,
            "recently_played": self.recently_played
        }


# -------------------------------------------------------------------
# AdminUser class - inherits from User, gets extra admin powers
# -------------------------------------------------------------------

class AdminUser(User):

    def __init__(self, username, password):
        super().__init__(username, password)  # runs User's __init__ first
        self.role = "Admin"

    def list_all_users(self, all_users):
        print("\n  All profiles in the system:")
        for uname, user_obj in all_users.items():
            print(f"   - {uname} [{user_obj.role}]")

    def delete_user(self, all_users, username):
        if username == self.username:
            print("  You can't delete your own account.")
            return False
        if username not in all_users:
            print(f"  Couldn't find a user called '{username}'.")
            return False
        del all_users[username]
        return True


# -------------------------------------------------------------------
# File handling - saving and loading all data using JSON
# -------------------------------------------------------------------

def load_data():
    users = {}

    # if there's no save file yet, just start fresh with a default admin
    if not os.path.exists(DATA_FILE):
        print("[Info] No save file found. Starting with a fresh system.")
        users["admin"] = AdminUser("admin", "admin123")
        save_data(users)
        return users

    try:
        f = open(DATA_FILE, "r")
        raw = json.load(f)
        f.close()

        # go through each saved user and rebuild the objects
        for username, data in raw.items():
            if data["role"] == "Admin":
                user = AdminUser(data["username"], data["password"])
            else:
                user = User(data["username"], data["password"])

            # rebuild playlists
            for pl_name, pl_data in data["playlists"].items():
                pl = Playlist(pl_data["name"])
                for song_data in pl_data["songs"]:
                    song = MediaItem(song_data["title"], song_data["artist"], song_data["media_type"])
                    pl.songs.append(song)
                user.playlists[pl_name] = pl

            # rebuild radio stations
            for s_data in data["stations"]:
                station = RadioStation(s_data["name"], s_data["frequency"])
                user.stations.append(station)

            # recently played is already a list of plain dicts so no rebuilding needed
            user.recently_played = data["recently_played"]

            users[username] = user

        print(f"[Info] Loaded {len(users)} profile(s) successfully.")

    except json.JSONDecodeError:
        # this happens if the file got corrupted somehow (e.g. incomplete write)
        print("[Warning] Save file is corrupted. Starting fresh.")
        users["admin"] = AdminUser("admin", "admin123")
        save_data(users)

    except IOError:
        # something went wrong trying to open the file
        print("[Warning] Could not read save file. Starting fresh.")
        users["admin"] = AdminUser("admin", "admin123")
        save_data(users)

    return users


def save_data(users):
    try:
        all_data = {}
        for username, user in users.items():
            all_data[username] = user.to_dict()

        f = open(DATA_FILE, "w")
        json.dump(all_data, f, indent=2)
        f.close()

    except IOError:
        print("[Error] Something went wrong while saving. Your data might not have saved.")


# -------------------------------------------------------------------
# Library - loads the pre-filled songs_library.json file
# -------------------------------------------------------------------

def load_library():
    if not os.path.exists(LIBRARY_FILE):
        print("  [Info] No library file found. Make sure songs_library.json is in the same folder.")
        return []

    try:
        f = open(LIBRARY_FILE, "r")
        raw = json.load(f)
        f.close()

        # combine songs, podcasts, and audiobooks into one flat list
        all_items = []
        for category in raw:
            for item in raw[category]:
                all_items.append(item)
        return all_items

    except json.JSONDecodeError:
        print("  [Warning] Library file seems corrupted. Couldn't load it.")
        return []
    except IOError:
        print("  [Warning] Couldn't open the library file.")
        return []


# -------------------------------------------------------------------
# Input helpers - keeps asking until user gives valid input
# -------------------------------------------------------------------

def get_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if value < low or value > high:
                print(f"  Please enter a number between {low} and {high}.")
            else:
                return value
        except ValueError:
            print("  That's not a valid number. Try again.")


def get_float(prompt, low, high):
    while True:
        try:
            value = float(input(prompt))
            if value < low or value > high:
                print(f"  Please enter a value between {low} and {high}.")
            else:
                return value
        except ValueError:
            print("  Invalid input. Enter a number like 98.5")


def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("  This field can't be left empty.")
        else:
            return value


# -------------------------------------------------------------------
# Playlist menu
# -------------------------------------------------------------------

def playlist_menu(users, user):
    while True:
        print("\n--- Playlist Menu ---")
        print("1. View my playlists")
        print("2. Create a new playlist")
        print("3. Add a song to a playlist (type it in manually)")
        print("4. Browse library and add to a playlist")
        print("5. Remove a song from a playlist")
        print("6. View songs in a playlist")
        print("7. Delete a playlist")
        print("0. Go back")

        choice = get_int("Choose: ", 0, 7)

        if choice == 0:
            break

        elif choice == 1:
            if len(user.playlists) == 0:
                print("  You haven't created any playlists yet.")
            else:
                print("\n  Your playlists:")
                for name in user.playlists:
                    count = len(user.playlists[name].songs)
                    print(f"   - {name} ({count} song(s))")

        elif choice == 2:
            name = get_nonempty("  Playlist name: ")
            if user.add_playlist(name):
                save_data(users)
                print(f"  Created playlist '{name}'.")

        elif choice == 3:
            if len(user.playlists) == 0:
                print("  Create a playlist first.")
                continue
            print("  Your playlists:")
            for name in user.playlists:
                print(f"   - {name}")
            pl_name = get_nonempty("  Which playlist do you want to add to? ")
            if pl_name not in user.playlists:
                print("  Playlist not found.")
                continue
            title = get_nonempty("  Song title: ")
            artist = get_nonempty("  Artist name: ")
            print("  Media type:  1 = song   2 = podcast   3 = audiobook")
            type_choice = get_int("  Choose: ", 1, 3)
            if type_choice == 1:
                media_type = "song"
            elif type_choice == 2:
                media_type = "podcast"
            else:
                media_type = "audiobook"
            song = MediaItem(title, artist, media_type)
            user.playlists[pl_name].add_song(song)
            save_data(users)
            print(f"  Added '{title}' to '{pl_name}'.")

        elif choice == 4:
            # browse the pre-loaded library and pick something to add
            if len(user.playlists) == 0:
                print("  Create a playlist first.")
                continue
            library = load_library()
            if len(library) == 0:
                print("  Library is empty or couldn't be loaded.")
                continue

            # let the user filter by type first
            print("\n  What do you want to browse?")
            print("  1 = Songs   2 = Podcasts   3 = Audiobooks   4 = Everything")
            filter_choice = get_int("  Choose: ", 1, 4)

            if filter_choice == 1:
                filtered = [item for item in library if item["media_type"] == "song"]
            elif filter_choice == 2:
                filtered = [item for item in library if item["media_type"] == "podcast"]
            elif filter_choice == 3:
                filtered = [item for item in library if item["media_type"] == "audiobook"]
            else:
                filtered = library

            if len(filtered) == 0:
                print("  Nothing found in that category.")
                continue

            # show the list with numbers
            print(f"\n  Library ({len(filtered)} items):")
            for i in range(len(filtered)):
                item = filtered[i]
                print(f"   {i + 1}. {item['title']} - {item['artist']} [{item['media_type']}]")

            idx = get_int("\n  Enter the number of the item you want to add: ", 1, len(filtered))
            selected = filtered[idx - 1]

            # pick which playlist to add it to
            print("\n  Your playlists:")
            for name in user.playlists:
                print(f"   - {name}")
            pl_name = get_nonempty("  Add to which playlist? ")
            if pl_name not in user.playlists:
                print("  Playlist not found.")
                continue

            song = MediaItem(selected["title"], selected["artist"], selected["media_type"])
            user.playlists[pl_name].add_song(song)
            save_data(users)
            print(f"  Added '{selected['title']}' to '{pl_name}'.")

        elif choice == 5:
            if len(user.playlists) == 0:
                print("  You have no playlists.")
                continue
            pl_name = get_nonempty("  Remove a song from which playlist? ")
            if pl_name not in user.playlists:
                print("  Playlist not found.")
                continue
            title = get_nonempty("  Song title to remove: ")
            if user.playlists[pl_name].remove_song(title):
                save_data(users)
                print(f"  Removed '{title}' from '{pl_name}'.")
            else:
                print("  Couldn't find that song in the playlist.")

        elif choice == 6:
            if len(user.playlists) == 0:
                print("  You have no playlists.")
                continue
            pl_name = get_nonempty("  Which playlist? ")
            if pl_name not in user.playlists:
                print("  Playlist not found.")
                continue
            print("  Sort by:  1 = title   2 = artist   3 = type")
            sort_choice = get_int("  Choose: ", 1, 3)
            if sort_choice == 1:
                key = "title"
            elif sort_choice == 2:
                key = "artist"
            else:
                key = "media_type"
            songs = user.playlists[pl_name].show_songs(key)
            if len(songs) == 0:
                print("  This playlist is empty.")
            else:
                print(f"\n  Songs in '{pl_name}' sorted by {key}:")
                for i in range(len(songs)):
                    songs[i].display()

        elif choice == 7:
            if len(user.playlists) == 0:
                print("  You have no playlists.")
                continue
            pl_name = get_nonempty("  Which playlist do you want to delete? ")
            if user.remove_playlist(pl_name):
                save_data(users)
                print(f"  Deleted '{pl_name}'.")
            else:
                print("  Playlist not found.")


# -------------------------------------------------------------------
# Radio station menu
# -------------------------------------------------------------------

def radio_menu(users, user):
    while True:
        print("\n--- Radio Station Menu ---")
        print("1. View saved stations")
        print("2. Add a station")
        print("3. Remove a station")
        print("4. Filter stations by frequency range")
        print("0. Go back")

        choice = get_int("Choose: ", 0, 4)

        if choice == 0:
            break

        elif choice == 1:
            if len(user.stations) == 0:
                print("  No stations saved yet.")
            else:
                print("\n  Your stations (sorted by frequency):")
                sorted_stations = user.get_stations_sorted()
                for s in sorted_stations:
                    s.display()

        elif choice == 2:
            name = get_nonempty("  Station name: ")
            freq = get_float("  Frequency in MHz (87.0 - 108.0): ", 87.0, 108.0)
            station = RadioStation(name, freq)
            user.add_station(station)
            save_data(users)
            print(f"  Saved '{name}' at {freq:.1f} MHz.")

        elif choice == 3:
            if len(user.stations) == 0:
                print("  No stations saved yet.")
                continue
            name = get_nonempty("  Which station do you want to remove? ")
            if user.remove_station(name):
                save_data(users)
                print(f"  Removed '{name}'.")
            else:
                print("  Station not found.")

        elif choice == 4:
            if len(user.stations) == 0:
                print("  No stations saved yet.")
                continue
            low = get_float("  Minimum frequency (MHz): ", 87.0, 108.0)
            high = get_float("  Maximum frequency (MHz): ", 87.0, 108.0)
            if low > high:
                print("  Minimum can't be greater than maximum.")
                continue
            results = user.filter_stations(low, high)
            if len(results) == 0:
                print("  No stations found in that range.")
            else:
                print(f"\n  Stations between {low} and {high} MHz:")
                for s in results:
                    s.display()


# -------------------------------------------------------------------
# Recently played menu
# -------------------------------------------------------------------

def recent_menu(users, user):
    while True:
        print("\n--- Recently Played ---")
        print("1. View history (newest first)")
        print("2. View history (oldest first)")
        print("3. Play a song from a playlist")
        print("4. Clear history")
        print("0. Go back")

        choice = get_int("Choose: ", 0, 4)

        if choice == 0:
            break

        elif choice == 1 or choice == 2:
            if len(user.recently_played) == 0:
                print("  No playback history yet.")
            else:
                if choice == 1:
                    entries = user.get_recent_sorted(newest_first=True)
                    print("\n  Recently played (newest first):")
                else:
                    entries = user.get_recent_sorted(newest_first=False)
                    print("\n  Recently played (oldest first):")
                for entry in entries:
                    print(f"   [{entry['timestamp']}] {entry['title']} - {entry['artist']} ({entry['media_type']})")

        elif choice == 3:
            if len(user.playlists) == 0:
                print("  You have no playlists. Add some songs first.")
                continue
            print("  Your playlists:")
            for name in user.playlists:
                print(f"   - {name} ({len(user.playlists[name].songs)} song(s))")
            pl_name = get_nonempty("  Play from which playlist? ")
            if pl_name not in user.playlists:
                print("  Playlist not found.")
                continue
            playlist = user.playlists[pl_name]
            if len(playlist.songs) == 0:
                print("  That playlist is empty.")
                continue
            print(f"\n  Songs in '{pl_name}':")
            for i in range(len(playlist.songs)):
                print(f"   {i + 1}. {playlist.songs[i].title} - {playlist.songs[i].artist}")
            idx = get_int("  Pick a song number: ", 1, len(playlist.songs))
            song = playlist.songs[idx - 1]
            user.play_song(song)
            save_data(users)
            print(f"\n  Now playing: {song.title} by {song.artist}")

        elif choice == 4:
            user.recently_played = []
            save_data(users)
            print("  History cleared.")


# -------------------------------------------------------------------
# Admin panel - only visible to admin users
# -------------------------------------------------------------------

def admin_menu(users, admin):
    while True:
        print("\n--- Admin Panel ---")
        print("1. List all profiles")
        print("2. Delete a profile")
        print("3. System summary")
        print("0. Go back")

        choice = get_int("Choose: ", 0, 3)

        if choice == 0:
            break

        elif choice == 1:
            admin.list_all_users(users)

        elif choice == 2:
            target = get_nonempty("  Username to delete: ")
            if admin.delete_user(users, target):
                save_data(users)
                print(f"  Deleted profile '{target}'.")

        elif choice == 3:
            total_users = len(users)
            total_playlists = 0
            total_songs = 0
            total_stations = 0
            for u in users.values():
                total_playlists = total_playlists + len(u.playlists)
                total_stations = total_stations + len(u.stations)
                for pl in u.playlists.values():
                    total_songs = total_songs + len(pl.songs)
            print(f"\n  Profiles   : {total_users}")
            print(f"  Playlists  : {total_playlists}")
            print(f"  Songs      : {total_songs}")
            print(f"  Stations   : {total_stations}")


# -------------------------------------------------------------------
# Main menu shown after login
# -------------------------------------------------------------------

def user_menu(users, user):
    while True:
        print(f"\n===== Welcome, {user.username} ({user.role}) =====")
        print("1. Manage Playlists")
        print("2. Manage Radio Stations")
        print("3. Recently Played")
        if user.role == "Admin":
            print("4. Admin Panel")
            max_opt = 4
        else:
            max_opt = 3
        print("0. Logout")

        choice = get_int("Choose: ", 0, max_opt)

        if choice == 0:
            print(f"  See you later, {user.username}!")
            break
        elif choice == 1:
            playlist_menu(users, user)
        elif choice == 2:
            radio_menu(users, user)
        elif choice == 3:
            recent_menu(users, user)
        elif choice == 4 and user.role == "Admin":
            admin_menu(users, user)


# -------------------------------------------------------------------
# Login and register
# -------------------------------------------------------------------

def login(users):
    print("\n-- Login --")
    username = get_nonempty("  Username: ")
    password = get_nonempty("  Password: ")
    if username not in users:
        print("  No account found with that username.")
        return
    if users[username].password != password:
        print("  Wrong password. Please try again.")
        return
    print(f"\n  Welcome back, {username}!")
    user_menu(users, users[username])


def register(users):
    print("\n-- Create New Profile --")
    username = get_nonempty("  Choose a username: ")
    if username in users:
        print("  That username is taken. Try a different one.")
        return
    password = get_nonempty("  Choose a password: ")
    is_admin = input("  Register as admin? (y/N): ").strip().lower()
    if is_admin == "y":
        new_user = AdminUser(username, password)
    else:
        new_user = User(username, password)
    users[username] = new_user
    save_data(users)
    print(f"  Profile created! You can now log in as '{username}'.")


# -------------------------------------------------------------------
# Start the program
# -------------------------------------------------------------------

print("=" * 50)
print("      VEHICLE INFOTAINMENT SYSTEM")
print("=" * 50)

users = load_data()

while True:
    print("\n--- Main Menu ---")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = get_int("Choose: ", 1, 3)

    if choice == 1:
        login(users)
    elif choice == 2:
        register(users)
    elif choice == 3:
        save_data(users)
        print("\nGoodbye! Your data has been saved.")
        break
