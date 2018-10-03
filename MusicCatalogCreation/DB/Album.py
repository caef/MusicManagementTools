"""
    Album Object definition
"""
from GlobalClass import GlobalClass
from DB.Track import Track
from Exceptions import MException

class Album():
    """ Definition for an Album
            Attributes:
                fullpath:       Full path for album
                album_name:     Name/Title of album
                cover:          Path of cover file
                tracks:         List of tracks for the album
    """
    def __init__(self, fullpath: str) -> None:
        self.fullpath: str = fullpath

        # parse name
        items: list = fullpath.split("\\")
        self.album_name: str = items[- 1]

        self.cover: str = ""
        self.tracks: list = []
        self.artist: str = ""
        self.label: str = ""
        self.genre: str = ""
        self.year: str = ""

    def LoadSongs(self, file_names: list) -> None:
        """ Populate tracks for an album

            Args:
                file_names:  Collection of file_names representing tracks
            Raises:
                Exception for unknown conditions
            Returns:
                Nothing
        """
        for file_name in file_names:
            try:
                if Track.IsMusicFile(file_name):
                    trk = Track(self, file_name)
                    self.tracks.append(trk)
                elif Track.IsCover(file_name):
                    self.cover = file_name
            except Exception as exc:
                print("Unable to analyze track file: " + repr(exc))
                raise MException("Unable to analyze track file " + repr(exc))

    def Print(self) -> None:
        """ printAlbum Info
        """
        print(self.album_name + "  ||  " + self.fullpath + "  ||  " + self.cover)
        for trk in self.tracks:
            print("    " + trk.trackName)

    def Save(self) -> None:
        """ Insert an Album in database
        """
        GlobalClass().database.Add(
            "INSERT INTO Albums(albumName,Artist,Genre,Location, year)VALUES(?, ?, ?, ?, ?)",
            self.album_name, self.artist, self.genre, self.fullpath, self.year,
            commit=True, keep_connection=True)
