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
        embed = discord.Embed(title=f"Saved file: `{file.filename}`",
                              description="Reloading file list...")
        await files.save_file(file.filename, file_bytes)
        file_saved_reponse = await ctx.respond(embed=embed)
        files.load_files()
        embed = discord.Embed(title=f"Saved file: `{file.filename}`",
                              description="File list reloaded!")
        await file_saved_reponse.edit_original_response(embed=embed)
    else:
        embed = discord.Embed(title=f"Failed to download file: `{file.filename}`")
        await ctx.respond(embed=embed)

@bot.slash_command(name="view", description="View a file from the drive, image files are embeded")
@option("file", description="File to view.", autocomplete=files.get_files)
async def view_file(ctx: discord.ApplicationContext, file: str): 
    if file not in files.loaded_files:
        embed = discord.Embed(title=f"File `{file}` not found")
        await ctx.respond(embed=embed)
        return

    try:
        file_content = await files.read_file(file)

        embed_title = f"Viewing file: `{file}`"
        
        if len(file_content) > 4093:
            embed_description = f"```{file_content[:4043]}\n[Message over 4096 characters, thus truncated]```"
        else:
            embed_description = f"```{file_content}```"

        embed = discord.Embed(title=embed_title, description=embed_description)

        await ctx.respond(embed=embed)

    except UnicodeDecodeError:
        image_file = discord.File(f"drive/{file}", filename=file)
        
        embed_title = f"Viewing image: `{file}`"
        embed = discord.Embed(title=embed_title)
        embed.set_image(url=f"attachment://{file}")

        await ctx.respond(embed=embed, file=image_file)

@bot.slash_command(name="remove", description="Remove a file from the drive")
@option("file", description="File to remove", autocomplete=files.get_files)
async def remove_file(ctx: discord.ApplicationContext, file: str): 
    if file not in files.loaded_files:
        embed = discord.Embed(title=f"File `{file}` not found")
        await ctx.respond(embed=embed)
        return
    
    os.remove(f"drive/{file}")

    embed = discord.Embed(title=f"File `{file}` deleted")
    await ctx.respond(embed=embed)

@bot.slash_command(name="list", description="List all loaded drive files")
async def list_files(ctx: discord.ApplicationContext):
    embed_title = "Current files stored in drive"
    embed_description = "\n".join(files.loaded_files)
    embed = discord.Embed(title=embed_title, description=embed_description)

    await ctx.respond(embed=embed)

@bot.slash_command(name="hello", description="Displays ping too")
async def hello_slash_command(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="World!",
                          description=f"Ping: {bot.latency}")
    await ctx.respond(embed=embed)

@bot.command(name="hello")
async def hello_command(ctx: discord.ext.commands.Context):
    embed = discord.Embed(title="World!",
                          description=f"Ping: {bot.latency}")
    await ctx.respond(embed=embed)

bot.run(os.getenv("BOT_TOKEN"))