from typing import Any

import discord
from discord.ext import commands, tasks

from database import (delete_table, get_expired_tables,
                      remove_all_users_from_table)


def setup_table_timer(bot: commands.Bot) -> None:
    @tasks.loop(minutes=5)  # Check every 5 minutes
    async def check_expired_tables(bot: commands.Bot):
        """Check for expired tables and delete them"""
        try:
            expired_table_ids: list[int] = get_expired_tables(mintues=5)

            for table_id in expired_table_ids:
                await delete_expired_table(bot, table_id)

        except Exception as e:
            print(f"Error checking expired tables: {e}")

    check_expired_tables.start(bot)


async def delete_expired_table(bot: commands.Bot, table_id: int) -> None:
    """Delete an expired table from Discord and database"""
    try:
        # Get the channel/thread
        channel: Any = bot.get_channel(table_id)

        if channel is None or not isinstance(channel, discord.Thread):
            raise ValueError(f"Channel {table_id} is not a thread")
        else:
            discord_thread: discord.Thread = channel

        # Send a message before deleting
        try:
            await discord_thread.send(
                "⏰ **Table expired!** This table has been automatically deleted after 5 minutes of inactivity."
            )
        except discord.Forbidden:
            pass  # Can't send message, but continue with deletion

        # Delete the thread
        try:
            await discord_thread.delete()
        except discord.Forbidden:
            print(f"Don't have permission to delete thread {table_id}")
        except discord.NotFound:
            print(f"Thread {table_id} not found (already deleted)")
        except Exception as e:
            print(f"Error deleting thread {table_id}: {e}")

        # Clean up database
        remove_all_users_from_table(table_id)
        delete_table(table_id)

        print(f"Deleted expired table {table_id}")

    except Exception as e:
        print(f"Error deleting expired table {table_id}: {e}")
