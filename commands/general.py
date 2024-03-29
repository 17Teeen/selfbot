import discord_self_embed as dembed

from discord.ext import commands
from utils import config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="A list of all categories.", usage="")
    async def help(self, ctx):
        cfg = config.Config()
        embed = dembed.Embed("command categories", description=f"""
{self.bot.command_prefix}fun - Fun commands
{self.bot.command_prefix}info - Information commands
{self.bot.command_prefix}mod - Moderation commands
{self.bot.command_prefix}util - Utility commands""", colour=cfg.get('theme')['colour'])

        if cfg.get("message_settings")["embeds"]:
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ {cfg.get('theme')['emoji']} {cfg.get('theme')['title']} ]\n{embed.params['description']}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command()
    async def ping(self, ctx):
        cfg = config.Config()
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms", delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(General(bot))