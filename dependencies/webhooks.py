import time
import discord
import os
import requests
import datetime
from dependencies.functions import *
from discord_webhook import DiscordWebhook, DiscordEmbed

icon_url = "https://bit.ly/3s2sUDt"
webhook_url = os.getenv('WEBHOOK')

def response_400(site):
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = "```Response 400: Unable To Display Product Variants```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {site} Variants Command", 
        icon_url = icon_url
    )
    return embed

def response_403(site):
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = "```Response 403: Please Try The Command Again```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {site} Variants Command", 
        icon_url = icon_url
    )
    return embed

def response_404(site):
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = "```Response 404: Product Page Has Been Removed```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {site} Variants Command", 
        icon_url = icon_url
    )
    return embed

def invalid_link(site):
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = f"```Invalid {site} Product Link```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {site} Variants Command", 
        icon_url = icon_url
    )
    return embed

def invalid_site(site):
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = f"```The Site Provided Is Not Powered By {site}```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {site} Variants Command", 
        icon_url = icon_url
    )
    return embed

def info_table():
    embed = discord.Embed(
        title = "Shopify Variants Bot", 
        description = "-----------------------------------------------------------------------------------------", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(
        name = "Commands -", 
        value = 
            "```" + ".puma [link]" + "```" + 
            "```" + ".ssense [link]" + "```" + 
            "```" + ".snipes [link]" + "```" + 
            "```" + ".vuja de [link]" + "```" + 
            "```" + ".shopify [link]" + "```" + 
            "```" + ".new balance [link]" + "```", 
        inline=True
    )
    embed.add_field(
        name = "Functions -", 
        value = 
            "```" + "Puma US Information" + "```" + 
            "```" + "SSENSE Information" + "```" + 
            "```" + "Snipes US Information" + "```" + 
            "```" + "VUJA DÉ Information" + "```" + 
            "```" + "AIO Shopify Information" + "```" + 
            "```" + "New Balance US Information" + "```", 
        inline=True
    )
    embed.set_footer(
        text = "Developed by clancy#0001 • Help Command", 
        icon_url = icon_url
    )
    return embed

def construct(command, title, price, link, time, image, sizes, variants, stock=False, total=False):
    embed = discord.Embed(
        title = title, 
        url = link, 
        description = 
            f"```Site: https://{site_name(link)}/```" + 
            f"```Price: {price}```", 
        color = 7572187, 
        timestamp = datetime.datetime.utcnow()
    )
    if not total:
        embed.set_thumbnail(
            url = image
        )
    if sizes:
        embed.add_field(
            name = "Sizes -", 
            value = sizes, 
            inline = True
        )
    if variants:
        embed.add_field(
            name = "Variants -", 
            value = variants, 
            inline = True
        )
    if stock:
        embed.add_field(
            name = "Stock -", 
            value = stock, 
            inline = True
        )
    embed.add_field(
        name = "Processing Time -", 
        value = f"{time} seconds", 
        inline = bool(total)
    )
    if total:
        embed.add_field(
            name = "Total Stock -", 
            value = f"{total - 1} Stock Loaded On Backend", 
            inline = True
        )
    embed.set_footer(
        text = f"Developed by clancy#0001 • {command}", 
        icon_url = icon_url
    )
    return embed

def command_logs(command_name, message):
    if message.author.id != 755891071128436766:
        timestamp = str(time.time()).split(".")[0]
        webhook = DiscordWebhook(
            url = webhook_url
        )
        embed = DiscordEmbed(
            url = message.content.split(" ")[-1],
            title = "Shopify Variants Command Logs", 
            description = f"<@{message.author.id}> Used The {command_name} Variants Command In {message.guild.name}", 
            color='738adb'
        )
        embed.set_thumbnail(
            url = f"{message.guild.icon_url}"
        )
        embed.add_embed_field(
            name = "Timestamp -", 
            value = f"<t:{timestamp}:R> ", 
            inline = True
        )
        embed.add_embed_field(
            name = "Message Link -", 
            value = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}", 
            inline = True
        )
        embed.set_footer(
            text = f"Developed by clancy#0001 • {command_name} Variants Command", 
            icon_url = icon_url
        )
        webhook.add_embed(embed)
        response = webhook.execute()