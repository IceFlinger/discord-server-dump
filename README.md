# Discord Server Dumper

```
Discord server data dumper. Usage:
`./dumper.py BotApiKey ServerId`
Dumps server to a folder named after the server id
```
Run `pip install -r requirements.txt` to install the dependencies (discord python api)

Needs a bot application/api key with a bot user that's joined to the server you want to dump (no you can't use this to dump servers you don't own/have permission for, thats pushing the discord tos). Will dump all visible channel logs to a .log file with that channel, as well as all attachments/images into an associated folder. The message an attachment was uploaded with can be traced using the message ids in the logfile line/attachment filename respectively.

```
todo maybe:
*dump rest of guild data like emojis etc
*more options for format/filtering/what to dump
*hosted version that doesn't need a bot app and emails you a zip (depends if i can maintain)
```