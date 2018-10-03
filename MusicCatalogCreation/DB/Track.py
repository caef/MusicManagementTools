"""
    Record and Track definitions
"""

from mutagen.flac import FLAC
from Exceptions import MException
from GlobalClass import GlobalClass

class Track():
    """
        Definition for a Record Song / Track
        Stores an InvalidRecords row if unable to decode it

        Attributes:
            album:          Album containing song/track
            track:          Song/Track name
            cover:          Cover file for album
            artist:         Track artist
            track_number:   Track Number
            composer:       Track Composer
            fullpath:       Full path for file contaning track

            ok_code         ok if successful, error if exception was thrown
    """
    def __init__(self, album, track: str) -> None:
        """
            Creates a song record data structure

            Args:
                album:  album name
                track:   song name

            Raises:
                internally Exception - when a record can not be interpreted by FLAC

            Returns:
                Complete Song / Track structure
        """
        self.fullpath: str = album.fullpath + "\\" + track
        self.album_name: str = album.album_name
        self.track_title: str = track
        self.cover: str = ""
        self.artist: str = ""
        self.track_number: str = ""
        self.composer: str = ""
        self.year: str = ""
        self.ok_code: str = "ok"

        if track.lower().endswith(".flac"):
            try:
                # get FLAC track attributes
                audio = FLAC(self.fullpath)
                self.track_title = self.GetTag(audio, "title")
                self.artist = self.GetTag(audio, "artist")
                self.track_number = self.GetTag(audio, "track_number")
                self.composer = self.GetTag(audio, "composer")
                self.year = self.GetTag(audio, "date")

                if album.artist == '':
                    album.album_name = self.GetTag(audio, "album")
                    album.artist = self.GetTag(audio, "album artist")
                    album.label = self.GetTag(audio, "label")
                    album.genre = self.GetTag(audio, "genre")
                    album.year = self.GetTag(audio, "date")

                    if album.artist.strip() == '':
                        album.artist = self.artist

            except MException as exc:
                print("Invalid FLAC file " + self.fullpath + " " + exc.args[0])
                self.ok_code = "error"
                GlobalClass().database.Add('''INSERT INTO InvalidTracks
                                           (album_Name,FileName)VALUES(?, ?)''',
                                           self.album_name, self.fullpath, commit=True,
                                           keep_connection=True)

    def GetTag(self, audio: FLAC, tagk: str) -> str:
        """
            Gets a tag in a flac file

            Args:
                audio:  FLAC object
                tagk:   tag name to evaluate

            Returns:
                Tag value if valid, or empty string
        """
        if tagk in audio:
            tag_value = audio[tagk][0]
            if tag_value:
                return tag_value
        return ""

    @staticmethod
    def IsMusicFile(filename: str) -> bool:
        """
            Returns true if a file is a playable track
            Ending in .flac, .wav

            Args:
                filename:   string storing the file name to evaluate

            Returns:
                True if is a valid music file
        """

        fname = filename.lower()
        return fname.endswith(".flac") or fname.endswith(".wav")

    ##########################################################################################

    @staticmethod
    def IsCover(filename: str) -> bool:
        """
            Returns true if a file is an image file
            Ending in .jpg

            Args:
                filename:   string storing the song cover

            Returns:
                True if is a valid image file
        """
        return filename.lower().endswith(".jpg")

    ##########################################################################################

    def Save(self) -> None:
        """
            Insert Track in database

        """
        GlobalClass().database.Add('''INSERT INTO Tracks
                                    (albumName,Title,trackNumber,Artist,Composer,Location,Year) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                   self.album_name, self.track_title, self.track_number,
                                   self.artist, self.composer, self.fullpath, self.year,
                                   commit=True, keep_connection=True)
