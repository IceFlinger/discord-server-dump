#!/bin/env python
import os
import discord
import sys
import traceback

class dumper(discord.Client):
	def initialize(self, args):
		self.serverId = args[2]

	def write_line(self, f, msg):
		timestamp = str(str(msg.created_at) + " ") 
		idtag = str(msg.id) + " "
		usertag = str(msg.author.name + "#" + msg.author.discriminator + ": ")
		attachtag = ""
		try:
			if msg.attachments:
				names = ""
				for name in msg.attachments:
					names = names + name.filename
				attachtag = " {" + names + "}"
		except AttributeError:
			pass
		f.write(timestamp + idtag + usertag + msg.clean_content + attachtag + "\n")		

	async def on_ready(self):
		servers = self.guilds
		server = None
		for s in servers:
			if self.serverId == str(s.id):
				server = s
		if server is None:
			print("Bot doesn't appear to be in that server, add it at https://discord.com/oauth2/authorize?client_id=" + str(self.user.id) + "&scope=bot&permissions=66560")
			await self.logout()
		else:
			try:
				foldername = str(server.id) + "-" + str(server.name)
				os.mkdir(foldername)
				for channel in server.channels:
					try:
						if channel.history:
							os.mkdir(foldername + "/" + channel.name + "-" + str(channel.id) + "-attachments")
							f = open(foldername + "/" + channel.name + "-" + str(channel.id) + ".log", "w")
							print("Dumping... " + channel.name + "-" + str(channel.id))
							linecount = 0
							attachmentcount = 0
							async for histm in channel.history(limit=None, oldest_first=True):
								self.write_line(f, histm)
								try:
									if histm.attachments:
										for attach in histm.attachments:
											filename = foldername + "/" + channel.name + "-" + str(channel.id) + "-attachments/" + str(histm.id) + "-" + attach.filename
											try:
												await attach.save(filename)
												print("Saved " + filename)
												attachmentcount += 1
											except discord.HTTPException:
												print("Failed to save attachment: " + filename)
											except discord.NotFound:
												print("Attachment was deleted: " + filename)
								except AttributeError:
									pass
								linecount += 1
								if ((linecount%1000)==0):
									print(str(linecount/1000).split(".")[0] + "k lines")
							print("Dumped " + str(linecount) + " lines and " + str(attachmentcount) + " from " + channel.name + "-" + str(channel.id))
					except AttributeError:
						pass
			except FileExistsError:
				print("Folder for server dump exists, delete or rename and rerun to start a new dump")
			await self.logout()

if __name__ == "__main__":
	if "--help" in sys.argv or len(sys.argv) != 3:
		print("Discord server data dumper. Usage:")
		print("./dumper.py BotApiKey ServerId")
		print("Dumps server to a folder named after the server id")
		exit()
	bot = dumper()
	try:
		bot.initialize(sys.argv)
		bot.run(sys.argv[1])
	except discord.errors.LoginFailure as e:
		print("Token is invalid.")
		exit()
	except:
		traceback.print_exc()
	exit()