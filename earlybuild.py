import discord
from discord import app_commands
import requests

ROBLOX_API_BASE_URL = "https://users.roblox.com/v1"
GAMES_API_BASE_URL = "https://games.roblox.com/v1"

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}!")

def fetch_user_stats(user_id):
    """
    Get stats for a user by their user ID.
    """
    try:
        response = requests.get(f"{ROBLOX_API_BASE_URL}/users/{user_id}")
        response.raise_for_status()
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "display_name": data["displayName"],
            "created": data["created"]
        }
    except requests.RequestException as e:
        return {"error": str(e)}

@bot.tree.command(name="account_lookup", description="Look up stats for a Roblox account.")
@app_commands.describe(account_id="Enter the Roblox account ID")
async def account_lookup(interaction: discord.Interaction, account_id: str):
    """
    Look up a Roblox account by its ID and display stats.
    """
    await interaction.response.defer()

    user_stats = fetch_user_stats(account_id)
    if user_stats is None or "error" in user_stats:
        await interaction.followup.send(f"Error: Could not locate user with account ID '{account_id}'.")
        return

    embed = discord.Embed(title="Roblox User Stats", color=discord.Color.red())
    embed.add_field(name="Display Name", value=user_stats["display_name"], inline=False)
    embed.add_field(name="Username", value=user_stats["name"], inline=False)
    embed.add_field(name="User ID", value=user_stats["id"], inline=False)
    embed.add_field(name="Account Created", value=user_stats["created"], inline=False)
    await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    bot.run("token")
