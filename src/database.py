import sqlite3

from constants import DATABASE_PATH


class UserData:
    def __init__(
        self,
        user_id: int,
        money: int,
        lifttime_losses: int,
        lifttime_wins: int,
        lifttime_profit: int,
    ):
        self.user_id = user_id
        self.money = money
        self.lifttime_losses = lifttime_losses
        self.lifttime_wins = lifttime_wins
        self.lifttime_profit = lifttime_profit


def create_main_table() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS main (
            user_id INTEGER NOT NULL PRIMARY KEY,
            money INTEGER NOT NULL DEFAULT 1000,
            lifttime_losses INTEGER NOT NULL DEFAULT 0,
            lifttime_wins INTEGER NOT NULL DEFAULT 0,
            lifttime_profit INTEGER NOT NULL DEFAULT 0
        )"""
        )


def check_user_exists(user_id: int) -> bool:
    """
    - Check if a user exists in the main table.
    - Returns True if the user exists, False otherwise.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("SELECT * FROM main WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None


def add_user(user_id: int, money: int = 1000) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        if not check_user_exists(user_id):
            cursor: sqlite3.Cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO main (user_id, money, lifttime_losses, lifttime_wins, lifttime_profit) VALUES (?, ?, ?, ?, ?)",
                (user_id, money, 0, 0, 0),
            )
            conn.commit()


def get_user_data(user_id: int) -> UserData:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("SELECT * FROM main WHERE user_id = ?", (user_id,))
        data: tuple[int, int, int, int, int] = cursor.fetchone()
        return UserData(
            user_id=data[0],
            money=data[1],
            lifttime_losses=data[2],
            lifttime_wins=data[3],
            lifttime_profit=data[4],
        )
