import sqlite3
from typing import Optional

from constants import DATABASE_PATH


# Tables below
def create_tables() -> None:
    create_main_table()
    create_tables_table()


def create_main_table() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER NOT NULL PRIMARY KEY,
            money INTEGER NOT NULL DEFAULT 1000,
            lifttime_losses INTEGER NOT NULL DEFAULT 0,
            lifttime_wins INTEGER NOT NULL DEFAULT 0,
            lifttime_profit INTEGER NOT NULL DEFAULT 0,
            joined_table INTEGER NOT NULL DEFAULT 0,
            joined_table_name TEXT NOT NULL DEFAULT ""
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
                max_bet INTEGER NOT NULL DEFAULT 0,
                last_message_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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


def get_expired_tables(mintues: int = 5) -> list[int]:
    """
    Get list of table IDs that have expired (older than specified hours since last message)
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT table_id FROM tables 
            WHERE datetime(last_message_at) < datetime('now', '-{} minutes')
            """.format(
                mintues
            )
        )
        table_ids: list[int] = [row[0] for row in cursor.fetchall()]
        print(f"Expired tables: {table_ids}")
        return table_ids


def remove_all_users_from_table(table_id: int) -> None:
    """
    Remove all users from a specific table
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET joined_table = 0, joined_table_name = '' WHERE joined_table = ?",
            (table_id,),
        )
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


def get_table_name(user_id: int) -> str:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT joined_table_name FROM users WHERE user_id = ?", (user_id,)
        )
        return cursor.fetchone()[0]


def update_table_last_message_time(table_id: int) -> None:
    """Update the last message time for a table"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "UPDATE tables SET last_message_at = CURRENT_TIMESTAMP WHERE table_id = ?",
            (table_id,),
        )
        conn.commit()


def get_table_last_message_time(table_id: int) -> Optional[str]:
    """Get the last message time of a table"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT last_message_at FROM tables WHERE table_id = ?", (table_id,)
        )
        result: Optional[tuple[str, ...]] = cursor.fetchone()
        return result[0] if result else None


# User Stuff below
class UserData:
    def __init__(
        self,
        user_id: int,
        money: int,
        lifttime_losses: int,
        lifttime_wins: int,
        lifttime_profit: int,
        joined_table: int,
        joined_table_name: str,
    ):
        self.user_id = user_id
        self.money = money
        self.lifttime_losses = lifttime_losses
        self.lifttime_wins = lifttime_wins
        self.lifttime_profit = lifttime_profit
        self.joined_table = joined_table
        self.joined_table_name = joined_table_name


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

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None


def add_user(user_id: int, money: int = 1000) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        if not check_user_exists(user_id):
            cursor: sqlite3.Cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (user_id, money, lifttime_losses, lifttime_wins, lifttime_profit, joined_table) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, money, 0, 0, 0, 0),
            )
            conn.commit()


def get_user_data(user_id: int) -> Optional[UserData]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        data: Optional[tuple[int, int, int, int, int, int, str]] = cursor.fetchone()
        if data is None:
            return None

        return UserData(
            user_id=data[0],
            money=data[1],
            lifttime_losses=data[2],
            lifttime_wins=data[3],
            lifttime_profit=data[4],
            joined_table=data[5],
            joined_table_name=data[6],
        )


def user_is_in_table(user_id: int) -> bool:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ? AND joined_table != 0",
            (user_id,),
        )
        return cursor.fetchone() is not None


def add_user_to_table(user_id: int, table_id: int) -> None:
    """
    - Takes a discord.User user id and a discord.Thread.id table id.
    - Add a user to a table.
    - Returns True if the user is added to the table, False otherwise.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM tables WHERE table_id = ?", (table_id,))
        table_name_row: Optional[tuple[str, ...]] = cursor.fetchone()
        table_name: str = table_name_row[0] if table_name_row else ""
        cursor.execute(
            "UPDATE users SET joined_table = ?, joined_table_name = ? WHERE user_id = ?",
            (table_id, table_name, user_id),
        )
        conn.commit()


def remove_user_from_table(user_id: int) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET joined_table = 0, joined_table_name = '' WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()
