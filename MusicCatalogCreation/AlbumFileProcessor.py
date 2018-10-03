"""
    Manager providing methods for for files containing albums and tracks
"""
from os import walk

from GlobalClass import GlobalClass
from DB.Album import Album

class AlbumFileProcessor():
    """ Provides methods to manage files and directories containg album songs

    """

    def __init__(self):
        self.all_albums: dict = dict()
        self.directories: list = []
        self.file_names: list = []
        self.album_count: int = 0

    def FindAlbums(self, path: str):
        """ Finds albums  from base directory

        Args:
            path:  Path of the music directory

        Raises:

        Returns:
            Dictionary with Album definitions indexed by album title
        """

        global_class = GlobalClass()

        print("Find Albums iterating the music directory " + path)

        for(dirpath, self.directories, self.file_names) in walk(path):
            try:
                if not self.directories and self.HasMusicFiles():
                    # load album directory. It has only children songs
                    new_album = Album(dirpath)
                    new_album.LoadSongs(self.file_names)
                    self.all_albums[new_album.album_name] = new_album
                    self.album_count += 1

                    # Eexecution trace
                    if self.album_count % 10 == 0:
                        print("\r" + str(self.album_count) + " ", end="")

                if self.album_count >= global_class.app_settings.max_albums:
                    break
            except Exception as exc:
                print(exc.args)
                break

        return self.all_albums

    def HasMusicFiles(self) -> bool:
        """ Returns true if the directory contains music files

            Args:
                items:  List of files in the album directory

            Returns:
                True if found files .flac or .wav
        """

        for item in self.file_names:
            if item.lower().endswith(".flac") or item.lower().endswith(".wav"):
                return True
        return False
