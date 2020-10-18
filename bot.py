import os
import discord
from github import Github

client = discord.Client()
gh = Github(os.environ.get("GH_TOKEN"))

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):

  def check(reaction, user):
    return user == message.author and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎")

  if str(message.channel.id) != os.environ.get('CHECK_CHANNEL'):
    print(os.environ.get("CHECK_CHANNEL"))
    print(message.channel.id)
    print(message.channel.id != os.environ.get("CHECK_CHANNEL"))
    return
  
  if message.author == client.user:
    return
  
  if len(message.content.split()) == 1:
    x = await message.channel.send("React to Confirm: Invite `" + message.content + "` to the GitHub Organization?")
    await x.add_reaction("✅")
    await x.add_reaction("❎")
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
      if (str(reaction.emoji) == "✅"):
        user = gh.get_user(message.content)
        org = gh.get_organization(os.environ.get("GH_ORG"))
        org.add_to_members(user)
        await message.channel.send("Invited " + message.content)
      else:
        await message.channel.send("Request aborted. Please type your username again and confirm!")  
    except:
      await message.channel.send("Request timed out. Please type your username again and confirm!")

client.run(os.environ.get("BOT_TOKEN"))