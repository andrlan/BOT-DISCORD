import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Token bot Anda 
TOKEN = 'TOKEN_BOT_DISCORD'

@bot.event
async def on_ready():
    print(f'Bot {bot.user} sudah online!')

@bot.command()
async def create(ctx):
    guild = ctx.guild
    member = ctx.author

    print(f"Command received from {member.name} in guild {guild.name}")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    try:
        existing_channel = discord.utils.get(guild.text_channels, name=f'private-{member.name.lower()}')
        if existing_channel:
            await ctx.send(f'Channel pribadi Anda sudah ada: {existing_channel.mention}')
            print(f"Existing channel found: {existing_channel.name}")
            return

        print(f"Creating channel for {member.name}")

        channel = await guild.create_text_channel(f'private-{member.name.lower()}', overwrites=overwrites)
        await ctx.send(f'Channel pribadi telah dibuat: {channel.mention}')

        print(f"Channel created: {channel.name}")

    except discord.Forbidden:
        await ctx.send("Bot does not have permission to create channels.")
        print("Permission error: Bot does not have permission to create channels.")
    except discord.HTTPException as http_err:
        await ctx.send("Failed to create channel due to an HTTP exception.")
        print(f"HTTP exception: {http_err}")
    except Exception as e:
        await ctx.send("Terjadi kesalahan saat membuat channel pribadi.")
        print(f"Unexpected error: {e}")

bot.run(TOKEN)
