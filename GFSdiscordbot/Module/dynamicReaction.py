import discord
from discord.ext import commands
import time
import config
import asyncio
import sys
import datetime
import os
import traceback
from operator import itemgetter
import util

started = True

roleCommands = {}

class dynamicReaction(commands.Cog):
	
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
	
	@commands.command(pass_context=True, brief="Syntax: !addreactionroles <messageIDNumber> <emoji>|<roleID> <emoji>|<roleID> <emoji>|<roleID>...", name='reactrole')
	@commands.check(is_allowedRole)
	async def addreactionrolesCommand(self,ctx,messageID,*rolesReactions):
		
		global roleCommands
		
		#print(rolesReactions)
		
		if ctx.message.guild:
			
			roleCommands[str(messageID)] = {}
			roleCommands[str(messageID)]["selections"] = {}
			roleCommands[str(messageID)]["messageID"] = str(messageID)
			roleCommands[str(messageID)]["guildID"] = str(ctx.message.guild.id)
			
			foundMessage = None
			for channel in ctx.message.guild.channels:
				
				try:
					if not foundMessage is None:
						break
					
					async for message in channel.history():
						if not foundMessage is None:
							break
						if str(message.id) == str(messageID):
							
							foundMessage = message
							break
				except:
					pass
						
			if foundMessage is None:
				await ctx.send("Unable to find the specified message")
				return False
			
			await message.clear_reactions()
			
			for selection in rolesReactions:
			
				emoji,roleID = selection.split("|")
			
				role = discord.utils.get(ctx.message.guild.roles, id=int(roleID))
				
				if not role is None:
					
					#print(emoji)
					emoteToAdd = emoji
					if ":" in emoji:
						emoteToAdd = ctx.bot.get_emoji(int(str(emoji).split(":")[2].replace(">","")))
						#print(emoteToAdd)
					try:
						await message.add_reaction(emoteToAdd)
					except:
						await ctx.send("Error adding emoji")
						return False
					
					try:
						roleCommands[str(messageID)]["selections"][emoteToAdd.name] = roleID
					except:
						roleCommands[str(messageID)]["selections"][emoteToAdd] = roleID
					
					await ctx.send("Role command for the role "+str(role)+" added")
				else:
					await ctx.send("Invalid role")
					return False
			
			util.save_data(roleCommands, "roleReactions")
			
			try:
				embed = discord.Embed(title="Command Used",description=ctx.message.author.mention+"\nUsed the "+str(ctx.command.name)+" command in "+str(ctx.message.channel.name)+"\n\nMessage content:\n"+str(ctx.message.content),colour=discord.Colour(0x5cddff))
				embed.set_author(name=str(ctx.message.author),icon_url=ctx.message.author.avatar_url)
				embed.timestamp = datetime.datetime.utcnow()
				embed.set_footer(text="User ID: "+str(ctx.message.author.id), icon_url=discord.Embed.Empty)
				embed.set_thumbnail(url=ctx.message.author.avatar_url)
				await self.bot.get_channel(int(config.logChannel)).send(embed=embed)
			except:
				traceback.print_exc()
			
	@commands.command(pass_context=True, brief="Syntax: !addreactionrolesUnique <messageIDNumber> <emoji>|<roleID> <emoji>|<roleID> <emoji>|<roleID>...", name='reactroleUnique')
	@commands.check(is_allowedRole)
	async def addreactionrolesCommandUnique(self,ctx,messageID,*rolesReactions):
		
		global roleCommandsUnique
		
		#print(rolesReactions)
		
		if ctx.message.guild:
			
			roleCommandsUnique[str(messageID)] = {}
			roleCommandsUnique[str(messageID)]["selections"] = {}
			roleCommandsUnique[str(messageID)]["messageID"] = str(messageID)
			roleCommandsUnique[str(messageID)]["guildID"] = str(ctx.message.guild.id)
			
			foundMessage = None
			for channel in ctx.message.guild.channels:
				
				try:
					if not foundMessage is None:
						break
					
					async for message in channel.history():
						if not foundMessage is None:
							break
						if str(message.id) == str(messageID):
							
							foundMessage = message
							break
				except:
					pass
						
			if foundMessage is None:
				await ctx.send("Unable to find the specified message")
				return False
			
			await message.clear_reactions()
			
			for selection in rolesReactions:
			
				emoji,roleID = selection.split("|")
			
				role = discord.utils.get(ctx.message.guild.roles, id=int(roleID))
				
				if not role is None:
					
					#print(emoji)
					emoteToAdd = emoji
					if ":" in emoji:
						emoteToAdd = ctx.bot.get_emoji(int(str(emoji).split(":")[2].replace(">","")))
						#print(emoteToAdd)
					try:
						await message.add_reaction(emoteToAdd)
					except:
						await ctx.send("Error adding emoji")
						return False
					
					try:
						roleCommandsUnique[str(messageID)]["selections"][emoteToAdd.name] = roleID
					except:
						roleCommandsUnique[str(messageID)]["selections"][emoteToAdd] = roleID
					
					await ctx.send("Role command for the role "+str(role)+" added")
				else:
					await ctx.send("Invalid role")
					return False
			
			util.save_data(roleCommandsUnique, "roleReactionsUnique")
			
			try:
				embed = discord.Embed(title="Command Used",description=ctx.message.author.mention+"\nUsed the "+str(ctx.command.name)+" command in "+str(ctx.message.channel.name)+"\n\nMessage content:\n"+str(ctx.message.content),colour=discord.Colour(0x5cddff))
				embed.set_author(name=str(ctx.message.author),icon_url=ctx.message.author.avatar_url)
				embed.timestamp = datetime.datetime.utcnow()
				embed.set_footer(text="User ID: "+str(ctx.message.author.id), icon_url=discord.Embed.Empty)
				embed.set_thumbnail(url=ctx.message.author.avatar_url)
				await self.bot.get_channel(int(config.logChannel)).send(embed=embed)
			except:
				traceback.print_exc()
			
	@commands.command(pass_context=True,brief="Remove all previusly added reaction messages with addreactionroles", name='clearreactroles')
	@commands.check(is_allowedRole)
	async def clearAllreactrolesCommand(self,ctx):
		global roleCommands
		roleCommands = {}
		util.save_data(roleCommands, "roleReactions")
		await ctx.send("Settings cleared")
		
		try:
			embed = discord.Embed(title="Command Used",description=ctx.message.author.mention+"\nUsed the "+str(ctx.command.name)+" command in "+str(ctx.message.channel.name)+"\n\nMessage content:\n"+str(ctx.message.content),colour=discord.Colour(0x5cddff))
			embed.set_author(name=str(ctx.message.author),icon_url=ctx.message.author.avatar_url)
			embed.timestamp = datetime.datetime.utcnow()
			embed.set_footer(text="User ID: "+str(ctx.message.author.id), icon_url=discord.Embed.Empty)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			await self.bot.get_channel(int(config.logChannel)).send(embed=embed)
		except:
			traceback.print_exc()
		
	@commands.command(pass_context=True,brief="Remove all previusly added reaction messages with addreactionrolesUnique", name='clearreactrolesUnique')
	@commands.check(is_allowedRole)
	async def clearAllreactrolesUniqueCommand(self,ctx):
		global roleCommandsUnique
		roleCommandsUnique = {}
		util.save_data(roleCommandsUnique, "roleReactionsUnique")
		await ctx.send("Settings cleared")
		
		try:
			embed = discord.Embed(title="Command Used",description=ctx.message.author.mention+"\nUsed the "+str(ctx.command.name)+" command in "+str(ctx.message.channel.name)+"\n\nMessage content:\n"+str(ctx.message.content),colour=discord.Colour(0x5cddff))
			embed.set_author(name=str(ctx.message.author),icon_url=ctx.message.author.avatar_url)
			embed.timestamp = datetime.datetime.utcnow()
			embed.set_footer(text="User ID: "+str(ctx.message.author.id), icon_url=discord.Embed.Empty)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			await self.bot.get_channel(int(config.logChannel)).send(embed=embed)
		except:
			traceback.print_exc()
		
	@commands.Cog.listener()
	async def on_raw_reaction_add(self,event):
		
		global roleCommands
		global roleCommandsUnique
		
		guild = discord.utils.get(self.bot.guilds, id=int(event.guild_id))
		if guild is None:
			print("Error guild is none")
			return False
		
		user = discord.utils.get(guild.members, id=int(event.user_id))
		if not user.bot:
		
			#print(event)
			
			#print(roleCommands)
			
			if not roleCommands == {}:
				for rolecmdMessageID in roleCommands:
					#print(rolecmdMessageID)
					#print(event)
					if (str(event.message_id) == str(roleCommands[rolecmdMessageID]["messageID"])):
						#print("valid role msg id")
						#guild = discord.utils.get(self.bot.guilds, id=int(roleCommands["guildID"]))
						#print(event.emoji)
						emojiSent = str(event.emoji.name)
						#if ":" in str(event.emoji):
							#emojiSent = str(event.emoji)
							#print(emojiSent)
						#print(emojiSent)
										
						if (str(event.message_id) == str(roleCommands[rolecmdMessageID]["messageID"])):				
							if emojiSent in roleCommands[rolecmdMessageID]["selections"]:
								#print("valid role emoji")
								#print(event)
								if not user is None:
									if not user.bot:
										role = discord.utils.get(guild.roles, id=int(roleCommands[rolecmdMessageID]["selections"][str(emojiSent)]))
										try:
											await user.add_roles(role)
										except:
											print("Error adding dynamic role")
			
			if not roleCommandsUnique == {}:
				for rolecmdMessageID in roleCommandsUnique:
					#print(rolecmdMessageID)
					#print(event)
					if (str(event.message_id) == str(roleCommandsUnique[rolecmdMessageID]["messageID"])):
						#print("valid role msg id")
						#guild = discord.utils.get(self.bot.guilds, id=int(roleCommands["guildID"]))
						#print(event.emoji)
						emojiSent = str(event.emoji.name)
						#if ":" in str(event.emoji):
							#emojiSent = str(event.emoji)
							#print(emojiSent)
						#print(emojiSent)
										
						if (str(event.message_id) == str(roleCommandsUnique[rolecmdMessageID]["messageID"])):				
							if emojiSent in roleCommandsUnique[rolecmdMessageID]["selections"]:
								#print("valid role emoji")
								#print(event)
								if not user is None:
									if not user.bot:
										roleToAdd = discord.utils.get(guild.roles, id=int(roleCommandsUnique[rolecmdMessageID]["selections"][str(emojiSent)]))
										for role in user.roles:
											for key in roleCommandsUnique[rolecmdMessageID]["selections"]:
												if str(roleCommandsUnique[rolecmdMessageID]["selections"][key]) == str(role.id):
													if not role == roleToAdd:
														try:
															await user.remove_roles(role)
														except:
															print("Error removing unique dynamic role")
											
										try:
											await user.add_roles(roleToAdd)
										except:
											print("Error adding unique dynamic role")
			
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self,event):
		
		global roleCommands
		
		if not roleCommands == {}:
			for rolecmdMessageID in roleCommands:
				if str(event.message_id) == str(roleCommands[rolecmdMessageID]["messageID"]):
					guild = discord.utils.get(self.bot.guilds, id=int(roleCommands[rolecmdMessageID]["guildID"]))
					#print(event.emoji)*
					emojiSent = str(event.emoji.name)
					#if ":" in str(event.emoji):
						#emojiSent = str(event.emoji)
						
					if emojiSent in roleCommands[rolecmdMessageID]["selections"]:
						user = discord.utils.get(guild.members, id=int(event.user_id))
						if not user is None:
							if not user.bot:
								role = discord.utils.get(guild.roles, id=int(roleCommands[rolecmdMessageID]["selections"][str(emojiSent)]))
								try:
									await user.remove_roles(role)
								except:
									print("Error removing dynamic role")
						
	def __init__(self,bot):
		
		self.bot = bot
		
		global roleCommands
		global roleCommandsUnique
		
		try:
			roleCommandsUnique = util.load_data('roleReactionsUnique')
		except:
			roleCommandsUnique = {}
		
		try:
			roleCommands = util.load_data('roleReactions')
		except:
			roleCommands = {}
		
		#print("roleCommandsUnique",str(roleCommandsUnique))
		
		print("Dynamic Reaction Module started")
		
def setup(bot):
	bot.add_cog(dynamicReaction(bot))