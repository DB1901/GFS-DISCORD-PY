import discord
from discord.ext import commands
import time
import config
import asyncio
import sys
import traceback

botAcc = None

class help(commands.Cog):
	
	@commands.command(pass_context=True, brief="", name='help')
	async def helpCmd(self,ctx,category=None):
		
		modules = {}
		moduleAliases = {}
		moduleAliasesReversed = dict(map(reversed, moduleAliases.items()))
		#print(moduleAliasesReversed)
		
		try:
			#print("RUNNING HELP CMD")
			helptext = "\n__*Commands:__*\n"
			'''
			for command in self.bot.commands:
				#print(command.__dict__)
				helptext = helptext +"**"+str(config.prefix)+str(command)+"**\n"
				try:
					for command2 in command.all_commands:
						helptext = helptext + "\t"+str(command2)+"\n"
						try:
							for command3 in command2.all_commands:
								helptext = helptext + "\t"+str(command3)+"\n"
						except:
							pass
				except:
					pass
			'''
			'''
			for command in self.bot.commands:
				#print(command.__dict__)
				if not str(command.module) in modules:
					modules[str(command.module)] = []
					modules[str(command.module)].append(command)
				else:
					modules[str(command.module)].append(command)
			'''

			for command in self.bot.commands:
				#print(command.__dict__)
				if not str(command.module) in modules:
					modules[str(command.module)] = []
					
				#helptext = helptext +"\n\n__"+str(command.module).replace("plugins.","").upper()+"__:\n"
				if not category is None:
					if str(category) == str(command):
						modules[str(command.module)].append(command)
					elif str(category).lower() == str(command.module).replace("plugins.","").lower():
						modules[str(command.module)].append(command)
					elif str(category) in moduleAliasesReversed:
						#print(str(moduleAliasesReversed[str(category)]))
						#print(str(command))
						if str(moduleAliasesReversed[str(category)]).lower() == str(command.module).replace("plugins.","").lower():
							#print("Adding command")
							modules[str(command.module)].append(command)
				else:
					modules[str(command.module)].append(command)
			
			if category is None:
				helptext = "**Use !help <category> for more information about a specific category**\n\n"
				for module in modules:
					if not str(module).replace("plugins.","") in moduleAliases:
						helptext = helptext +str(module).replace("plugins.","").capitalize()+"\n"
					else:
						helptext = helptext +moduleAliases[str(module).replace("plugins.","")]+"\n"
				
				if not str(helptext).strip() == "":
					embed = discord.Embed(title="Help",description=str(helptext))
					await ctx.send(embed=embed)
				return True
			
			#print(modules)
			for module in modules:
				if not len(modules[module]) == 0:
					helptext = helptext +"\n\n__"+str(module).replace("plugins.","").upper()+"__:\n"
				for command in modules[module]:
					#print(command.__dict__)
					sorted_key_list = [i for i in command.params.keys()]
					params = sorted_key_list[2:]
					argString = ""
					for param in params:
						argString = argString+" <"+param+"> "
					
					try:
						if not command.brief is None:
							desc = command.brief+"\n\n"
							if desc == "\n\n":
								desc = ""
						else:
							desc = ""
					except:
						desc = ""
					
					helptext = helptext +str(config.prefix)+str(command)+" "+str(argString)+"\n"+str(desc)
					try:
						for command2 in command.all_commands:
							sorted_key_list = [i for i in command.all_commands[command2].params.keys()]
							params = sorted_key_list[2:]
							argString = ""
							for param in params:
								argString = argString+" <"+param+"> "
							
							#print(command.all_commands[command2].__dict__)
							try:
								if not command.all_commands[command2].brief is None:
									desc2 = command.all_commands[command2].brief+"\n\n"
									if desc2 == "\n\n":
										desc2 = ""
								else:
									desc2 = ""
							except:
								desc2 = ""
								
							helptext = helptext + "\t"+str(config.prefix)+str(command)+" "+str(command2)+" "+str(argString)+"\n"+str(desc2)
							
							if len(helptext) > 1000:
								embed = discord.Embed(title="Help",description=str(helptext))
								await ctx.send(embed=embed)
								helptext = ""
							
							try:
								#print(command.all_commands[command2])
								for command3 in command.all_commands[command2].all_commands:
									sorted_key_list = [i for i in command.all_commands[command2].all_commands[command3].params.keys()]
									params = sorted_key_list[2:]
									argString = ""
									for param in params:
										argString = argString+" <"+param+"> "
									
									try:
										if not command.all_commands[command3].brief is None:
											desc3 = command.all_commands[command3].brief+"\n\n"
											if desc3 == "\n\n":
												desc3 = ""
										else:
											desc3 = ""
									except:
										desc3 = ""
										
									helptext = helptext + "\t\t"+str(config.prefix)+str(command)+" "+str(command2)+" "+str(command3)+" "+str(argString)+"\n"+str(desc3)
									try:
										for command4 in command.all_commands[command2].all_commands[command3].all_commands:
											sorted_key_list = [i for i in command.all_commands[command2].all_commands[command3].all_commands[command4].params.keys()]
											params = sorted_key_list[2:]
											argString = ""
											for param in params:
												argString = argString+" <"+param+"> "
											
											try:
												if not command.all_commands[command4].brief is None:
													desc4 = command.all_commands[command4].brief+"\n\n"
													if desc4 == "\n\n":
														desc4 = ""
												else:
													desc4 = ""
											except:
												desc4 = ""
												
											helptext = helptext + "\t\t"+str(config.prefix)+str(command)+" "+str(command2)+" "+str(command3)+" "+str(command4)+" "+str(argString)+"\n"+str(desc4)
									except:
										pass
							except:
								#traceback.print_exc()
								pass
					except:
						#print(command.__dict__)
						pass
				if len(helptext) > 1000:
					embed = discord.Embed(title="Help",description=str(helptext))
					await ctx.send(embed=embed)
					helptext = ""
				#helptext = helptext +"\n"
			#helptext+="```"
			if not str(helptext).strip() == "":
				embed = discord.Embed(title="Help",description=str(helptext))
				await ctx.send(embed=embed)
		except:
			traceback.print_exc()
		
	def __init__(self,bot):
		
		self.bot = bot
		
		botAcc = bot
		
		print("Help Module started")
		
def setup(bot):
	bot.add_cog(help(bot))