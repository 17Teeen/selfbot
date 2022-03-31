import os
import sys
import requests
import discord
import discord_self_embed as dembed

from discord.errors import LoginFailure
from discord.ext import commands

from utils import console
from utils import config
from utils import Notifier

cfg = config.Config()
cfg.check()

if requests.get("https://discord.com/api/users/@me/settings", headers={"Authorization": cfg.get("token")}).status_code == 200:
    status = requests.get("https://discord.com/api/users/@me/settings", headers={"Authorization": cfg.get("token")}).json()["status"]
else:
    status = "online"

flight = commands.Bot(command_prefix=cfg.get("prefix"), self_bot=True, help_command=None, status=discord.Status.try_value(status))

for command_file in os.listdir("commands"):
    if command_file.endswith(".py"):
        flight.load_extension(f"commands.{command_file[:-3]}")

@flight.event
async def on_connect():
    console.clear()
    console.resize(columns=90, rows=25)
    console.print_banner()
    console.print_info(f"Logged in as {flight.user.name}#{flight.user.discriminator}")
    console.print_info(f"You can now use commands with {cfg.get('prefix')}")
    print()

    Notifier.send("Flight", f"Logged in as {flight.user.name}#{flight.user.discriminator}")

@flight.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except Exception as e:
        console.print_error(str(e))

    console.print_cmd(ctx.command.name)

@flight.event
async def on_command_error(ctx, error):
    cfg = config.Config()

    try:
        await ctx.message.delete()
    except Exception as e:
        console.print_error(str(e))

    try:
        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed(title="", description=str(error), color=0xFF0000)
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ error ] {str(error).lower()}\n```", delete_after=cfg.get("message_settings")["auto_delete_delay"])
    except Exception as e:
        console.print_error(f"{e}")

    console.print_error(str(error))

try:
    flight.run(cfg.get("token"))
except LoginFailure:
    console.print_error("Invalid token, please set a new one below.")
    new_token = input("> ")
    cfg.set("token", new_token)
    cfg.save()

    os.execl(sys.executable, sys.executable, *sys.argv)