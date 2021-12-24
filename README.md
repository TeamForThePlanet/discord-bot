# discord-bot
A bot to integrate into the Time for the Planet Discord

## How to run the Bot ?

You must have a Discord account in order to create the application and the bot.

- Create an application on the Developer portal of Discord (https://discord.com/developers/applications)
- Create a bot in this application and grab the Token ID. (Settings > Bot > Copy "Token")
- Since the bot tracks has to download the entire member list, check the option `Server Members Intent` in the **Privileged Gateway Intents** section
- Get Server ID: Server Settings > Widget > Copy "Server ID"
- Add the bot into the wanted Discord Server (also grab the ID of the server, you must activate Developer mode in order to see it)
- `git clone https://github.com/TimeForThePlanet/discord-bot.git`
- `pip install -r requirements.txt`
- Create an `.env` file with the following information :

```
TOKEN={Discord Bot Token ID goes here}
TARGET_GUILD_ID={Discord Server ID goes here}
TARGET_ENGLISH_GUILD_ID={English Discord ID goes here}

SHORT_IO_SECRET_KEY={Secret key from Short.io goes here}
SHORT_IO_DOMAIN_ID={Your domain ID from Short.io goes here}

COMMAND_PREFIX={You can change the default command prefix "!"}

CREATOR_ID={Your Discord User ID}
```

- Compile translation messages : `pybabel compile -d locale`
- Run `main.py` script

## Commands

### `!alerte-la-planete`

This command is useful to notify every member from a planet in the Time Discord server. It searches every user that have the planet emoji in their Discord nickname.

For example :

    !alerte-la-planete 🔍

This will ping every member from the evaluators.  
You can also use the hashtag notation to search the planet channel :

    !alerte-la-planete #🔍-évaluateurs-et-évaluatrices

It is also possible to mention multiple planets at the same time :

    !alerte-la-planete #🇪🇸-españa #🇮🇹-italia #🇩🇪-deutschland

### `!quarks-a-accueillir`

This command will generate a CSV file containing all server's members that don't have a `*` in their Discord nickname.

## Behaviour

The bot has a chance to react with a random answer when the word "apero" or a beer emoji seems to appear in someone's message.

## Translation

In order to extract messages to translate, you can use this command:

    pybabel extract . -o locale/base.pot

Then you can update translations for a locale like this:

    pybabel update -d locale -l fr_FR -i locale/base.pot

If the locale doesn't exist in the locale directory, you'll want to init that locale with this command:

    pybabel init -d locale -l it -i locale/base.pot

Finally, after editing `.mo` files, you can compile translations in a `.po` file with this command:

    pybabel compile -d locale