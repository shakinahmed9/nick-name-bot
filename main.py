import discord
from discord.ext import tasks, commands
import os
import asyncio
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Environment variables (set these in Render)
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))  # Your server ID

# Create bot
intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    change_name.start()

# 💬 Command: !mrbean <new_name>
@bot.command()
@commands.has_permissions(manage_guild=True)  # only admins can rename
async def mrbean(ctx, *, new_name: str):
    try:
        guild = ctx.guild
        await guild.edit(name=new_name)
        await ctx.send(f"✅ Server name successfully changed to **{new_name}**")
        print(f"Server name changed to: {new_name}")
    except discord.Forbidden:
        await ctx.send("❌ I don’t have permission to change the server name.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")

# ⚠️ Error handler for missing permissions
@mrbean.error
async def mrbean_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 You don’t have permission to change the server name!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Usage: `!mrbean <new_name>`")
    else:
        await ctx.send("⚠️ Something went wrong!")

# Keep alive route for Render + UptimeRobot
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

import threading
threading.Thread(target=run_flask).start()
