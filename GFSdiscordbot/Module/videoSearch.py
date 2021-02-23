import discord
from discord.ext import commands
import time
import config
import asyncio
import sys
import traceback
import util
import datetime
import requests

botAcc = None
lastCacheUpdate = 0
lastCacheUpdate2 = 0
allvideos = []

class videoSearch(commands.Cog):
	
	def is_allowedRole(ctx):
				
		groups = ctx.message.author.roles
		admin = False
		for group in groups:
			if group.permissions.administrator:
				admin = True
		if str(ctx.message.guild.owner_id) == str(ctx.message.author.id):
			admin = True
		if admin:
			return True
				
		return False
	
	@commands.command(pass_context=True,brief="", name='check')
	async def searchVideoCMD(self,ctx,*text):
		
		global lastCacheUpdate
		global lastCacheUpdate2
		global allvideos
		
		text = " ".join(text)
		
		if (lastCacheUpdate+1800) < int(time.time()):
			print("Cache too old, updating page 1")
			
			url = "https://www.googleapis.com/youtube/v3/search?key="+str(config.config['SETTINGS']['youtubeAPIkey'].strip())+"&channelId="+str(config.config['SETTINGS']['youtubeChannelID'].strip())+"&part=snippet,id&order=date&maxResults=50"

			r = requests.get(url)

			result = r.json()

			hasMorePages = False
			pageToken = ""
			hitLimit = False
			counter = 1
			
			try:
			
				for item in result["items"]:
					try:
						if not [item["snippet"]["title"],item["id"]["videoId"]] in allvideos:
							allvideos.append([item["snippet"]["title"],item["id"]["videoId"]])
					except:
						if not [item["snippet"]["title"],""] in allvideos:
							allvideos.append([item["snippet"]["title"],""])
			
			except:
				print("API LIMIT HIT! On page "+str(counter))
				pageToken = ""
				hasMorePages = False
				hitLimit = True
			
			if not hitLimit:
				try:
					pageToken = result["nextPageToken"]
					hasMorePages = True
				except:
					pageToken = ""
					hasMorePages = False

				if pageToken == "":
					hasMorePages = False
			
			if (lastCacheUpdate2+21600) < int(time.time()):
				print("Cache too old, updating page 2 and more")
				while hasMorePages:
					
					lastCacheUpdate2 = int(time.time())
					counter = counter +1
					#print(pageToken)
					url = "https://www.googleapis.com/youtube/v3/search?key="+str(config.config['SETTINGS']['youtubeAPIkey'].strip())+"&channelId="+str(config.config['SETTINGS']['youtubeChannelID'].strip())+"&part=snippet,id&order=date&maxResults=50&pageToken="+str(pageToken)

					r = requests.get(url)

					result = r.json()
					
					try:
						for item in result["items"]:
							try:
								if not [item["snippet"]["title"],item["id"]["videoId"]] in allvideos:
									allvideos.append([item["snippet"]["title"],item["id"]["videoId"]])
							except:
								if not [item["snippet"]["title"],""] in allvideos:
									allvideos.append([item["snippet"]["title"],""])
						
						try:
							pageToken = result["nextPageToken"]
							hasMorePages = True
						except:
							pageToken = ""
							hasMorePages = False

						if pageToken == "":
							hasMorePages = False
				
					except:
						print("API LIMIT HIT! On page"+str(counter))
						break
			
			lastCacheUpdate = int(time.time())
		
		for video in allvideos:
			if str(text).lower() in str(video[0]).lower():
				await ctx.send("Video found!\nhttps://www.youtube.com/v/"+str(video[1]))
				return False
		
		await ctx.send("Video not found!")
		
	def __init__(self,bot):
		
		self.bot = bot
		
		botAcc = bot
		
		print("GFS Video Search module started")
		
def setup(bot):
	bot.add_cog(videoSearch(bot))