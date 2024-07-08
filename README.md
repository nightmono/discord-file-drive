# 🗃️ Discord File Drive

Add, view, and manage files online using a Discord bot interface.

## Commands

`/add [file]` Adds a file

`/view [file]` View a file, images are embedded, file is from a dropdown

`/remove [file]` Remove a file, file is from a dropdown

`/list` List all files

`/hello` + `$hello` Returns bot latency

## Installation

### Requirements

Make sure you have the following requirements:

1. [Pycord](https://pycord.dev/)
2. [python-dotenv](https://github.com/theskumar/python-dotenv)
3. [aiohttp](https://pypi.org/project/aiohttp/)
4. [aiofiles](https://pypi.org/project/aiofiles/)

All requirements can be installed using `pip install py-cord python-dotenv aiohttp aiofiles`

### Setup

Create a `.env` file. Inside the file, create the key `BOT_TOKEN` with the value of your bot token.

Create a directory called `drive`. This is where all the drive files will be stored.

### Running

To run the bot, run `python3 bot.py`.

## TODO

- [ ] Emojis
- [ ] `/source/`. `/github`, `/code`, or similar command
- [ ] Logging to both stdout and file
