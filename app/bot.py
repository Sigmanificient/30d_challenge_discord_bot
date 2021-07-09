import os

from app.timer import time
from app.embeds import Embed
from app.logging import temp_print, warn

import dotenv
from discord import Activity, ActivityType, Colour, Intents
from discord.ext import commands, tasks


class Bot(commands.Bot):

    def __init__(self, prefix: str):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(
            case_insensitive=True,
            command_prefix=commands.when_mentioned_or(prefix),
            intents=Intents.default(),
            owner_id=812699388815605791
        )

        print(self)
        Embed.load(self)

        self.colour: Colour = Colour(0xCE1A28)
        self.base_prefix = prefix

        self.remove_command('help')  # removing default help command for overriding
        self.load_components()

    def __repr__(self) -> str:
        return '\n'.join(
            (
                r"██████╗  ██████╗     ██████╗  █████╗ ██╗   ██╗███████╗    ██████╗  ██████╗ ████████╗",
                r"╚════██╗██╔═████╗    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝",
                r" █████╔╝██║██╔██║    ██║  ██║███████║ ╚████╔╝ ███████╗    ██████╔╝██║   ██║   ██║",
                r" ╚═══██╗████╔╝██║    ██║  ██║██╔══██║  ╚██╔╝  ╚════██║    ██╔══██╗██║   ██║   ██║",
                r"██████╔╝╚██████╔╝    ██████╔╝██║  ██║   ██║   ███████║    ██████╔╝╚██████╔╝   ██║",
                r"╚═════╝  ╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝"
            )
        )

    def load_components(self):
        for file_name in os.listdir("app/cogs"):
            if not file_name.endswith("py"):
                continue

            self.load_component(file_name[:-3])

    def load_component(self, component_name: str) -> bool:
        try:
            self.load_extension(f"app.cogs.{component_name}")

        except commands.ExtensionFailed as error:
            warn(f"Could not load component '{component_name}' due to {error.__cause__}")
            return False

        else:
            temp_print(f"loaded {component_name}")
            return True

    def run(self):
        time("start")
        super().run(self.token)

    @property
    def token(self):
        if self.is_ready():
            return

        return dotenv.dotenv_values(".env").get('TOKEN')

    @tasks.loop(seconds=30)
    async def update_latency(self):
        await self.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{self.base_prefix}help | {self.latency * 1000:,.3f} ms"
            )
        )

    async def on_connect(self):
        self.update_latency.start()

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        ctx.time = time()

        await self.invoke(ctx)
