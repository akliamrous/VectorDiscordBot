import discord 
from discord.ext import commands 
from vectorbotcommands import VectorBotGeneralCommands, PizzaOrder

bot = commands.Bot(command_prefix="!",
description="Hey! I'm applying for a new villain loan. I go by the name of VectorBot. It's a Software term, represented by a Discord API Application with both direction and magnitude. VectorBot! That's me, because I accept general commands with both direction and magnitude. Oh yeah!")

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help"))

bot.add_cog(VectorBotGeneralCommands(bot))
bot.add_cog(PizzaOrder(bot))
bot.run('NzYxMTA1NzYwMTUxMTQyNDEw.X3Vw-Q.-viLNNjqO1lhXyx2bdAr2XbR08w')