from window_countdown import CountdownWindow
from db_connection import DBConnector
from app_constants import AppConstants


def main():
    db = DBConnector(AppConstants.DB_FILE_NAME)
    countdown_window = CountdownWindow(db)
    countdown_window.display()


if __name__ == "__main__":
    main()
