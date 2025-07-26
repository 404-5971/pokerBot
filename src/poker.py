import discord
from discord.ext import commands


def setup_poker_commands(bot: commands.Bot) -> None:
    """Setup all poker commands for the bot"""

    # Table management
    @bot.tree.command(name="create", description="Create a poker table")
    async def create(
        interaction: discord.Interaction,
        temp_money: bool = False,
        min_bet: int = 5,
        max_bet: int = 0,
        table_name: str = "",
    ) -> None:
        # In case of no max bet
        if max_bet == 0:
            max_bet *= 100

        # In case of no table name
        if table_name == "":
            table_name = f"{interaction.user.name}'s Table"

        # Check if the channel supports creating threads
        if not isinstance(
            interaction.channel, (discord.TextChannel, discord.ForumChannel)
        ):
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

    @bot.tree.command(name="join", description="Join's the current table")
    async def join(interaction: discord.Interaction) -> None:
        pass

    @bot.tree.command(name="leave", description="Leave's the current table")
    async def leave(interaction: discord.Interaction) -> None:
        pass

    @bot.tree.command(name="start", description="Start's the current table")
    async def start(interaction: discord.Interaction) -> None:
        pass





    # Actions
    @bot.tree.command(name="check", description="Check's the current table")
    async def check(interaction: discord.Interaction) -> None:
        pass

    @bot.tree.command(name="call", description="Call's the current table")
    async def call(interaction: discord.Interaction) -> None:
        pass

    @bot.tree.command(name="raise", description="Raise's the current table")
    async def raise_command(interaction: discord.Interaction, amount: int) -> None:
        pass

    @bot.tree.command(name="fold", description="Fold's the current table")
    async def fold(interaction: discord.Interaction) -> None:
        pass

    @bot.tree.command(name="all-in", description="All-in's the current table")
    async def all_in(interaction: discord.Interaction) -> None:
        pass
