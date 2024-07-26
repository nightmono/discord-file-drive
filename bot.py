import os
from dotenv import load_dotenv

import discord
from discord import option
from discord.ext import commands

import files
import logs

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

        logs.debug(f"{ctx.author.name} ({ctx.author.id}) saved file {file.filename}")

        embed = discord.Embed(title=f"Saved file: `{file.filename}`",
                              description="Reloading file list...")
        file_saved_reponse = await ctx.respond(embed=embed)

        files.load_files()

        embed = discord.Embed(title=f"Saved file: `{file.filename}`",
                              description="File list reloaded!")
        await file_saved_reponse.edit_original_response(embed=embed)

    else:
        logs.debug(f"{ctx.author.name} ({ctx.author.id}) failed to save file {file.filename}")

        embed = discord.Embed(title=f"Failed to download file: `{file.filename}`")
        await ctx.respond(embed=embed)

@bot.slash_command(name="view", description="View a file from the drive, image files are embedded")
@option("file", description="File to view.", autocomplete=files.get_files)
async def view_file(ctx: discord.ApplicationContext, file: str):
    if file not in files.loaded_files:
        logs.debug(f"{ctx.author.name} ({ctx.author.id}) tried to view non-existant file {file}")

        embed = discord.Embed(title=f"File `{file}` not found")
        await ctx.respond(embed=embed)
        return

    try:
        file_content = await files.read_file(file)

        logs.debug(f"{ctx.author.name} ({ctx.author.id}) viewed text file {file}")

        embed_title = f"Viewing file: `{file}`"

        if len(file_content) > 4093:
            embed_description = f"```{file_content[:4043]}\n[Message over 4096 characters, thus truncated]```"
        else:
            embed_description = f"```{file_content}```"

        embed = discord.Embed(title=embed_title, description=embed_description)

        await ctx.respond(embed=embed)

    except UnicodeDecodeError:
        logs.debug(f"{ctx.author.name} ({ctx.author.id}) viewed image file {file}")

        image_file = discord.File(f"drive/{file}", filename=file)

        embed_title = f"Viewing image: `{file}`"
        embed = discord.Embed(title=embed_title)
        embed.set_image(url=f"attachment://{file}")

        await ctx.respond(embed=embed, file=image_file)

@bot.slash_command(name="remove", description="Remove a file from the drive")
@option("file", description="File to remove", autocomplete=files.get_files)
async def remove_file(ctx: discord.ApplicationContext, file: str):
    if file not in files.loaded_files:
        logs.debug(f"{ctx.author.name} ({ctx.author.id}) tried to remove non-existant file {file}")

        embed = discord.Embed(title=f"File `{file}` not found")
        await ctx.respond(embed=embed)
        return

    logs.debug(f"{ctx.author.name} ({ctx.author.id}) removed file {file}")

    await files.remove_file(file)
    files.load_files()

    embed = discord.Embed(title=f"File `{file}` deleted")
    await ctx.respond(embed=embed)

@bot.slash_command(name="list", description="List all loaded drive files")
async def list_files(ctx: discord.ApplicationContext):
    logs.debug(f"{ctx.author.name} ({ctx.author.id}) listed stored files")

    embed_title = "Current files stored in drive"
    embed_description = "\n".join(files.loaded_files)
    embed = discord.Embed(title=embed_title, description=embed_description)

    await ctx.respond(embed=embed)

@bot.slash_command(name="github", description="Return the GitHub repo for this bot")
async def github_slash_command(ctx: discord.ApplicationContext):
    await ctx.respond("https://github.com/nightmono/discord-file-drive")

@bot.command(name="github")
async def github_command(ctx: commands.Context):
    await ctx.reply("https://github.com/nightmono/discord-file-drive")

@bot.slash_command(name="hello", description="Displays ping too")
async def hello_slash_command(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="World!",
                          description=f"Ping: {bot.latency:.3f} ms")
    await ctx.respond(embed=embed)

@bot.command(name="hello")
async def hello_command(ctx: commands.Context):
    embed = discord.Embed(title="World!",
                          description=f"Ping: {bot.latency:.3f} ms")
    await ctx.reply(embed=embed)

bot.run(os.getenv("BOT_TOKEN"))
