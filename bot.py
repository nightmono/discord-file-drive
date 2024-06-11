import os
from dotenv import load_dotenv
import aiohttp
import aiofiles

import discord
from discord import option
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

async def download_file(ctx: discord.ApplicationContext, file: discord.Attachment) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                await ctx.respond(f"Failed to download file: {file.filename}")
                return None

async def save_file(ctx: discord.ApplicationContext, filename: str, file_bytes: bytes):
    async with aiofiles.open(f"drive/{filename}", "wb") as f:
        await f.write(file_bytes)
    
    await ctx.respond(f"Saved file: {filename}")

@bot.slash_command(name="add", description="Add a file to the drive")
@option("file", discord.Attachment, description="File to add to the drive",)
async def add_file(ctx: discord.ApplicationContext, file: discord.Attachment): 
    file_bytes = await download_file(ctx, file)
    if file_bytes is not None:
        await save_file(ctx, file.filename, file_bytes)

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