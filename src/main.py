import os
import time
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import *
from helpers import setup_helper_commands
from poker import setup_poker_commands

load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError(
        "TOKEN is not set. Set it in the .env file as TOKEN=your_token_here"
    )


bot: commands.Bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

start_time: float = time.time()


@bot.event
async def on_member_join(member: discord.Member) -> None:
    add_user(member.id)


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected to Discord!")

    create_main_table()

    # Setup helper commands
    setup_helper_commands(bot)
    setup_poker_commands(bot)

    await bot.tree.sync()

    end_time: float = time.time()

    elapsed_time: float = end_time - start_time

    print("Time to start up", round(elapsed_time, 2), "seconds")


if __name__ == "__main__":
    bot.run(TOKEN)
