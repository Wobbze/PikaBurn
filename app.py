import discord
from discord.ext import commands
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

# Define the necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure this is enabled for commands to function

token = os.getenv("BOT_TOKEN")
if not token:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Token contract address
token_address = "0xD1e64bcc904Cfdc19d0FABA155a9EdC69b4bcdAe"

# Your Etherscan API key
api_key = os.getenv("API_TOKEN")
if not api_key:
    raise ValueError("API_TOKEN environment variable not set!")

# Initial supply of the tokens
initial_supply = 50000000000  # Assuming the initial supply was 50,000,000,000

def get_total_supply(token_address, api_key):
    url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={token_address}&apikey={api_key}"
    response = urllib.request.urlopen(url)
    data = json.load(response)
    total_supply = float(data["result"])
    total_supply = total_supply/1000000000
    return total_supply

def calculate_total_burned(initial_supply, total_supply):
    total_burned = initial_supply - total_supply
    return total_burned

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def burn(ctx):
    try:
        total_supply = get_total_supply(token_address, api_key)
        total_burned = calculate_total_burned(initial_supply, total_supply)
        formatted_total_supply = "{:,.0f}".format(total_supply)
        formatted_total_burned = "{:,.0f}".format(total_burned)
        response = f"Total Supply: {formatted_total_supply}\nTotal Burned: {formatted_total_burned}"
    except Exception as e:
        response = f"Error occurred: {str(e)}"
    await ctx.send(response)

@bot.command()
async def price(ctx):
    try:
        # Fetch the current token price via Etherscan API
        url = f"https://api.etherscan.io/api?module=stats&action=tokenprice&contractaddress={token_address}&apikey={api_key}"
        response = urllib.request.urlopen(url)
        data = json.load(response)

        print("API response:", data)  # Debug: Print the API response to see the actual structure

        # Check if 'result' is in data and if 'ethPrice' is in result
        if 'result' in data and 'ethPrice' in data['result']:
            token_price = data['result']['ethPrice']  # Adjust this path as per the actual API response
            formatted_price = "{:,.4f}".format(float(token_price))
            response = f"Current Token Price: ${formatted_price} ETH"
        else:
            response = "Error: Unexpected API response format"
    except Exception as e:
        response = f"Error occurred: {str(e)}"
    await ctx.send(response)

bot.run(token)

