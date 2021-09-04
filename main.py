import csv

import os
import re
from datetime import datetime
from random import choice, randint

import requests

from discord import ChannelType, File, Intents, Embed
from discord.ext.commands import Bot
from dotenv import load_dotenv
from emoji import emoji_lis

load_dotenv()

print_information = False


class MyBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set an arbitrary count for the word apero based on the current date when initializing the bot
        self.apero_count = datetime.today().day * 44
        self.planet_mention_count = 0
        self.search_links_count = 0

    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        if print_information:
            # Display categories and channels of the target Discord server
            target_guild_id = int(os.getenv('TARGET_GUILD_ID'))
            for guild in bot.guilds:
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
        if not message.author.bot:

            # Prepare and random number to add randomness if the bot replies or not
            random_number = randint(0, 100)

            # Search if message contains "apero"
            if re.search(r"ap[eé]?ro", message.content, re.IGNORECASE):
                # Reset counter on first day of month
                if datetime.today().day == 1 and self.apero_count > 50:
                    self.apero_count = 0
                self.apero_count += 1
                if self.apero_count % 100 == 0:
                    await message.reply(f'Bravo ! Tu viens de proposer la {self.apero_count}ème mention '
                                        f'du mot apéro ce mois-ci 🥳🍹')
                elif random_number < 20:
                    answer_choices = [
                        "On parle toujours d'apéro ici ! 😮",
                        "J'ai cru entendre parler d'apéro ? 😄",
                        '"Il faut apéroiser le changement climatique !" 😁',
                        'Encore un apéro ? 😛',
                        "Où ça un apéro !? 😅",
                        "Vivement l'apéro du 20 à 20h20 ! 😁",
                        "Pensez à préparer 2 mensonges et 1 vérité pour animer l'apéro 😉",
                        'Et... Il y aura du Ricard à cet apéro ? 😍',
                        'Tu prévois le cidre aussi ? (pour les bretons !)',
                        'Apéro (nom masculin) : Du latin apertivus qui signifie ouvrir 🤓',
                        'Euh... Vous avez prévenu <@!696086695283523604> de cet apéro ? 😱',
                        '<@!696086695283523604> a bien donné son aval pour cet apéro ? 😄',
                        "C'est chez <@!696086695283523604> l'apéro ? 😂",
                        "Qui s'occupe de préparer des mojitos ? 🍹🍸",
                        "Eh bah alors ! On n'attend pas Patrick ? 😤"
                    ]
                    if datetime.now().hour < 10:
                        answer_choices.append("Il n'est pas encore un peu tôt pour lancer l'apéro ? 😂")
                    await message.reply(choice(answer_choices))

            # Search if message contains "aper'agro"
            elif re.search(r"ap[eé]r'? ?agro", message.content, re.IGNORECASE):
                answer_choices = [
                    "Rejoignez les Agros, y'a Apér'Agro",
                    "Un verre acheté, une baleine sauvée",
                    'Un verre acheté, un éléphant sauvé',
                    'Un verre acheté, une loutre sauvée',
                    "Un verre acheté, un lama sauvé",
                    "Venez à l'Apér'Agro, les Agros sont aussi chauds que le climat !",
                    "Les Agros ne vous connaissent pas mais vous aiment déjà",
                    "Viens planter des baleines autour d'un verre",
                    "Viens planter des éléphants autour d'un verre",
                    "Viens soutenir les filières agricoles et viticoles avec les Agros ce soir !",
                    'Les Agros, ça suffit, vous êtes trop chauds !',
                ]
                await message.reply(choice(answer_choices))

            # Search if message contains beers emoji
            elif '🍺' in message.content or '🍻' in message.content and random_number < 40:
                answer_choices = [
                    "A la tienne ! 😀",
                    "Oh je vois des bières par ici 😁",
                    'Tchin ! 🍻',
                    'Apéro ? 😄'
                ]
                await message.reply(choice(answer_choices))

        await self.process_commands(message)


