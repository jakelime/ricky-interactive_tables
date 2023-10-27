from collections import UserDict
import pandas as pd

from hrit.utils import init_logger, PathFinder

APP_NAME = "hrit"
lg = init_logger(APP_NAME)


class Database(UserDict):
    def __init__(self, inputfolder: str = "input_files"):
        super().__init__()
        self.inputfolder = inputfolder
        self.load_data(inputfolder)

    def load_data(self, inputfolder: str):
        pf = PathFinder(resources_foldername=inputfolder)
        for fp in pf.get_csv_files():
            df = pd.read_csv(fp)
            self[fp.stem] = df
            lg.info(f"loaded to db['{fp.stem}']")


def main():
    db = Database()
    print(db["1_tball"])


if __name__ == "__main__":
    main()
