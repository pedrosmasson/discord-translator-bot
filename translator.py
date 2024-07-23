import discord
from discord.ext import commands
from googletrans import Translator

import os
from dotenv import load_dotenv

#.env token discord constant
load_dotenv(".env")
token = os.getenv("token")

#prepping our bot
bot = discord.Client()
bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')

#setting the base lang
baseLanguage = ['pt-BR']
print(baseLanguage[0])

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed()
            embed.set_author(name='KappaTeam Translator')
            embed.add_field(name='Use `!lang` or `!l` to pick the base language. Then you can use `!translate` or `!t` and voilà.', inline=False)
            await channel.send(embed=embed)
    break

@bot.command(aliases = ['t'])
async def translate(ctx, *, input = None):

    translator = Translator()
    text = str(input)

    translation = translator.translate(text, dest=str(baseLanguage[0]))

    author_mention =ctx.message.author.mention
    author = ctx.message.author

    embed=discord.Embed()
    embed.set_author(name=str(author)[:-5],icon_url=author.avatar_url)   
    embed.add_field(name=translation.text + '   *(' + baseLanguage[0] + ')*', value='Translation of ' + '"' + text + '"', inline=False)
    msg = await ctx.send(embed=embed)
    await ctx.message.delete()
    await msg.add_reaction('🌍')
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@bot.command(aliases = ['l', 'language'])
async def lang(ctx, language = None):

    with open('languages.txt', 'r') as f:
        if language == None:
            language = 'en'
            baseLanguage[0] = language
            await ctx.send('Language has been set to `' + str(language) + '`👍')
        elif language in f.read():
            await ctx.send('Language has been set to `' + str(language) + '`👍')
            baseLanguage[0] = language
        elif language not in f.read():
            await ctx.send('Language `' + language + '` does not exist, double check the languages with `!list`🌍')
        await ctx.message.delete()

bot.run(token)