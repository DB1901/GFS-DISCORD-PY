import discord
from discord.ext import commands
import time
import config
import asyncio
import json
import random
import traceback
import util

questions = str(config.config['SETTINGS']['questionsReport'].strip()).split("|")
#questions = ["What discord user would you like to report?","What is it you would like to report?","Anything you would like to add?"]
reportChannelID = str(config.config['SETTINGS']['reportLogChannel'].strip())

currentintrosessionReport = {}
botAcc = None
allowedReporters = []

async def introStartCommand(id,guildID):
	global currentintrosessionReport
	
	currentintrosessionReport[str(id)] = {}
	currentintrosessionReport[str(id)]['confirmed'] = "False"
	currentintrosessionReport[str(id)]['guildID'] = str(guildID)
	currentintrosessionReport[str(id)]['createdTime'] = str(time.time())
	#currentintrosessionReport[str(id)]['createdTime'] = "9999999999999"
	currentintrosessionReport[str(id)]['answers'] = []
	currentintrosessionReport[str(id)]['lastAnswerTime'] = str(int(time.time()))
	
	guild = discord.utils.get(botAcc.guilds, id=int(guildID))
	member = discord.utils.get(guild.members, id=int(id))
	
	if member is None:
		print("Member none")
		return False
	
	try:
		await member.send("Please answer each question.")
	except:
		return False
		
	messageToSendRAW = questions[0]
	messageToSend = messageToSendRAW.split("{")[0]
	messageSent = await member.send(messageToSend)
	util.save_data(currentintrosessionReport, "currentintrosessionReport")

async def confirm(authorID,serverID):
		
	global currentintrosessionReport
	global reportChannelID
	
	print("Doing confirm command")
		
	if len(currentintrosessionReport[str(authorID)]['answers']) >= len(questions):
		if currentintrosessionReport[str(authorID)]['confirmed'] == "False":
			#print(orderID)
			
			guild = discord.utils.get(botAcc.guilds, id=int(serverID))
			member = discord.utils.get(guild.members, id=int(authorID))
			
			if not member is None:
				
				guild = discord.utils.get(botAcc.guilds, id=int(currentintrosessionReport[str(authorID)]['guildID']))
				newIntroChannel = discord.utils.get(guild.channels, id=int(reportChannelID))
				
				introID = len(currentintrosessionReport) +1
				currentintrosessionReport[str(authorID)]['introID'] = str(introID)
				currentintrosessionReport[str(authorID)]['confirmedTime'] = str(time.time())
				currentintrosessionReport[str(authorID)]['confirmed'] = 'True'
				currentintrosessionReport[str(authorID)]['lastAnswerTime'] = str(int(time.time()))
				
				embed = discord.Embed(title=str(member)+" Report")
				#messageToSend = ""
				counter = 0
				for messageAnswer in currentintrosessionReport[str(authorID)]['answers'][:-1]:
					#messageToSend = messageToSend + questions[counter].split("{")[0] + ": " + str(messageAnswer)+"\n"
					
					counter = counter +1
				counter = 0
				for messageAnswer in currentintrosessionReport[str(authorID)]['answers']:
					if not messageAnswer == "":
						embed.add_field(name=questions[counter], value=str(messageAnswer),inline=False)
					counter = counter +1
				newIntroMessage = await newIntroChannel.send(embed=embed)
						
				currentintrosessionReport[str(authorID)]['newIntroMessageID'] = str(newIntroMessage.id)
						
				await member.send("Thank you. The answers have been sent to the GFS moderators.")
				util.save_data(currentintrosessionReport, "currentintrosessionReport")

async def answer(message,sentAnswer):
	
	global currentintrosessionReport
	
	if not message.guild:
			
		if len(currentintrosessionReport[str(message.author.id)]['answers']) < len(questions):
			if currentintrosessionReport[str(message.author.id)]['confirmed'] == "False":
				
				currentintrosessionReport[str(message.author.id)]['answers'].append(str(sentAnswer).replace("'",""))
				currentintrosessionReport[str(message.author.id)]['lastAnswerTime'] = str(int(time.time()))
				
				if len(currentintrosessionReport[str(message.author.id)]['answers']) < len(questions):
				
					messageToSendRAW = questions[len(currentintrosessionReport[str(message.author.id)]['answers'])]
					messageToSend = messageToSendRAW.split("{")[0]
					messageSent = await message.author.send(messageToSend)
		
		if currentintrosessionReport[str(message.author.id)]['confirmed'] == "False":
			if len(currentintrosessionReport[str(message.author.id)]['answers']) == len(questions):
				await confirm(str(message.author.id),currentintrosessionReport[str(message.author.id)]['guildID'])
				
		util.save_data(currentintrosessionReport, "currentintrosessionReport")
		
