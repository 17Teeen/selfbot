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

    @commands.command(name="userinfo", description="Get information about a user.", aliases=["ui"], usage="<user>")
    async def userinfo(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        created_at = user.created_at.strftime("%d %B, %Y")

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed(f"", description=f"""
Username : {user.name}
ID : {user.id}
Created at : {created_at}
""", colour=cfg.get('theme')['colour'])
            embed.set_author(name=f"{user.name}#{user.discriminator}")
            try:
                embed.set_image(url=user.avatar_url)
            except:
                pass
                
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ {user.name}#{user.discriminator} ]\n\nUsername : {user.name}\nID : {user.id}\nCreated at : {created_at}```\n{user.avatar_url}", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="serverinfo", description="Get information about the server.", aliases=["si"], usage="")
    async def serverinfo(self, ctx):
        cfg = config.Config()

        embed = dembed.Embed(f"", description=f"""
Server name : {ctx.guild.name}
Server ID : {ctx.guild.id}
Owner : {ctx.guild.owner}
Members : {ctx.guild.member_count}
""", colour=cfg.get('theme')['colour'])
        embed.set_author(name=f"{ctx.guild.name}")
        embed.set_image(url=ctx.guild.icon_url)

        if cfg.get("message_settings")["embeds"]:
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ {ctx.guild.name} ]\n\nServer name : {ctx.guild.name}\nServer ID : {ctx.guild.id}\nOwner : {ctx.guild.owner}\nMembers : {ctx.guild.member_count}```\n{ctx.guild.icon_url}", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="avatar", description="Get the avatar of a user.", aliases=["av"], usage="<user>")
    async def avatar(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed(f"", colour=cfg.get('theme')['colour'])
            embed.set_author(name=f"{user.name}'s avatar")
            embed.set_image(url=user.avatar_url)
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"{user.avatar_url}", delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Info(bot))