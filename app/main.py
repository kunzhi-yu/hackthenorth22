import asyncio
import math

import discord
from discord.ext import commands

from _cohere.cohere_shit import *
from _cohere.classification import *
from app.db import *

intents = discord.Intents().all()
intents.message_content = True

with open("token") as f:
    token = f.readline()
bot = commands.Bot(command_prefix=".", intents=intents)
embed_picture = "https://cdn.discordapp.com/attachments/1020748712173109392/1020919160953393213/unknown.png"
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
        description = ""
        await reply.edit(content="No description was added, description was set to none.")
    try:
        deadline = await bot.wait_for("message", check=is_same_author(ctx.author), timeout=60)
        pass
    except asyncio.TimeoutError:
        deadline = ""
        await ctx.send("No deadline was added, deadline was set to none.")
    write({
        "id": str(ctx.author.id),
        "title": title,
        "description": description.content,
        "deadline": deadline.content
    })
    embed = discord.Embed(title="Task successfully added!", colour=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(aliases=["rt", "remove"])
async def removetask(ctx, title):
    # query db and remove task
    task = delete_entry(title)
# should be the contents of the query
    embed = discord.Embed(title=f"You are about to remove {task['title']}", description=task['description'])
    embed.set_thumbnail(url=embed_picture)
    if task['deadline'] != 0:
        embed.add_field(name="Deadline", value=task['deadline'], inline=False)
    #embed.set_thumbnail(url="deeznuts")
    embed_msg = await ctx.message.reply(embed=embed)
    # can be buttons, rather should be buttons
    await embed_msg.add_reaction("❌")
    await embed_msg.add_reaction("✅")
    try:
        def check(reaction, user):
            return user != bot.user and str(reaction) in ["❌", "✅"]
        r = await bot.wait_for("reaction_add", check=check, timeout=60)
        if str(r[0].emoji) == "❌":
            await embed_msg.edit(content="Cancelled")
            return
        elif str(r[0].emoji) == "✅":
            print("here")
            delete_entry(title)
            return
    except asyncio.TimeoutError:
        await embed_msg.edit(content="Took too long, cancelled")

@bot.command(aliases=["all", "allt"])
async def alltasks(ctx):
    records = get_all_db()
    relevant_tasks = [i for i in records if i["id"] == str(ctx.author.id)]
    chunked_tasks = [relevant_tasks[i:i + 10] for i in range(0, len(relevant_tasks), 5)]

    embed = discord.Embed(title="Tasks", description="All tasks")
    index = 0
    for task in chunked_tasks[index]:
        embed.add_field(name=task["title"], value=task["description"], inline=False)
    msg_embed = await ctx.reply(embed=embed)
    await msg_embed.add_reaction("⬅️")
    await msg_embed.add_reaction("➡️")
    while True:
        try:
            def check(reaction, user):
                return user != bot.user and str(reaction) in ["⬅️", "➡️"]
            r = await bot.wait_for("reaction_add", check=check, timeout=60)
            if str(r[0].emoji) == "⬅️":
                index = max(0, index - 1)
            elif str(r[0].emoji) == "➡️":
                index = min(index + 1, len(chunked_tasks))
            edit_embed = discord.Embed(title="Tasks", description="All tasks")
            for task in chunked_tasks[index]:
                edit_embed.add_field(name=task["title"], value=task["description"], inline=False)
            await msg_embed.edit(embed=edit_embed)
        except asyncio.TimeoutError:
            return
        except:
            pass


@bot.event
async def on_message(message):

    if (message.author.id != bot.user.id):
        # some shit
        messages.append(message)

        if len(messages) > 10:
            messages.pop(0)
        if len(messages) == 10:
            prompt = "\n".join([bot.get_user(i.author.id).name + ": " + i.content for i in messages])
            tasks = gettasks(prompt, bot.get_user(message.author.id).name)
            for i in range(len(tasks)):
                tasks[i] = tasks[i].strip("\\n")
            goodtasks = classifyPredictionSpam(tasks)
            if len(goodtasks) != 0:
                messages.clear()
                embed = discord.Embed(title="Tasks", description=goodtasks[0])
                embed.set_thumbnail(url=embed_picture)
                embed.set_footer(text="Do you want to add tasks?")
                embed_msg = await message.reply(embed=embed)
                await embed_msg.add_reaction("❌")
                await embed_msg.add_reaction("✅")
                dm_embed = discord.Embed(title="Confirmed!",
                                         description=f"{goodtasks[0]}",
                                         colour=discord.Color.green())
                while True:
                    try:
                        def check(reaction, user):
                            return user != bot.user and str(reaction) in ["❌", "✅"]

                        r = await bot.wait_for("reaction_add", check=check, timeout=90)
                        if str(r[0].emoji) == "❌":
                            await embed_msg.delete()
                            return
                        elif str(r[0].emoji) == "✅":
                            member = r[1]
                            await member.send(embed=dm_embed)
                            write({
                                "id": str(member.id),
                                "title": f"{goodtasks[0]}",
                                "description": "",
                                "deadline": ""
                            })


                            confirmed_embed = discord.Embed(title="Confirmed",
                                                            description=f"{embed.title}\n{', '.join(goodtasks)}",
                                                            colour=discord.Color.green())
                            embed.set_thumbnail(url=embed_picture)
                            confirmed_embed.set_footer(text=f"{r[0].count - 1} users have joined")




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
