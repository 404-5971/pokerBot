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


def create_tables() -> None:
    create_main_table()
    create_tables_table()


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


def create_tables_table() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tables (
                table_id INTEGER NOT NULL PRIMARY KEY,
                table_owner_id INTEGER NOT NULL,
                temp_money BOOLEAN NOT NULL DEFAULT FALSE,
                table_name TEXT NOT NULL,
                min_bet INTEGER NOT NULL DEFAULT 5,
                max_bet INTEGER NOT NULL DEFAULT 0
            )"""
        )


def add_table(
    table_id: int,
    table_owner_id: int,
    table_name: str,
    temp_money: bool,
    min_bet: int,
    max_bet: int,
) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tables (table_id, table_owner_id, table_name, temp_money, min_bet, max_bet) VALUES (?, ?, ?, ?, ?, ?)",
            (table_id, table_owner_id, table_name, temp_money, min_bet, max_bet),
        )
        conn.commit()


def delete_table(table_id: int) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("DELETE FROM tables WHERE table_id = ?", (table_id,))
        conn.commit()


def channel_is_table(channel_id: int) -> bool:
    """
    - Takes a discord channel id.
    - Check if a channel is a table.
    - Returns True if the channel is a table, False otherwise.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM tables WHERE table_id = ?", (channel_id,))
        return cursor.fetchone() is not None


def user_is_owner_of_table(user_id: int, table_id: int) -> bool:
    """
    - Takes a discord.User user id and a discord.Thread.id table id.
    - Check if a user is the owner of a table.
    - Returns True if the user is the owner of the table, False otherwise.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tables WHERE table_id = ? AND table_owner_id = ?",
            (table_id, user_id),
        )
        return cursor.fetchone() is not None


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


def add_user_to_table(user_id: int, table_id: int) -> None:
    """
    Add a user to a poker table.
    This function would typically manage table participants.
    For now, it's a placeholder that can be expanded later.
    """
    # TODO: Implement table participants management
    # This could involve creating a new table or updating existing table data
    pass
