import discord
import os

from discord import ChannelType
from dotenv import load_dotenv


load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
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

    return 0


if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))
