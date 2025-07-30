import random

import discord
from discord.ext import commands

from database import *


def setup_helper_commands(bot: commands.Bot) -> None:
    """Setup all helper commands for the bot"""

    @bot.command()
    async def ip(ctx: commands.Context) -> None:
        random_int_1: int = random.randint(1, 255)
        random_int_2: int = random.randint(1, 255)
        await ctx.send(f"Your IP is 192.168.{random_int_1}.{random_int_2}")

    @bot.tree.command(name="ping", description="Ping the bot")
    async def ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Pong!")

    @bot.tree.command(name="init", description="Initialize your account")
    async def init(interaction: discord.Interaction) -> None:
        if not check_user_exists(interaction.user.id):
            add_user(interaction.user.id)
            await interaction.response.send_message(
                "Your account has been initialized!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Your account has already been initialized!", ephemeral=True
            )

    @bot.tree.command(name="stats", description="View your stats")
    async def stats(interaction: discord.Interaction) -> None:
        if not check_user_exists(interaction.user.id):
            await interaction.response.send_message(
                "You don't have an account (somehow), use `/init` to initialize your account",
                ephemeral=True,
            )
            return

        user_data: Optional[UserData] = get_user_data(interaction.user.id)
        if user_data is None:
            await interaction.response.send_message(
                "You don't exist in the database! Use `/init` to initialize your account.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Your stats:\n"
            f"Money: {user_data.money}\n"
            f"Lifttime losses: {user_data.lifttime_losses}\n"
            f"Lifttime wins: {user_data.lifttime_wins}\n"
            f"Lifttime profit: {user_data.lifttime_profit}\n"
            f"Lifttime profit percentage: {user_data.lifttime_profit / user_data.money * 100}%",
            ephemeral=True,
        )
