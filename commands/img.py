import discord_self_embed as dembed
import requests

from discord.ext import commands
from utils import config

class Img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="img", description="Image commands.", aliases=["image"], usage="")
    async def img(self, ctx, selected_page: int = 1):
        cfg = config.Config()

        pages = []
        commands = self.bot.get_cog("Img").walk_commands()
        commands_str = ""

        for cmd in commands:
            if len(commands_str) > 300:
                pages.append(commands_str)
                commands_str = ""
                
            if cmd.parent is not None:
                commands_str += f"{self.bot.command_prefix}{cmd.parent.name} {cmd.name} {cmd.usage} - {cmd.description}\n"
            else:
                commands_str += f"{self.bot.command_prefix}{cmd.name} {cmd.usage} - {cmd.description}\n"

        if len(commands_str) > 0:
            pages.append(commands_str)

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed(f"", description=f"{pages[selected_page - 1]}", colour=cfg.get('theme')['colour'])
            embed.set_author(f"img commands ({selected_page}/{len(pages)})")
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ img commands ({selected_page}/{len(pages)}) ]\n\n{pages[selected_page - 1]}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="gato", description="Get a random cat picture.", aliases=["cat", "catpic"], usage="")
    async def gato(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/cats")
        image = resp.json()["file"]

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("gato", colour=cfg.get('theme')['colour'])
            embed.set_image(url=image)
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="doggo", description="Get a random cat picture.", aliases=["dog", "dogpic"], usage="")
    async def doggo(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/dogs")
        image = resp.json()["file"]

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("doggo", colour=cfg.get('theme')['colour'])
            embed.set_image(url=image)
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="bird", description="Get a random cat picture.", aliases=["birb", "birdpic"], usage="")
    async def birb(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/birb")
        image = resp.json()["file"]

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("birb", colour=cfg.get('theme')['colour'])
            embed.set_image(url=image)
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Img(bot))