class report(commands.Cog):
	
	def is_allowedRole(ctx):
		
		global allowedReporters
		
		admin = False
		
		groups = ctx.message.author.roles
		for group in groups:
			if group.permissions.administrator:
				admin = True
			if (str(group.id) in allowedReporters):
				admin = True
		if str(ctx.message.guild.owner_id) == str(ctx.message.author.id):
			admin = True
		if admin:
			return True
				
		return False
	
	def is_allowedRoleAdmin(ctx):
		
		global allowedReporters
		
		admin = False
		
		groups = ctx.message.author.roles
		for group in groups:
			if group.permissions.administrator:
				admin = True
		if str(ctx.message.guild.owner_id) == str(ctx.message.author.id):
			admin = True
		if admin:
			return True
				
		return False
	
	@commands.Cog.listener()
	async def on_message(self,message: discord.Message):
		
		global currentintrosessionReport
		
		if not message.author.bot:
			#print("Message is not a command")
			if not message.guild:
				#print("Message is a DM")
				if str(message.author.id) in currentintrosessionReport:
					if not currentintrosessionReport[str(message.author.id)]['confirmed'] == "True":
						if 'lastAnswerTime' in currentintrosessionReport[str(message.author.id)]:
							if (int(currentintrosessionReport[str(message.author.id)]['lastAnswerTime']) + 300) < int(time.time()):
								currentintrosessionReport[str(message.author.id)]['confirmed'] = 'Aborted'
								util.save_data(currentintrosessionReport, "currentintrosessionReport")
							else:
								await answer(message,message.content)
						else:
							await answer(message,message.content)
	
	@commands.command(pass_context=True, brief="", name="abort")
	async def abort(self,ctx):
		
		global currentintrosessionReport
		
		if not ctx.message.guild:
				
			if currentintrosessionReport[str(ctx.message.author.id)]['confirmed'] == "False":
				currentintrosessionReport[str(ctx.message.author.id)]['confirmed'] = 'Aborted'
				await ctx.message.author.send("You have now aborted your questions")
				util.save_data(currentintrosessionReport, "currentintrosessionReport")
		else:
			await ctx.message.author.send("Please answer the questions in the DM")
			await ctx.message.delete()
			
	
	@commands.command(pass_context=True, brief="", name="report")
	#@commands.check(is_allowedChannel)
	async def startIntro(self,ctx):
		
		global reportChannelID
		global currentintrosessionReport
		
		try:
		
			if reportChannelID == "":
				return False
			
			if reportChannelID is None:
				return False
			
			testValidChannel = discord.utils.get(ctx.message.guild.channels, id=int(reportChannelID))
			if testValidChannel is None:
				return False
			
			if not ctx.message.guild:
				return False
			
			#print("ok")
			
			if str(ctx.message.author.id) in currentintrosessionReport:
				if currentintrosessionReport[str(ctx.message.author.id)]['confirmed'] == "True":
					if 'processedTime' in (currentintrosessionReport[str(ctx.message.author.id)]):
						if not ((int(currentintrosessionReport[str(ctx.message.author.id)]['processedTime'])+30) < int(time.time())):
							await ctx.message.author.send("You need to wait at least 30 seconds before redoing the report")
							return False
			
			await introStartCommand(ctx.message.author.id,ctx.message.guild.id)
		except:
			traceback.print_exc()
	
	def __init__(self,bot):
		
		global currentintrosessionReport
		global botAcc
		
		try:
			currentintrosessionReport = util.load_data('currentintrosessionReport')
		except:
			currentintrosessionReport = {}
		
		self.bot = bot
		botAcc = bot
		
		print("Report Module started")
		
def setup(bot):
	bot.add_cog(report(bot))