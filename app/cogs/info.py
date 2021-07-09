from os import listdir

from app.embeds import Embed
from discord.ext import commands


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

        # Preloading file content
        self.files_info = {}
        folders = (".", "app", "app/cogs")
        for file, path in {
            _f: path for path in folders for _f in listdir(path) if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files_info[file] = f.read()

        self.files_info['Total'] = "\n".join(self.files_info.values())

    @commands.command(
        name="ping",
        description="Return Bot Latency",
        brief="Ping command"
    )
    async def ping(self, ctx) -> None:
        """Return Bot Latency."""
        await ctx.send(f"Pong ! `{self.client.latency * 1000:.3f}` ms")

    @commands.command(name="code")
    async def get_code_info(self, ctx):
        await ctx.send(
            embed=Embed(ctx)(
                title="Code Structure",
                description=f"> This is the whole code structure of {self.client.user.name}!"
            ).add_fields(
                self.files_info,
                map_title=lambda name: f"📝 {name}" if name != "Total" else "📊 Total",
                map_values=lambda file: "`%s` characters\n `%s` lines" % (f"{len(file):,}", len(file.splitlines())),
            )
        )


def setup(client):
    client.add_cog(InfoCog(client))