if __name__ == '__main__':
    intents = Intents.default()
    intents.members = True
    bot = MyBot(command_prefix='!', intents=intents)

    @bot.command()
    async def ping(ctx):
        await ctx.channel.send("pong")\


    @bot.command(name='alerte-la-planete', aliases=['alerte-la-planète'])
    async def mention_planet_members(ctx, *args):
        bot.planet_mention_count += 1
        print(ctx.message.content)

        # Create a list with all emojis to search in usernames
        emojis = []
        # Add mentioned channels name in the args list
        for channel in ctx.message.channel_mentions:
            args += (channel.name,)
        # Foreach args, check if it starts with an emoji then add it to the emojis list
        for arg in args:
            emoji_list = emoji_lis(arg)
            if emoji_list and emoji_list[0]['location'] == 0:
                emojis.append(emoji_list[0]['emoji'])

        print('emojis : ', str(emojis))

        # Search the emoji in the nickname of all guild members
        members_to_ping = []
        for member in ctx.guild.members:
            # Use nickname to search the emoji inside (fallback to the name if nickname hasn't been set)
            for emoji in emojis:
                if emoji in member.display_name:
                    members_to_ping.append(member)
                    break

        # Ping all targeted members if at least one has been found
        if members_to_ping:
            print('Nombre de personnes à pinguer : ', len(members_to_ping))
            offset = 80
            for start in range(1 + (len(members_to_ping) - 1) // offset):
                start = start * offset
                await ctx.message.reply(
                    ' '.join(user.mention for user in members_to_ping[start:start + offset])
                )
        else:
            await ctx.message.reply('Aucun utilisateur à mentionner...')

    @bot.command(name='search-links')
    async def search_links(ctx, *args):
        bot.search_links_count += 1
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
            embed = Embed()
            embed.title = ' '.join(args)
            embed.description = '\n'.join(f'- [{link["title"]}]({link["shortURL"]})' for link in found_links)
            initial_search = ' '.join(args)
            await ctx.message.reply(f'Voici les résultats de votre recherche "{initial_search}":')
            for link in found_links:
                embed = Embed()
                embed.title = link['title']
                embed.type = 'link'
                embed.url = link['shortURL']
                embed.set_thumbnail(url=link['icon'])
                embed.add_field(name='Lien', value=link["shortURL"], inline=False)
                if link['tags']:
                    embed.add_field(name='Tags', value=' | '.join(tag for tag in link['tags']))
                await ctx.send(embed=embed)
        else:
            await ctx.message.reply('Aucun résultat pour votre recherche...')


    @bot.command(name='quarks-a-accueillir', aliases=['quarks-à-accueillir'])
    async def quarks_to_welcome(ctx):
        filename = 'quarks à accueillir.csv'
        written = False
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom utilisateur Discord', 'Pseudo serveur Time', 'Date arrivée sur le serveur'])
            for member in ctx.guild.members:
                if not member.bot and '*' not in member.display_name:
                    writer.writerow([
                        str(member),
                        member.nick or '',
                        member.joined_at.strftime('%d/%m/%Y %H:%M')]
                    )
                    written = True

        if written:
            # Send file to Discord in message
            with open(filename, 'rb') as file:
                await ctx.message.reply(
                    "Fichier CSV contenant la liste des quarks n'ayant pas d'astérique dans leur nom :",
                    file=File(file, filename)
                )
        else:
            await ctx.message.reply('Aucun quarks à accueillir 😮')
        # Delete file at the end of processing
        os.remove(filename)


    @bot.command(name='bot-info')
    async def get_bot_information(ctx):
        await ctx.message.reply(
            f'Compteur du mot "apéro" : {bot.apero_count}.\n'
            f'Nombre d\'utilisation de la commande "alerte-la-planete" : {bot.planet_mention_count}.\n'
            f'Nombre d\'utilisation de la commande "search-links" : {bot.search_links_count}.\n'
        )


    @bot.command(name='set-bot-apero-count')
    async def set_bot_apero_count(ctx, *args):
        if ctx.message.author.id != int(os.getenv('CREATOR_ID')):
            await ctx.message.reply(f"Désolé, cette commande est réservé au créateur du bot 😜")
        else:
            try:
                value = int(args[0])
            except IndexError:
                await ctx.message.reply('Il faut spécifier une valeur')
            except ValueError:
                await ctx.message.reply(f"{args[0]} n'a pas l'air d'être un nombre")
            else:
                if value < 1:
                    await ctx.message.reply(f"Il me faut une valeur supérieure à 0 😛")
                else:
                    bot.apero_count = value
                    await ctx.message.reply(f"Le compteur du mot apéro a bien été défini à {value} 😉")

    bot.run(os.getenv('TOKEN'))
