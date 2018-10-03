""" generate Music Catalog
"""
import csv
import xlsxwriter
from GlobalClass import GlobalClass
from Util.Database import Database
from Util.AppSettings import AppSettings
from Exceptions import MException

class CatalogManager():
    """ Generates music catalog

        Attributes:
            catType:    Type of Catalog to generate:
                                csv     Excel csv
                                xlsx    Excel
                                dbsql   SQL Server database
    """
    globalClass = GlobalClass()
    database: Database = globalClass.database
    config: AppSettings = globalClass.app_settings

    def __init__(self):
        """ Initializer

            Args:
                catType:    Type of Catalog to generate:
                                csv     Excel csv
                                xlsx    Excel
                                dbsql   SQL Server database
                                dbmysql MySql database
        """
        self.cat_type: str = self.config.generate

    @staticmethod
    def CreateCSV(albums: dict):
        """
        Creates a csv file with all records

            Args:
                albums:  Dictionary containing all albums

            Returns:
                None

            Raises:
                 None
        """

        with open(GlobalClass().app_settings.generated_file + ".csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel', quoting=csv.QUOTE_ALL)

            # Create titles
            if GlobalClass().app_settings.option == 'FullAlbums':
                csv_writer.writerow(["Album", "Genre", "", "Artist", "", "Location", "Cover"])
                csv_writer.writerow(["", "Track", "Title", "", "Composer"])
            elif GlobalClass().app_settings.option == 'Albums':
                csv_writer.writerow(["Album", "Artist", "Genre", "Location"])
            elif GlobalClass().app_settings.option == 'Tracks':
                csv_writer.writerow(["Album", "Track", "Title", "Artist", "Genre", "Location"])

            # process all files in music directory sorted
            for album in sorted(albums):
                # trace
                print(album.Album)

                if GlobalClass().app_settings.option == 'FullAlbums':
                    csv_writer.writerow([album.Album, album.Genre, "", album.Artist, "",
                                         album.FullPath, album.Cover])
                elif GlobalClass().app_settings.option == 'Albums':
                    csv_writer.writerow([album.Album, album.Artist, album.Genre,
                                         album.FullPath])

                for song in album.Songs:
                    print(song.Track)
                    if GlobalClass().app_settings.option == 'FullAlbums':
                        csv_writer.writerow(["", song.track_number, song.Title,
                                             song.Artist, song.Composer, song.FullPath])
                    elif GlobalClass().app_settings.option == 'Tracks':
                        csv_writer.writerow([song.Album, song.track_number, song.Title,
                                             song.Artist, song.Composer, song.FullPath])

    @staticmethod
    def CreateXlsx(albums: dict):
        """
        Creates an excel file with all records

            Args:
                albums:  Dictionary containing all albums

            Returns:
                None

            Raises:
                 None
        """

        workbook = xlsxwriter.Workbook(GlobalClass().app_settings.generated_file + ".xlsx")
        worksheet = workbook.add_worksheet()

        format_album = workbook.add_format({'font_color': 'blue'})
        format_album_title = workbook.add_format({'bold': True, 'font_color': 'blue'})
        format_track = workbook.add_format({'align':'center'})

        irow = 1    # row in spreadsheet
        if GlobalClass().app_settings.option == 'FullAlbums':
            worksheet.write_row(0, 0, ["Album", "", "Genre", "Artist", "", "Location", "Cover"],
                                format_album_title)
            worksheet.write_row(1, 0, ["", "Track", "Title", "", "Composer"], format_album_title)
            irow += 1
        elif GlobalClass().app_settings.option == 'Albums':
            worksheet.write_row(irow, 0, ["Album", "Artist", "Genre", "Location"],
                                format_album_title)
        elif GlobalClass().app_settings.option == 'Tracks':
            worksheet.write_row(irow, 0, ["Album", "Track", "Title", "Artist",
                                          "Composer", "Location"],
                                format_album_title)

        for an_album in sorted(albums):
            album = albums[an_album]
            print(album.album_name)

            if GlobalClass().app_settings.option == 'FullAlbums':
                irow += 1
                worksheet.write_row(irow, 0, [album.album_name, "", album.genre, album.artist, "",
                                              album.fullpath, album.cover], format_album)
            elif GlobalClass().app_settings.option == 'Albums':
                irow += 1
                worksheet.write_row(irow, 0, [album.album_name, album.artist,
                                              album.genre, album.fullPath])
            if GlobalClass().app_settings.option in ['FullAlbums', "Tracks"]:
                for song in album.tracks:
                    if GlobalClass().app_settings.option == 'FullAlbums':
                        irow += 1
                        worksheet.write_row(irow, 0, ["", song.track_number], format_track)
                        worksheet.write_row(irow, 2, [song.track_title, song.artist,
                                                      song.composer, song.fullpath])
                    elif GlobalClass().app_settings.option == 'Tracks':
                        irow += 1
                        worksheet.write_row(irow, 0, [song.album, str(song.track_number)],
                                            format_track)
                        worksheet.write_row(irow, 2, [song.track_title, song.artist,
                                                      song.composer, song.fullpath])

        workbook.close()

##########################################################################################

    @staticmethod
    def CreateDatabase(albums: dict):
        """ Populates database tables with the music catalog

                Args:
                    albums:      Dictionary containing all records indexed by record title

                Raises:

                Returns:
                    Nothing
        """
        global_class = GlobalClass()
        option: str = global_class.app_settings.option.lower()

        print("\nInitialize Database")
        global_class.database.Execute("TRUNCATE TABLE Albums", keep_connection=True)
        global_class.database.Execute("TRUNCATE TABLE Tracks", keep_connection=True)
        global_class.database.Execute("TRUNCATE TABLE InvalidTracks", keep_connection=True)

        print("Store Album Records")
        # totals
        album_count: int = 0
        track_count: int = 0

        # one letter trace
        strace = ''
        for an_album_key in sorted(albums.keys()):
            album = albums[an_album_key]

            # trace
            if  an_album_key != '' and an_album_key[0] != strace:
                strace = an_album_key[0]
                print("\r" + strace, end="")

            #save albums and tracks
            try:
                if album.album_name != "":
                    if option in ['allmusic', 'albumsonly']:
                        album_count += 1
                        album.Save()

                    if option in ['allmusic', 'tracks']:
                        ntrack: int = 0  # track count in an album
                        for song in album.tracks:
                            track_count += 1
                            ntrack += 1
                            song.track_number = ntrack
                            song.Save()
                else:
                    global_class.database.Add('''INSERT INTO InvalidTracks
                                              (albumName,FileName)VALUES(?, ?)''',
                                              album.album_name, album.fullpath, commit=True)
            except MException as dbe:
                print(dbe.args[0])
        global_class.database.DBDisconnect()

        print("\r_________________________________________________________________\n")
        print("Total Albums: " + str(album_count))
        print("Total Tracks: " + str(track_count))

##########################################################################################

    def Generate(self, albums: dict):
        """ Generate catalog in requested format

        Args:
            all_albums:  Dictionary with all albums indexed by album Title

        Returns:
            Number of Albums
        """

        self.CreateDatabase(albums)
        return len(albums)
