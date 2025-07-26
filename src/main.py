import os
import random
import time
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError(
        "TOKEN is not set. Set it in the .env file as TOKEN=your_token_here"
    )


bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

start_time: float = time.time()


@bot.command()
async def ip(ctx):
    random_int_1 = random.randint(1, 255)
    random_int_2 = random.randint(1, 255)
    await ctx.send(f"Your IP is 192.168.{random_int_1}.{random_int_2}")


@bot.tree.command(name="ping", description="Ping the bot")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="create-table", description="Create a poker table")
async def create_table(
    interaction: discord.Interaction,
    temp_money: bool = False,
    min_bet: int = 5,
    max_bet: int = 0,
    table_name: str = "",
) -> None:
    # In case of no max bet
    if max_bet == 0:
        max_bet = min_bet * 100

    # In case of no table name
    if table_name == "":
        table_name = f"{interaction.user.name}'s Table"

    # Check if the channel supports creating threads
    if not isinstance(interaction.channel, (discord.TextChannel, discord.ForumChannel)):
        await interaction.response.send_message(
            "This command can only be used in text channels or forum channels!"
        )
        return

    try:
        # Send initial response to acknowledge the command
        await interaction.response.send_message(
            f"Creating table `{table_name}`, Temp money: {temp_money}, Min bet: {min_bet}, Max bet: {max_bet}"
        )

        # Create thread with the table name
        if isinstance(interaction.channel, discord.TextChannel):
            thread = await interaction.channel.create_thread(
                name=table_name, auto_archive_duration=60
            )
        else:
            await interaction.followup.send("❌ Unsupported channel type!")
            return

        # Create a message in the thread
        await thread.send(
            f"🎰 **Table {table_name}** created!\n"
            f"💸 Temp money: {temp_money}\n"
            f"💰 Min bet: {min_bet}\n"
            f"💎 Max bet: {max_bet}\n"
            f"👤 Created by: {interaction.user.mention}"
        )

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to create threads in this channel!"
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to create table: {str(e)}")


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected to Discord!")

    await bot.tree.sync()

    end_time: float = time.time()

    elapsed_time: float = end_time - start_time

    print("Time to start up", round(elapsed_time, 2), "seconds")


if __name__ == "__main__":
    bot.run(TOKEN)
