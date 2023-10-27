import tempfile
import logging

from pathlib import Path


APP_NAME = "hrit"


class NonePath:
    # Monkey patching to create a "None" Path object

    @staticmethod
    def is_file():
        return False

    @staticmethod
    def is_dir():
        return False

    @staticmethod
    def exists():
        return False


def init_logger(
    name: str = "", logfile_in_temp_dir: bool = True, cleanup_logfile: bool = True
) -> logging.Logger:
    """
    initialize an logger (console output and file output)
    returns existing logger if already initialized before

    :param name: name of the logger. this name must be consistent throughout the app, defaults to ""
    :type name: str, optional
    :param logfile_in_temp_dir: creates the log file in the tmpdir = tempfile.TemporaryDirectory(), defaults to True
    :type logfile_in_temp_dir: bool, optional
    :param cleanup_logfile: tempfile.TemporaryDirectory(delete=True), defaults to True
    :type cleanup_logfile: bool, optional
    :return: _description_
    :rtype: logging.Logger
    """

    logger_name = name if name else __name__
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter("%(levelname)-8s: %(message)s")
    c_handler.setFormatter(c_format)
    c_handler.setLevel(logging.INFO)
    logger.addHandler(c_handler)
    logger_filename = (
        f"{logger_name}.log" if logger_name != "__main__" else f"{name}.log"
    )
    if logfile_in_temp_dir:
        tmpdir = tempfile.TemporaryDirectory()
        # tmpdir = tempfile.TemporaryDirectory(delete=cleanup_logfile) # only applicable for python3.12
        f_handler = logging.FileHandler(Path(tmpdir.name) / logger_filename)
    else:
        f_handler = logging.FileHandler(logger_filename)
    f_format = logging.Formatter(
        "[%(asctime)s]%(levelname)-8s: %(message)s", "%d-%b-%y %H:%M"
    )
    f_handler.setFormatter(f_format)
    f_handler.setLevel(logging.INFO)
    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO)
    logger.info(f"logger initialized - {logger_filename}")
    try:
        logfile_path = logger.handlers[-1].baseFilename  # type: ignore
        logger.info(f"{logfile_path=}")
    except Exception as e:
        logger.debug(f"failed to acquire logger path, {e=}")
    return logger


class PathFinder:
    def __init__(self, resources_foldername: str = "resources"):
        self.cwd = Path(__file__).parent.parent
        if resources_foldername:
            self.set_resources_dir(resources_foldername)
        else:
            self.resources_dir = NonePath()

    def __call__(self, name) -> Path:
        return self.get_resource(name)

    def get_pdf_files(self) -> list[Path]:
        files = [x for x in self.cwd.glob("*.[pP][dD][fF]")]
        return sorted(files)

    def set_resources_dir(self, name: str = "resources") -> Path:
        resources_dir = self.cwd / name
        if not resources_dir.is_dir():
            raise NotADirectoryError(f"target resources_dir={resources_dir}")
        self.resources_dir = resources_dir
        return resources_dir

    def get_resources_dir(self, name: str = "") -> Path:
        if name:
            self.set_resources_dir(name)
        else:
            self.set_resources_dir()
        return self.resources_dir  # type: ignore (handled by set_resources_dir)

    def get_resource(self, name: str) -> Path:
        fp = self.get_resources_dir() / name  # type: ignore
        if not fp.is_file():
            raise FileNotFoundError(f"{fp=}")
        return fp
