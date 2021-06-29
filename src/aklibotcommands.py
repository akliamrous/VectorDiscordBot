"""
File Name: aklibotcommands.py
Author: Akli Amrous
Description: This file contains classes (known as cogs in the discord api)
that are used to encapsulate various commands that the discord bot has access
to. Currently, this bot responds to basic text commands and soon will be able
to order pizza utilizing the dominoes api.

Small TODOs:

+Fix meme generator by implementing a python scripting in the res folder
+Implement Embedding to Show what user information that bot has
+Have some handling to prevent user from typing in credit card in non DM chat
+ Implement reddit API to generate memes 
+ Implement AddToOrder Command

Big TODOS:

+Implement a Database system (MongoDB or MySQL) to save user's info for easy pizza

+Host this on a heroku server for constant integration

+Mess around with the Uber API to maybe add rideshare hailing capabilities
"""


from pizzapi.pizzapy import *
import discord 
from discord.ext import commands
import re
import random
import usaddress
import creditcardchecker as c
from memegenerator import MemeGenerator

class PizzaOrder(commands.Cog):
    """
    This class represents a cog in terms of the discord api.
    It defines several methods to allow a user to order
    a pizza utilizing the dominoes api including commands
    to set personal information, several helper methods to
    check the validity of certain sensitive pieces of information
    (such as ccn and phone #), and the main ordering function

    The constructor inherits the client class representing a discord
    bot and defines all neccessary parameters to construct a customer
    object to then order a pizza.

    isValidCreditCard(ccn):    Uses Luhn's algorithm to check if valid ccn
    isValidEmail(email):       Uses a regular expression to check if email is valid
    setname():                 A discord bot command to set the user's name
    setemail():                A discord bot command to set the user's email address
    setnumber():               A discordbot command to set the user's phone number
    setaddress():              A discordbot command to set the User's physical address
    createOrder():             Allows User to enter their order if all
    orderpizza():              If the command has all necessary info, asks for ccn and orders pizza
    """
    def __init__(self, client):
        self.client = client
        self._fname = ""
        self._lname = ""
        self._email = ""
        self._phone = ""
        self._street = ""
        self._state = ""
        self._city = ""
        self._zip = ""
        self._ccn = ""
        self._expdate = ""
        self._cvv = ""
        self._payment = None

    def isValidEmail(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False
        

    @commands.command()
    async def setname(self, ctx, fname, lname):
        await ctx.channel.purge(limit=1)
        if(self._fname == "" and self._lname == ""):
            self._fname = fname 
            self._lname = lname
            await ctx.send("Your name is set as {} {}".format(fname, lname))
        else:
            await ctx.send("You already have a name set, {} {}".format(fname, lname))
    
    @commands.command()
    async def setnumber(self, ctx, number):
        await ctx.channel.purge(limit=1)
        if(self._phone == ""):
            try:
                valuetest = int(number)
                if(len(number) == 10):
                    self._phone = number
                    await ctx.send("Your phone number is set!")
                else:
                    await ctx.send("Enter your phone number in the format: 1234567890")
                    return

            except ValueError:
                await ctx.send("Enter your phone number in the format: 1234567890")
                return
            
        else:
            await ctx.send("You already have a phone number set!")
    
    @commands.command()
    async def setemail(self, ctx, email):
        await ctx.channel.purge(limit=1)
        if(self._email == ""):
            if(self.isValidEmail(email) != True):
                await ctx.send("Sorry, you entered an invalid email!")
                return
            elif(self.isValidEmail(email) == True):
                self._email = email
            
                await ctx.send("Your email is set as {}".format(email))
        else:
            await ctx.send("You already have an email set {} ".format(email))

    @commands.command()
    async def setaddress(self, ctx, *args):
        checkers = ["AddressNumber", "StreetName", "StreetNamePostType", "StreetNamePostDirectional"]
        await ctx.channel.purge(limit=1)
        addr = ""
        street = []
        if(True):
            arguments = args[:]
            for i in arguments:
                if(i is not None):
                    addr= " ".join(args[:]) 
            tagged_addr = usaddress.parse(addr)
            for i in range(0, len(tagged_addr)):
                if(tagged_addr[i][1] in checkers):
                    street.append(tagged_addr[i][0].strip(" ,"))

                if(tagged_addr[i][1] == "PlaceName"):
                    self._city= tagged_addr[i][0].strip(" ,")
                
                if(tagged_addr[i][1] == "StateName"):
                    self._state = tagged_addr[i][0].strip(" ,")
                
                if(tagged_addr[i][1] == "ZipCode"):
                    self._zip = tagged_addr[i][0].strip(" ,")
                
            self._street = " ".join(street)
            
            await ctx.send("Your address is set!")
             
            print(self._street)
            print(self._state)
            print(self._city)
            print(self._zip)
        else:
            await ctx.send("You already have an address set!")

    @commands.command()
    async def setpayment(self, ctx, *args):
        await ctx.channel.purge(limit=1)
        arguments = args
        print(arguments)
        if(len(arguments) != 3):
            await ctx.send("Sorry, Please enter your payment information in the following format: CCN MMYY CVV")
            print("1")
            return
        
        elif(c.isValidCreditCard(arguments[0]) == False):
            await ctx.send("Sorry, Please enter a valid Credit Card Number in the following format: CCN MMYY CVV")
            print(arguments[0])
            return 0

        elif(c.isValidCreditCard(arguments[0]) == True):
            self._cnn = arguments[0]
            self._expdate = arguments[1]
            self._cvv = arguments[2]
            self._zip = "98125"
        
            
            self._payment = CreditCard(self._ccn, self._expdate, self._cvv, self._zip)
            await ctx.send("Payment Method Set!")
        
        
class AkliBotGeneralCommands(commands.Cog):
    """
    This class represents a cog in terms of the discord api.
    It defines several methods to allow a user to access general commands
    through the bot

    The constructor inherits the client class representing a discord
    bot and defines all neccessary parameters such as the monologue
    and a dictionary that references image file to represent memes

    introduceyourself(ctx)           A Discord command that sends the monologue
    meme(ctx)                        A Discord command that sends a random image
    on_message(message)              A Discord event that listens for DMs from the User
    """
    def __init__(self, client):
        self.client = client
        self.SPEECH = "Hey! I'm AkliBot. A digital representation of Akli, my creator. I can do admin tasks and cool API interactions."
        self.memes = MemeGenerator()


    @commands.command()
    async def introduceyourself(self, ctx):
        await ctx.send(self.SPEECH)
        
    @commands.command()
    async def meme(self, ctx):
        await ctx.send(file=discord.File(self.memes.generateMeme()))


    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.channel.TextChannel):
            if message.content.startswith('!ack'):
                await message.author.send('I am AkliBot! Beep Boop!')

        elif isinstance(message.channel, discord.channel.DMChannel):
            if message.content.startswith('!showyourself'):
                await message.channel.send(file=discord.File('vec.jpg'))
            if "Akli" in message.content:
                await message.channel.send("you said my name")



    
