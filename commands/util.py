import os
import sys
import discord_self_embed as dembed

from discord.ext import commands
from utils import config
# from utils import embed

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="util", description="Utility commands.", aliases=["utilities", "utility"], usage="")
    async def util(self, ctx, selected_page: int = 1):
        cfg = config.Config()

        pages = []
        commands = self.bot.get_cog("Util").walk_commands()
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
            embed = dembed.Embed(f"util commands ({selected_page}/{len(pages)})", description=f"{pages[selected_page - 1]}", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ util commands ({selected_page}/{len(pages)}) ]\n\n{pages[selected_page - 1]}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.group(name="config", description="Configure flight.", usage="")
    async def config(self, ctx):
        cfg = config.Config()

        if ctx.invoked_subcommand is None:
            description = ""
            for key, value in self.cfg.config.items():
                if key == "token":
                    continue
                # check if the key is a dict
                if isinstance(value, dict):
                    sub_msg = f"{key} :\n"
                    for sub_key, sub_value in value.items():
                        if cfg.get("message_settings")["embeds"]:
                            sub_msg += f" {sub_key} : {sub_value}\n"
                        else:
                            sub_msg += f"\t{sub_key} : {sub_value}\n"
                    description += sub_msg
                else:
                    description += f"{key} : {value}\n"

            if cfg.get("message_settings")["embeds"]:
                embed = dembed.Embed("", description=description, colour=cfg.get('theme')['colour'])
                await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            else:
                await ctx.send(f"""```ini\n[ config ]\n\n{description}\n```""", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @config.command(name="set", description="Set a config value.", usage="[key] [value]")
    async def set(self, ctx, key, *, value):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        if key.lower() == "message_settings.auto_delete_delay":
            try:
                value = int(value)
            except ValueError:
                if self.cfg.get("message_settings")["embeds"]:
                    embed = dembed.Embed("", description=f"the value isn't an integer", colour=self.cfg.get('theme')['colour'])
                    await ctx.send(f"{self.cfg.get('theme')['emoji']} `{self.cfg.get('theme')['title']}`" + str(embed), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                else:
                    await ctx.send(f"```ini\n[ error ] the value isn't an integer\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if "." in key:
            key2 = key.split(".")
            if key2[0] not in self.cfg.config or key2[1] not in self.cfg.config[key2[0]]:
                if self.cfg.get("message_settings")["embeds"]:
                    embed = dembed.Embed("", description=f"invalid key", colour=self.cfg.get('theme')['colour'])
                    await ctx.send(f"{self.cfg.get('theme')['emoji']} `{self.cfg.get('theme')['title']}`" + str(embed), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                else:
                    await ctx.send(f"```ini\n[ error ] invalid key\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return
        
        else:
            if key not in self.cfg.config:
                if self.cfg.get("message_settings")["embeds"]:
                    embed = dembed.Embed("", description=f"invalid key", colour=self.cfg.get('theme')['colour'])
                    await ctx.send(f"{self.cfg.get('theme')['emoji']} `{self.cfg.get('theme')['title']}`" + str(embed), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                else:
                    await ctx.send(f"```ini\n[ error ] invalid key\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
                return

        if key == "prefix":
            self.bot.command_prefix = value

        if "." in key:
            key2 = key.split(".")
            self.cfg.config[key2[0]][key2[1]] = value

        else:
            self.cfg.config[key] = value

        self.cfg.save()
        if self.cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"key updated successfully\n{key} : {value}", colour=self.cfg.get('theme')['colour'])
            await ctx.send(f"{self.cfg.get('theme')['emoji']} `{self.cfg.get('theme')['title']}`" + str(embed), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

        else:
            await ctx.send(f"```ini\n[ config ]\n\nkey updated successfully\n{key} : {value}\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="restart", description="Restart the bot.", usage="", aliases=["reboot", "reload"])
    async def restart(self, ctx):
        cfg = config.Config()
        
        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description="restarting...", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ flight ] restarting...\n```", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])
        
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(name="settings", description="View Flight's settings.", usage="")
    async def settings(self, ctx):
        cfg = config.Config()
        command_amount = len(self.bot.commands)

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"""    prefix : {self.bot.command_prefix}
version : {config.VERSION}
command amount : {command_amount}""", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"""```ini
    [ settings ]

    prefix : {self.bot.command_prefix}
    version : {config.VERSION}
    command amount : {command_amount}
    ```""", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Util(bot))