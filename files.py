"""Helper script with file functions."""

import os
import aiohttp
import aiofiles
import logging

import discord

logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

def load_files():
    global loaded_files

    loaded_files = os.listdir("drive")
    logging.debug(f"Loaded files:\n{loaded_files}")

load_files()

async def download_file(file: discord.Attachment) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                return None

async def save_file(filename: str, file_bytes: bytes):
    async with aiofiles.open(f"drive/{filename}", "wb") as f:
        await f.write(file_bytes)

async def read_file(filename: str) -> str:
    try:
        async with aiofiles.open(f"drive/{filename}", "r") as f:
            return await f.read()
    except FileNotFoundError:
        return None

async def get_files(ctx: discord.AutocompleteContext) -> list:
    return loaded_files

async def remove_file(filename: str):
    os.remove(f"drive/{filename}")
    logging.debug(f"File {filename} removed")