""" Global classes and methods """
from Util.AppSettings import AppSettings
from Util.Database import Database

class GlobalClass():

    """ Borg Singleton parent class
        Every instance is different, but all share the state
        stores AppSettings and Database
    """
    _state = None

    def __init__(self):
        if GlobalClass._state:
            self.__dict__ = GlobalClass._state
        else:
            # Initialize singleton ################################
            self.app_settings = AppSettings()
            self.database = Database(self.app_settings)
            #######################################################

            GlobalClass._state = self.__dict__

    def Set(self, location: str, option: str, max_albums: int) -> None:
        """ Apply parameters retrieved interactively
            Args:
                location:   Directory where Music is stored
                option:     AllMusic or Albums
                max_albums: Max albums to retrieve
            Raises:
            Returns:
                None
        """
        # strip spaces and validate
        location = location.strip(" ")
        option = option.strip(" ").lower()
        if option  not in ["allmusic", "albumsonly"]:
            option = ""

        # override config.ini values
        if location != "":
            self.app_settings.location = location
        if option != "":
            self.app_settings.option = option
        self.app_settings.max_albums = max_albums
