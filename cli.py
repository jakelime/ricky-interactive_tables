from hrit.utils import init_logger
from hrit.dashboard import create_dashboard_report

APP_NAME = "hrit"
lg = init_logger(APP_NAME)


def main():
    create_dashboard_report()


if __name__ == "__main__":
    main()
