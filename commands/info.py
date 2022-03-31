import discord_self_embed as dembed

from discord.ext import commands
from utils import config

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="info", description="Information commands.", aliases=["information"], usage="")
    async def info(self, ctx, selected_page: int = 1):
        cfg = config.Config()

        pages = []
        commands = self.bot.get_cog("Info").walk_commands()
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
            embed.set_author(name=f"info commands ({selected_page}/{len(pages)})")
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ info commands ({selected_page}/{len(pages)}) ]\n\n{pages[selected_page - 1]}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Info(bot))