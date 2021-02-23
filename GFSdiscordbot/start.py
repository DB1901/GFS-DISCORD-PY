import discord
import os
import asyncio
import config
from discord.ext import commands
import sys

from os import listdir
from os.path import isfile, join
import traceback
import time
import datetime
import random

from pprint import pprint

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=str(config.prefix), case_insensitive=True,heartbeat_timeout=300,intents=intents)
bot.remove_command("help")

if getattr(sys, 'frozen', False):
	import plugins
	
cogs_dir = "plugins"

@bot.event
async def on_ready():
	print('\nLogged in as:')
	print(" Username",bot.user.name)
	print(" User ID",bot.user.id)
	print("To invite the bot use this link:\n https://discordapp.com/oauth2/authorize?&client_id="+str(bot.user.id)+"&scope=bot&permissions=0")
	print("Time now",str(datetime.datetime.now()))
	
def run_client(token):
	global bot
	
	while True:
		print("Starting at time",str(datetime.datetime.now()))
		loadPlugins()
		loop = asyncio.get_event_loop()
		try:
			#loop.run_until_complete(bot.connect())
			loop.run_until_complete(bot.start(token))
		#except Exception as e:
			#print("Error", e)
		except Exception as e:
			print("Error", e)
			loop.run_until_complete(bot.logout())
			
		for plugin in bot.extensions:
			plugin.unload()
			
		print("Restarting in 60 seconds")
		time.sleep(60)
		bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True,heartbeat_timeout=300,intents=intents)
		bot.remove_command("help")
		#if bot.is_closed():
			#loop.run_until_complete(bot.connect())

def loadPlugins():
	#bot.clear()
	
	activadedPlugins = []
	with open(cogs_dir+"/activated.conf") as f:
		activadedPlugins = f.readlines()
		
	activadedPlugins = [x.strip() for x in activadedPlugins]
	
	if not getattr(sys, 'frozen', False):
		for extension in [f for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
			try:
				if (str(extension)[-3:] == ".py") and (not str(extension) == "__init__.py"):
					if extension[:-3] in activadedPlugins:
						
						'''
						try:
							module = bot.extensions.get(cogs_dir + "." + extension[:-3])
							print("Unloaded plugin",str(plugin))
							module.unload()
						except:
							pass

						try:
							bot.unload_extension(cogs_dir + "." + extension[:-3])
							print("Unloaded plugin",str(plugin))
						except:
							pass
						'''
						bot.load_extension(cogs_dir + "." + extension[:-3])
					else:
						print(str(extension[:-3])," disabled")
			except Exception as e:
				print('Failed to load extension {extension}.')
				traceback.print_exc()
	else:
		for plugin in activadedPlugins:
			
			'''
			try:
				module = bot.extensions.get(cogs_dir+"."+str(plugin))
				print("Unloaded plugin",str(plugin))
				module.unload()
			except:
				pass
			
			try:
				bot.unload_extension(cogs_dir+"."+str(plugin))
				print("Unloaded plugin",str(plugin))
			except:
				pass
			'''
			
			bot.load_extension(cogs_dir+"."+str(plugin))
		
if __name__ == "__main__":
			
	run_client(config.discordtoken)