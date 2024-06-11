import os
from dotenv import load_dotenv

import discord
from discord import option
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.slash_command(name="add")
@option("file", discord.Attachment, description="File to add")
async def add_file(ctx: discord.ApplicationContext, file: discord.Attachment): 
    await ctx.respond("Not implemented yet.")

@bot.slash_command(name="view")
@option("file", description="File to view. Image files are viewed with an embed.")
async def view_file(ctx: discord.ApplicationContext, file: str): 
    await ctx.respond("Not implemented yet.")

@bot.slash_command(name="remove")
@option("file", description="File to remove")
async def remove_file(ctx: discord.ApplicationContext, file: str): 
    await ctx.respond("Not implemented yet.")

@bot.slash_command(name="list")
async def list_files(ctx: discord.ApplicationContext):
    await ctx.respond("Not implemented yet.")

@bot.slash_command(name="hello")
async def hello_slash_command(ctx: discord.ApplicationContext):
    await ctx.respond("World!")

@bot.command(name="hello")
async def hello_command(ctx: discord.ext.commands.Context):
    await ctx.reply("World!")

bot.run(os.getenv("BOT_TOKEN"))