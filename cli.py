from hrit import dashboard
from hrit.utils import init_logger

APP_NAME = "hrit"
lg = init_logger(APP_NAME)


def main():
    app = dashboard.app()


if __name__ == "__main__":
    main()
