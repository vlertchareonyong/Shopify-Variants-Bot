import os
import asyncio
import discord
from modules.ssense import *
from modules.vuja_de import *
from modules.shopify import *
from modules.new_balance import *
from dependencies.webhooks import *

client = discord.Client()

@client.event
async def on_ready():
    activity_string = '{} servers'.format(len(client.guilds))
    await client.change_presence(
        activity = discord.Activity(
            type = discord.ActivityType.watching, 
            name = activity_string
        )
    )
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startstwith('.help'):
        await message.channel.send(embed=info_table())
    elif message.content.startswith('.shopify '):
        command_logs("Shopify", message)
        await message.channel.send(embed=shopify(message))
    elif message.content.startswith('.new balance '):
        command_logs("New Balance", message)
        await message.channel.send(embed=new_balance(message))
    elif message.content.startswith('.ssense '):
        command_logs("SSENSE", message)
        await message.channel.send(embed=ssense(message))
    elif message.content.startswith('.vuja de '):
        command_logs("VUJA DÉ", message)
        await message.channel.send(embed=vuja_de(message))

@client.event
async def on_reaction_add(reaction, user):
    pass

client.run(os.getenv('TOKEN'))