import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
import subprocess
from mcrcon import MCRcon

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
rcon_pass_a = os.getenv('RCON_PASS_A')
rcon_pass_v = os.getenv('RCON_PASS_V')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.group(name="start",invoke_without_command=True)
async def start(ctx):
    pass
@start.command(name="airsoft")
async def start_airsoft(ctx):
    now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
    username = ctx.author.display_name
    user_id = ctx.author.id

    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","start","minecraft"],capture_output=True,text=True)
    if result.returncode == 0:
        await ctx.send(f"{ctx.author.mention}, Airsoft Server Starting.")
        log_entry = f"[{now}] Airsoft Server Launched by {username}\n"
    else:
        await ctx.send(f"{ctx.author.mention} - Airsoft Server Failed to Start")
        log_entry = f"[{now}] Attempted Airsoft server launch failed by {username}\n"
        print(result.stderr)
    with open('/home/server/mc_bot/log.txt', 'a') as log:
        log.write(log_entry)

@start.command(name="vanilla")
async def start_vanilla(ctx):
    now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
    username = ctx.author.display_name
    user_id = ctx.author.id

    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","start","uni-minecraft"],capture_output=True,text=True)
    if result.returncode == 0:
        await ctx.send(f"{ctx.author.mention}, Vanilla Server Starting.")
        log_entry = f"[{now}] Vanilla Server Launched by {username}\n"
    else:
        await ctx.send(f"{ctx.author.mention} - Vanilla Server Failed to Start")
        log_entry = f"[{now}] Attempted Vanilla server launch failed by {username}\n"
        print(result.stderr)
    with open('/home/server/mc_bot/log.txt', 'a') as log:
        log.write(log_entry)

@bot.group(name="stop",invoke_without_command=True)
async def stop(ctx):
    pass
@stop.command(name="airsoft")
async def stop_airsoft(ctx):
    now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
    username = ctx.author.display_name
    user_id = ctx.author.id

    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","stop","minecraft"],capture_output=True,text=True)
    if result.returncode == 0:
        await ctx.send(f"{ctx.author.mention},  Airsoft Server Stopping.")
        log_entry = f"[{now}] Airsoft Server Stopped by {username}\n"
    else:
        await ctx.send(f"{ctx.author.mention} - Airsoft Server Failed to Stop")
        log_entry = f"[{now}] Attempted Airsoft server stop failed by {username}\n"
        print(result.stderr)
    with open('/home/server/mc_bot/log.txt', 'a') as log:
        log.write(log_entry)

@stop.command(name="vanilla")
async def stop_vanilla(ctx):
    now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
    username = ctx.author.display_name
    user_id = ctx.author.id

    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","stop","uni-minecraft"],capture_output=True,text=True)
    if result.returncode == 0:
        await ctx.send(f"{ctx.author.mention},  Vanilla Server Stopping.")
        log_entry = f"[{now}] Vanilla Server Stopped by {username}\n"
    else:
        await ctx.send(f"{ctx.author.mention} - Vanilla Server Failed to Stop")
        log_entry = f"[{now}] Vanilla Attempted server stop failed by {username}\n"
        print(result.stderr)
    with open('/home/server/mc_bot/log.txt', 'a') as log:
        log.write(log_entry)

@bot.group(name="status",invoke_without_command=True)
async def status(ctx):
    pass
@status.command(name="airsoft")
async def status_airsoft(ctx):
    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","is-active","minecraft"],capture_output=True,text=True)
    if result.stdout.strip() != "active":
        await ctx.send(f"{ctx.author.mention}, Airsoft Server is currently Inactive")
        return

    try:
        with MCRcon("127.0.0.1", rcon_pass_a, port=25575) as mcr:
            response = mcr.command("list")
                    
        if ":" in response:
            player_list = response.split(":", 1)[1].strip()
        else:
            player_list = ""

        if player_list:
            await ctx.send(f"{ctx.author.mention}, Airsoft Server is **Active**\n" f"**Players:** {player_list}")
        else:
            await ctx.send(f"{ctx.author.mention}, Airsoft Server is **Active**\n" f"**No players online**")
    except Exception as e:
        await ctx.send(f"{ctx.author.mention}, Airsoft Server is **ONLINE**, "f"Player list unavailable")
        now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
        log_entry = f"[{now}] RCON error: {e}\n"
        with open('/home/server/mc_bot/log.txt', 'a') as log:
            log.write(log_entry)

@status.command(name="vanilla")
async def status_vanilla(ctx):

    result = subprocess.run(["sudo","-n","/usr/bin/systemctl","is-active","uni-minecraft"],capture_output=True,text=True)
    if result.stdout.strip() != "active":
        await ctx.send(f"{ctx.author.mention}, Vanilla Server is currently Inactive")
        return

    try:
        with MCRcon("127.0.0.1", rcon_pass_v, port=25576) as mcr:
            response = mcr.command("list")
                
            if ":" in response:
                player_list = response.split(":", 1)[1].strip()
            else:
                player_list = ""

            if player_list:
                await ctx.send(f"{ctx.author.mention}, Vanilla Server is **Active**\n" f"**Players:** {player_list}")
            else:
                await ctx.send(f"{ctx.author.mention}, Vanilla Server is **Active**\n" f"**No players online**")
    except Exception as e:
        await ctx.send(f"{ctx.author.mention}, Vanilla Server is **ONLINE**, "f"Player list unavailable")
        now = datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
        log_entry = f"[{now}] RCON error: {e}\n"
        with open('/home/server/mc_bot/log.txt', 'a') as log:
            log.write(log_entry)
        

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

