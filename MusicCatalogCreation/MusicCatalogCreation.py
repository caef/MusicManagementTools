"""
    Creates a record catalog based on the content of the Music directory

    Arguments:


    Configuration:

"""

import sys
import colorama
from CatalogManager import CatalogManager
from GlobalClass import GlobalClass
from AlbumFileProcessor import AlbumFileProcessor

##########################################################################################
def GetParameters() -> None:
    """ Gets execution paramters and overrides config

        Args:
        Raises:
        Returns:
            Nothing
    """
    global_class = GlobalClass()

    colorama.init() # required for text formatting

    print(colorama.Style.BRIGHT + "START MUSIC LIST GENERATION\n" + colorama.Style.DIM)
    print("Python:  ", sys.version[0:sys.version.index("(")], "\n",)

    # Ask for parameters
    print("Enter execution parameters")
    print("Music Location (" + colorama.Fore.LIGHTBLUE_EX + global_class.app_settings.location +
          colorama.Fore.RESET +  "): " + colorama.Fore.CYAN, end="")
    location: str = input().strip(' ')
    print(colorama.Fore.RESET, end="")

    option: str = ""
    while True:
        print("Options (" + colorama.Fore.LIGHTBLUE_EX + "AllMusic" + colorama.Fore.RESET +
              " | AlbumsOnly): " + colorama.Fore.CYAN, end="")
        option = input().lower().strip(" ")
        print(colorama.Fore.RESET, end="")

        # validate
        if option in ["", "allmusic", "albumsonly"]:
            break

    print("Max Albums (" + colorama.Fore.LIGHTBLUE_EX + str(global_class.app_settings.max_albums) +
          colorama.Fore.RESET + "): " + colorama.Fore.CYAN, end="")
    max_albums_wanted: str = input()
    print(colorama.Fore.RESET)

    # Default max albums
    max_albums: int = 99999

    # Apply entered value
    if (max_albums_wanted != "") and max_albums_wanted.isnumeric:
        max_albums = int(max_albums_wanted)

    global_class.Set(location, option, max_albums)

##########################################################################################
if __name__ == "__main__":
    GetParameters()

    print(colorama.Style.DIM +
          "_________________________________________________________________\n")
    print(colorama.Style.BRIGHT + "Music Location:", GlobalClass().app_settings.location)
    print("Options:       ", GlobalClass().app_settings.option + colorama.Style.DIM +  "\n")
    print("_________________________________________________________________\n")

    # Create dictionary with albums
    all_albums: dict = AlbumFileProcessor().FindAlbums(GlobalClass().app_settings.location)

    # Generate database
    count_albums: int = CatalogManager().Generate(all_albums)

    print("\n" + colorama.Style.BRIGHT + colorama.Fore.RED + "COMPLETE " + str(count_albums) +
          " albums loaded\n" + colorama.Style.DIM + colorama.Fore.RESET)

### modified
#local change 3:01
