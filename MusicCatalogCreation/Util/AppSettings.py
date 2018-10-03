""" Application Settings """
import configparser
import sys
from argparse import ArgumentParser

CONFIGURATION_FILE = "config.ini"
class Configuration:
    """ Generic definition for Application settings

    Attributes:
        config:     Configuration Parser
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIGURATION_FILE)

    def ConfigSectionMap(self, section) -> dict:
        """ Maps a single configuration parameter section

        Args:
            section:    Section name from config.ini

        Returns:
            Dictionary with the configuration parameters
        """

        dict1: dict = {}                        # configuration parameters returned

        for option in self.config.options(section):
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except Exception:
                print("Exception on %s!" % option)
                dict1[option] = None
        return dict1

class AppSettings(Configuration):
    """ Application Settings for MusicList

    Attributes:
        location:      MusicDirectory parameter from config.ini or command line
        option:        Option parameter from config.ini or command line
        generate:      Generate parameter from config.ini or command
        generated_file: File created if generate is xls or csv
        db_connection:  Database connection if generte is dbsql or dbmysql
        max_albums:    maximum albums to process
    """

    def __init__(self):
        """ Initializer """
        Configuration.__init__(self)

        # parameters passed in the command line
        argv: list = sys.argv[1:]

        # parameters in configuration file
        self.location: str = Configuration().ConfigSectionMap("MusicStore")["musicdirectory"]
        self.option: str = Configuration().ConfigSectionMap("MusicStore")["option"]
        self.generate: str = Configuration().ConfigSectionMap("MusicStore")["generate"].lower()
        self.max_albums: int = 99999

        # parse command line parameters overriding ini file
        parser = ArgumentParser(argv)
        parser.add_argument('-o', '--Option', choices=['Albums', 'FullAlbums', 'Tracks'],
                            default=self.option, help='Generated Excel options')
        parser.add_argument('-m', '--MusicDirectory', default=self.location,
                            help='Directory where the music files are stored')
        parser.add_argument('-f', '--File', default='D:\\music\\Music Catalog',
                            help='File to generate')
        parser.add_argument('-d', '--Database', default='music', help='Database')
        parser.add_argument('-g', '--Generate', choices=['xlsx', 'csv', 'dbsql', 'dbsql'],
                            default=self.generate,
                            help='dexcel(xlsx), csv(csv), SQL Server(dbsql), MySql(dbmysql)')
        parser.add_argument('-x', '--MaxAlbums', default='100000', help='Max Albums to Process')

        # parameters parsed
        args = parser.parse_args(argv)

        # override
        self.option = args.Option
        self.location = args.MusicDirectory
        self.generated_file = args.File
        self.generate = args.Generate.lower()
        self.max_albums = int(args.MaxAlbums)

        # get connections
        conns: dict = {"dbsql": "connectionsqlserver", "dbmysql": "connectionmysql"}
        if conns[self.generate]:
            self.db_connection = Configuration().ConfigSectionMap("Databases")[conns[self.generate]]
