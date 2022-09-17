import asyncio

import discord
from discord.ext import commands

from _cohere.cohere_shit import *
from _cohere.classification import *

intents = discord.Intents().all()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)
token = ""

messages = []
# wait_for checks
def is_same_author(author):
    def inner(message):
        return message.author.id == author.id
    return inner

@bot.event
async def on_ready():
    print("I'm alive")

@bot.command(aliases=["at", "add"])
async def addtask(ctx, title):
    reply = await ctx.reply("Please input a description (optional)")
    try:
        description = await bot.wait_for("message", check=is_same_author(ctx.author), timeout=60)
        await description.reply("Please input a deadline (optional)")
    except asyncio.TimeoutError:
        await reply.edit(content="No description was added, description was set to none.")
    try:
        deadline = await bot.wait_for("message", check=is_same_author(ctx.author), timeout=60)
        # put into db
        pass
    except asyncio.TimeoutError:
        await ctx.send("No deadline was added, deadline was set to none.")

@bot.command(aliases=["rt", "remove"])
async def removetask(ctx, title):
    # query db and remove task
    task = title  # should be the contents of the query
    embed = discord.Embed(title=f"You are about to remove {task.title}", description=task.description)
    if task.deadline != 0:
        embed.add_field(name="Deadline", value=task.deadline, inline=False)
    embed.set_thumbnail(url="deeznuts")
    embed_msg = await ctx.message.reply(embed=embed)
    # can be buttons, rather should be buttons
    await embed_msg.add_reaction("❌")
    await embed_msg.add_reaction("✅")
    try:
        def check(reaction, user):
            return reaction.id == user.id
        r = await bot.wait_for("reaction", check=check, timeout=60)
        if str(r[0].emoji) == "❌":
            await embed_msg.edit(content="Cancelled")
            return
        elif str(r[0].emoji) == "✅":
            # remove from db
            return
    except asyncio.TimeoutError:
        await embed_msg.edit(content="Took too long, cancelled")

@bot.event
async def on_message(message):

    if (message.author.id != bot.user.id):
        # some shit
        messages.append(message)

        if len(messages) > 2:
            messages.pop(0)
        if len(messages) == 2:

            prompt = "\n".join([bot.get_user(i.author.id).name + ": " + i.content for i in messages])
            tasks = gettasks(prompt, bot.get_user(message.author.id).name)
            for i in range(len(tasks)):
                tasks[i] = tasks[i].strip("\\n")
            goodtasks = classifyPrediction(tasks)
            if len(goodtasks) != 0:
                messages.clear()
                embed = discord.Embed(title="Tasks", description=", ".join(goodtasks))
                embed.set_footer(text="Do you want to add tasks?")
                embed_msg = await message.reply(embed=embed)
                await embed_msg.add_reaction("❌")
                await embed_msg.add_reaction("✅")
                while True:
                    try:
                        def check(reaction, user):
                            return user != bot.user and str(reaction) in ["❌", "✅"]

                        r = await bot.wait_for("reaction_add", check=check, timeout=90)
                        if str(r[0].emoji) == "❌":
                            await embed_msg.delete()
                            return
                        elif str(r[0].emoji) == "✅":
                            confirmed_embed = discord.Embed(title="Confirmed",
                                                            description=f"{embed.title}\n{', '.join(goodtasks)}",
                                                            colour=discord.Color.green())
                            confirmed_embed.set_footer(text=f"{r[0].count - 1} users have joined")
                            member = r[1]
                            dm_embed = discord.Embed(title="Confirmed!",
                                                            description=f"{', '.join(goodtasks)}",
                                                            colour=discord.Color.green())
                            await member.send(embed = dm_embed)

                            await embed_msg.edit(embed=confirmed_embed)
                            user_id = member.id
                            task = f"{', '.join(goodtasks)}"
                            # Send this selection to the database
                    except asyncio.TimeoutError:
                        await embed_msg.delete()
                        break
            else:

                await bot.process_commands(message)

bot.run(token)
