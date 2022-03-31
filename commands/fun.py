import discord
import requests
import asyncio
import random
import discord_self_embed as dembed

from discord.ext import commands
from utils import config

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="fun", description="Fun commands.", usage="")
    async def fun(self, ctx, selected_page: int = 1):
        cfg = config.Config()

        pages = []
        commands = self.bot.get_cog("Fun").walk_commands()
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
            embed.set_author(name=f"fun commands ({selected_page}/{len(pages)})")
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + embed.generate_url(hide_url=True, shorten_url=False), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"```ini\n[ fun commands ({selected_page}/{len(pages)}) ]\n\n{pages[selected_page - 1]}```", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="shrug", description="Shrug your arms.", usage="")
    async def shrug(self, ctx):
        await ctx.send("¯\_(ツ)_/¯")

    @commands.command(name="tableflip", description="Flip the table.", usage="")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command(name="unflip", description="Put the table back.", usage="")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.command(name="lmgtfy", description="Let me Google that for you.", usage="[search]", aliases=["letmegooglethatforyou"])
    async def lmgtfy(self, ctx, *, search):
        await ctx.send(f"https://lmgtfy.app/?q={search.replace(' ', '+')}")

    @commands.command(name="blank", description="Send a blank message", usage="", aliases=["empty"])
    async def blank(self, ctx):
        await ctx.send("** **")

    @commands.command(name="rickroll", description="Never gonna give you up.", usage="")
    async def rickroll(self, ctx):
        lyrics = requests.get("https://gist.githubusercontent.com/bentettmar/c8f9a62542174cdfb45499fdf8719723/raw/2f6a8245c64c0ea3249814ad8e016ceac45473e0/rickroll.txt").text    
        for line in lyrics.splitlines():
            await ctx.send(line)
            await asyncio.sleep(1)

    @commands.command(name="dadjoke", description="Get a dad joke.", usage="")
    async def dadjoke(self, ctx):
        resp = requests.get("https://api.benny.fun/v1/dadjoke").json()
        # await ctx.send(f"```ini\n[ dad joke ] {resp['text']}\n```")
        await ctx.send(resp.get("text"))

    @commands.command(name="roast", description="Roast someone.", usage="[user]")
    async def roast(self, ctx, *, user: discord.User):
        resp = requests.get(f"https://api.benny.fun/v1/roast").json()
        await ctx.send(f"{user.mention} " + resp["text"])

    @commands.command(name="fml", description="Get a fml article.", usage="")
    async def fml(self, ctx):
        resp = requests.get("https://api.benny.fun/v1/fml").json()
        # await ctx.send(f"```ini\n[ fml ] {resp['text']}\n```")
        await ctx.send(resp.get("text"))

    @commands.command(name="iq", description="Get the IQ of a user.", usage="[user]")
    async def iq(self, ctx, *, user: discord.User):
        cfg = config.Config()
        iq = random.randint(45, 135)
        smart_text = ""

        if iq > 90 and iq < 135:
            smart = "They're very smart!"
        if iq > 70 and iq < 90:
            smart = "They're just below average."
        if iq > 50 and iq < 70:
            smart = "They might have some issues."
        if iq > 40 and iq < 50:
            smart = "They're severely retarded."

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"{user.name}'s IQ is {iq}. {smart}", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"""```ini\n[ iq ] {user.name}'s IQ is {iq}. {smart}\n```""")

    @commands.command(name="howgay", description="Get the gayness of a user.", usage="[user]", aliases=["gay", "gayrating"])
    async def howgay(self, ctx, *, user: discord.User):
        cfg = config.Config()
        gay_percentage = random.randint(0, 100)

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"{user.name}#{user.discriminator} is {gay_percentage}% gay.", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"""```ini\n[ how gay? ] {user.name}#{user.discriminator} is {gay_percentage}% gay.\n```""")

    @commands.command(name="pp", description="Get the size of a user's dick.", usage="[user]", aliases=["dick", "dicksize", "penis"])
    async def pp(self, ctx, *, user: discord.User):
        cfg = config.Config()
        penis = "8" + ("=" * random.randint(0, 12)) + "D"
        inches = str(len(penis)) + "\""

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"{user.name}#{user.discriminator} has a {inches} dick.\n{penis}", colour=cfg.get("theme")["colour"])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"""```ini\n[ pp ] {user.name}#{user.discriminator} has a {inches} dick.\n{penis}\n```""", delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="blocksend", description="Send a message to a blocked user.", usage="[user] [message]")
    async def blocksend(self, ctx, user: discord.User, *, message: str):
        cfg = config.Config()
        
        await user.unblock()
        await user.send(message)
        await user.block()

        if cfg.get("message_settings")["embeds"]:
            embed = dembed.Embed("", description=f"Sent {message} to {user.name}#{user.discriminator} ({user.id}).", colour=cfg.get('theme')['colour'])
            await ctx.send(f"{cfg.get('theme')['emoji']} `{cfg.get('theme')['title']}`" + str(embed), delete_after=cfg.get("message_settings")["auto_delete_delay"])
        else:
            await ctx.send(f"""```ini\n[ block send ] Sent {message} to {user.name}#{user.discriminator} ({user.id}).\n```""", delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="cembed", description="Create a custom embed.", usage="")
    async def customembed(self, ctx, *, args):
        args = args.lower().split("\n")
        embed_args = {}

        for arg in args:
            arg = arg.split(":")

            if arg[0] == "title":
                embed_args["title"] = arg[1]
            if arg[0] == "description":
                embed_args["description"] = arg[1]
            if arg[0] == "colour" or arg[0] == "color":
                embed_args["colour"] = arg[1]
            if arg[0] == "author":
                embed_args["author"] = arg[1]
            if arg[0] == "author_url":
                embed_args["author_url"] = arg[1]
            if arg[0] == "provider":
                embed_args["provider"] = arg[1]
            if arg[0] == "provider_url":
                embed_args["provider_url"] = arg[1]
            if arg[0] == "url":
                embed_args["url"] = arg[1]
            if arg[0] == "image":
                embed_args["image"] = arg[1]

        custom_embed = dembed.Embed(embed_args.get("title", ""), description=embed_args.get("description", ""), colour=embed_args.get("colour", ""), url=embed_args.get("url", ""))
        
        if "author" in embed_args:
            custom_embed.set_author(embed_args["author"], url=embed_args.get("author_url", ""))
        if "provider" in embed_args:
            custom_embed.set_provider(embed_args["provider"], url=embed_args.get("provider_url", ""))
        if "image" in embed_args:
            custom_embed.set_image(embed_args["image"])

        await ctx.send("`custom embed`" + str(custom_embed), delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Fun(bot))