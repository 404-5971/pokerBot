import discord
from discord.ext import commands


def setup_poker_commands(bot: commands.Bot) -> None:
    """Setup all poker commands for the bot"""

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
