# discord-bot
A bot to integrate into the Time for the Planet Discord

## How to run the Bot ?

You must have a Discord account in order to create the application and the bot.

- Create an application on the Developer portal of Discord (https://discord.com/developers/applications)
- Create a bot in this application and grab the Token ID. (Settings > Bot > Copy "Token"
- Since the bot tracks has to download the entire member list, check the option `Server Members Intent` in the **Privileged Gateway Intents** section
- Get Server ID: Server Settings > Widget > Copy "Server ID"
- Add the bot into the wanted Discord Server (also grab the ID of the server, you must activate Developer mode in order to see it)
- `git clone https://github.com/TimeForThePlanet/discord-bot.git`
- `pip install -r requirements.txt`
- Create an `.env` file with the following information :

```
TOKEN={Discord Bot Token ID goes here}
TARGET_GUILD_ID={Discord Server ID goes here}

SHORT_IO_SECRET_KEY={Secret key from Short.io goes here}
SHORT_IO_DOMAIN_ID={Your domain ID from Short.io goes here}
```

- Run `main.py` script
