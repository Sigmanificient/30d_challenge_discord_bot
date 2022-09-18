from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Union

from discord import app_commands, Interaction
from discord.ext import commands

if TYPE_CHECKING:
    from sigmou.bot import Bot

from sigmou.utils.timer import time


@app_commands.guild_only()
class TimeCommandsGroup(app_commands.Group, name="time"):

    @app_commands.command(
        name="chronometer",
        description=(
            "A simple chronometer commands that start on first call, "
            "then give time elapsed. "
        )
    )
    async def chronometer_command(self, interaction: Interaction) -> str:
        """Clear the number of messages asked.
        If no number is given, clear all message in the channel."""

        t: Union[str, float] = time(interaction.user.id)

        await interaction.response.send_message(
            f"Timer ended: `{t:,.3f}s`"
            if isinstance(t, float)
            else "Timer started..."
        )

    @app_commands.command(
        name="lap",
        description=(
            "A command that give the current chronometer time of an user "
            "without stopping it. "
        )
    )
    async def lap_command(self, interaction: Interaction) -> str:
        """give the current time of a timer without destroying it."""
        t: Union[bool, float] = time(
            interaction.user.id,
            keep=True,
            create=False
        )

        await interaction.response.send_message(
            f"`{t:,.3f}s`" if t else "You dont have any timer"
        )

    @app_commands.command(
        name="timer",
        description="A command that wait the given time then ping the user."
    )
    async def timer_command(self, interaction):
        """A simple timer that ping you at end"""
        await interaction.response.send_message("started...")
        await asyncio.sleep(interaction.time)
        await interaction.response.send_message("> Ended!")


async def setup(client: commands.Bot):
    client.tree.add_command(TimeCommandsGroup())
