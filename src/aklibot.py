import discord 
from discord.ext import commands 
from vectorbotcommands import VectorBotGeneralCommands, PizzaOrder

bot = commands.Bot(command_prefix="!",
description="Hey! I'm AkliBot. A digital representation of Akli, my creator. I can do admin tasks and cool API interactions.")

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help"))

bot.add_cog(VectorBotGeneralCommands(bot))
bot.add_cog(PizzaOrder(bot))
bot.run('')
