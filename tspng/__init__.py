from importlib import metadata

__app_name__ = "tspng"
__version__ = metadata.version(__package__ or __name__)

PNG_FILE_EXT: str = ".png"
