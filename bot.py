import os
from dotenv import load_dotenv
import aiohttp
import aiofiles

import discord
from discord import option
from discord.ext import commands

import files

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.slash_command(name="add", description="Add a file to the drive")
@option("file", discord.Attachment, description="File to add to the drive",)
async def add_file(ctx: discord.ApplicationContext, file: discord.Attachment): 
    file_bytes = await files.download_file(file)
    if file_bytes is not None:
        await files.save_file(file.filename, file_bytes)
        file_saved_reponse = await ctx.respond(f"Saved file: {file.filename}\nReloading file list...")
        files.load_files()
        await file_saved_reponse.edit_original_response(content=f"Saved file: {file.filename}\nFile list reloaded!")
    else:
        await ctx.respond(f"Failed to download file: {file.filename}")

@bot.slash_command(name="view", description="View a file from the drive, image files are displayed using an embed.")
@option("file", description="File to view.", autocomplete=files.get_files)
async def view_file(ctx: discord.ApplicationContext, file: str): 
    file_content = await files.read_file(file)

    embed_title = f"Viewing file: {file}"
    
    if len(file_content) > 4093:
        embed_description = f"```{file_content[:4043]}\n[Message over 4096 characters, thus truncated]```"
    else:
        embed_description = f"```{file_content}```"
    
    await ctx.respond(embed=discord.Embed(title=embed_title, description=embed_description))

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