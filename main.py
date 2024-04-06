import discord
from discord.ext import commands, tasks
import logging

bot = commands.Bot(command_prefix="> ", intents=discord.Intents.all())
bot.remove_command("help")

logger = logging.getLogger("embed-creator.bot")
logger.setLevel(logging.DEBUG)

@bot.event
async def on_ready():
    await status_task()
    logger.info("Bot is online!")

    try:
        synced = await bot.tree.sync()
        logger.info(f"{len(synced)} slash commands registered.")
    except Exception as e:
        logger.error(e)

async def status_task():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("Your status..."))

class EmbedModal(discord.ui.Modal, title = "Embed-Creator"):
    def __init__(self):
        super().__init__()

    title_input = discord.ui.TextInput(
        label = "Title",
        required = True,
        style = discord.TextStyle.short
    )

    description_input = discord.ui.TextInput(
        label = "Description",
        required = True,
        style = discord.TextStyle.long
    )

    footer_input = discord.ui.TextInput(
        label = "Footer",
        required = True,
        style = discord.TextStyle.short
    )

    color_input = discord.ui.TextInput(
        label = "Color",
        placeholder = "#efc565",
        required = True,
        max_length = 7,
        style = discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        title = self.title_input.value
        description = self.description_input.value
        footer = self.footer_input.value
        color_str = self.color_input.value

        try:
            color = discord.Colour(value=int(color_str.strip("#"), 16))
        except ValueError:
            color = discord.Colour.default()

        embed = discord.Embed(
            title = title,
            description = description,
            colour = color 
        )

        if footer:
            embed.set_footer(text=footer)

        try:
            await interaction.channel.send(embed=embed)
            await interaction.response.send_message("Embed was successfully created!", ephemeral = True, delete_after = 3)
        except discord.HTTPException as e:
            print(f"Failed to send embed: {e}")

@bot.tree.command(name = "embed", description = "Create a custom embed.")
async def embed(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())

# Paste your bot token in
bot.run(token = "YOUR_BOT_TOKEN", root_logger = True, reconnect = True)