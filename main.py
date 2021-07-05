import discord
import os
import requests

from discord import ChannelType
from dotenv import load_dotenv
from emoji import UNICODE_EMOJI

load_dotenv()

print_information = False


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        if print_information:
            # Display categories and channels of the target Discord server
            target_guild_id = int(os.getenv('TARGET_GUILD_ID'))
            for guild in client.guilds:
                if int(guild.id) == target_guild_id:
                    categories = [c for c in guild.channels if c.type == ChannelType.category]
                    text_channels = [c for c in guild.channels if c.type == ChannelType.text]
                    category_to_channel = {}
                    for category in categories:
                        print(f'{category.name} :')
                        category_to_channel[category.name] = []
                        for c in text_channels:
                            if c.category_id == category.id:
                                print(' -', c, repr(c))
                                category_to_channel[category.name].append(c)

    async def on_message(self, message):
        # Ignore itself
        if message.author.id == self.user.id:
            return

        # Command !alerte-la-planete
        if message.content.startswith('!alerte-la-planete') or message.content.startswith('!alerte-la-planète'):
            print(message.content)
            args = message.content.split(' ')
            args.pop(0)  # Remove command

            # Create a list with all emojis to find in usernames
            emojis = []
            # Add emoji from mentioned channels
            for channel in message.channel_mentions:
                # Ignore channel if it doesn't start with an emoji
                if channel.name[0] in UNICODE_EMOJI['en']:
                    emojis.append(channel.name[0])
            # Also add first character of other args (should be an emoji to work)
            for arg in args:
                if arg and arg[0] in UNICODE_EMOJI['en']:
                    emojis.append(arg[0])

            print('emojis : ', str(emojis))

            # Search the emoji in the nickname of all guild members
            members_to_ping = []
            for member in message.guild.members:
                # Use nickname to search the emoji inside (fallback to the name if nickname hasn't been set)
                nickname = member.nick if member.nick else member.name
                for emoji in emojis:
                    if emoji in nickname:
                        members_to_ping.append(member)
                        break

            # Ping all targeted members if at least one has been found
            if members_to_ping:
                print('Nombre de personnes à pinguer : ', len(members_to_ping))
                offset = 80
                for start in range(len(members_to_ping) // offset + 1):
                    start = start * offset
                    await message.reply(
                        ' '.join(user.mention for user in members_to_ping[start:start+offset]),
                        mention_author=True
                    )
            else:
                await message.reply(
                    'Aucun utilisateur à mentionner...',
                    mention_author=True
                )

        # Command !search-links
        if message.content.startswith('!search-links'):
            args = message.content.split(' ')
            args.pop(0)  # Remove command

            found_links = []
            if args:
                url = 'https://api.short.io/api/links'
                querystring = {'domain_id': os.getenv('SHORT_IO_DOMAIN_ID')}
                headers = {
                    'Accept': 'application/json',
                    'Authorization': os.getenv('SHORT_IO_SECRET_KEY')
                }
                response = requests.get(url, headers=headers, params=querystring)

                # Loop through each links and add it to found_links if one of the args is matching
                for link in response.json()['links']:
                    # Ignore archived links
                    if link['archived']:
                        continue

                    for arg in args:
                        # Stop searching if link has been added
                        if link in found_links:
                            break

                        # Check if in one of the fields is matching one of the args
                        for field in ('title', 'originalURL'):
                            if arg.lower() in link[field].lower():
                                found_links.append(link)
                                break

                        # Check in the tags if link is still not in found_links
                        if link not in found_links:
                            for tag in link['tags']:
                                if arg.lower() in tag.lower():
                                    found_links.append(link)
                                    break

            if found_links:
                embed = discord.Embed()
                embed.title = ' '.join(args)
                embed.description = '\n'.join(f'- [{link["title"]}]({link["shortURL"]})' for link in found_links)
                initial_search = ' '.join(args)
                await message.reply(
                    f'Voici les résultats de votre recherche "{initial_search}":',
                    mention_author=True
                )
                for link in found_links:
                    embed = discord.Embed()
                    embed.title = link['title']
                    embed.type = 'link'
                    embed.url = link['shortURL']
                    embed.set_thumbnail(url=link['icon'])
                    embed.add_field(name='Lien', value=link["shortURL"], inline=False)
                    if link['tags']:
                        embed.add_field(name='Tags', value=' | '.join(tag for tag in link['tags']))
                    await message.channel.send(embed=embed)
            else:
                await message.reply(
                    'Aucun résultat pour votre recherche...',
                    mention_author=True
                )


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    client = MyClient(intents=intents)
    client.run(os.getenv('TOKEN'))
