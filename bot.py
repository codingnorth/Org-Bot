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
  # Checks to see if the emoji reaction is from the author and a ✅ or ❎, to remove extraneous reactions 
  # Called in the reaction listener
  def check(reaction, user):
    return user == message.author and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎")

  # Ends code if the message was not sent in the designated listner channel
  if str(message.channel.id) != os.environ.get('CHECK_CHANNEL'):
    return
  
  # Ends code if the message was sent by the bot user, in order to prevent a feedback loop
  if message.author.bot:
    return
  
  # Checks to make sure that the message is only one word, since all GitHub usernames are
  if len(message.content.split()) == 1:
    
    # Sends the confirmation message and adds initial reactions for the User to click on
    x = await message.channel.send("React to Confirm: Invite `" + message.content + "` to the GitHub Organization?")
    await x.add_reaction("✅")
    await x.add_reaction("❎")

    try:
      # Waits for a reaction that satisfies the conditions of the "check" function, and check which it is
      reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
      
      if (str(reaction.emoji) == "✅"):
        # If ✅, get the GitHub user based on the name and add to the Organization
        user = gh.get_user(message.content)
        org = gh.get_organization(os.environ.get("GH_ORG"))
        org.add_to_members(user)
        await message.channel.send("Invited " + message.content)
      
      else:
        # If ❎, send a cancellation confirmation
        await message.channel.send("Request aborted. Please type your username again and confirm!")  
    
    except:
      # On timeout, send a timeout confirmation
      await message.channel.send("Request timed out. Please type your username again and confirm!")

client.run(os.environ.get("BOT_TOKEN"))