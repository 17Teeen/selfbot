import discord_self_embed as dembed

from discord.ext import commands
from utils import config

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="mod", description="Moderation commands.", aliases=["moderation"], usage="")
    async def mod(self, ctx, selected_page: int = 1):
        cfg = config.Config()

        pages = []
        commands = self.bot.get_cog("Mod").walk_commands()
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
            embed = dembed.Embed(f"mod commands ({selected_page}/{len(pages)})", description=f"{pages[selected_page - 1]}", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ mod commands ({selected_page}/{len(pages)}) ]\n\n{pages[selected_page - 1]}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Mod(bot))