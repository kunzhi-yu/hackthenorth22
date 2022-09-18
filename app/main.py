import asyncio
import functools
import typing

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from _cohere import cohere_semantic_extraction
from _cohere.classification import *
from _cohere.cohere_shit import *
from app.db import *

intents = discord.Intents().all()
intents.message_content = True

with open("token") as f:
    token = f.readline()
bot = commands.Bot(command_prefix=".", intents=intents)
embed_picture = "https://cdn.discordapp.com/attachments/1020748712173109392/1020919160953393213/unknown.png"
messages = []

showcasedictionary = {
    '166271462175408130': ['bake cake', 'go to math office hours', 'read research papers', 'get art supplies',
                           'practice math proofs'],
    '375149906240733184': ['read research paper', 'Go to the Art Gallery']}


# wait_for checks
def is_same_author(author):
    def inner(message):
        return message.author.id == author.id

    return inner


@bot.event
async def on_ready():
    print("I'm alive")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.command(aliases=["at", "add"])
async def addtask(ctx, *args):
    global messages
    title = " ".join(args)
    reply = await ctx.reply("Please input a description (optional)")
    try:
        d = await bot.wait_for("message", check=is_same_author(ctx.author), timeout=60)
        description = d.content
        try:
            messages = [i for i in messages if i != description]
        except:
            pass
        await d.reply("Please input a deadline (optional)")
    except asyncio.TimeoutError:
        description = "None"
        await reply.edit(content="No description was added, description was set to none.")
    try:
        dl = await bot.wait_for("message", check=is_same_author(ctx.author), timeout=60)
        deadline = dl.content
        try:
            messages = [i for i in messages if i != deadline]
        except:
            pass
    except asyncio.TimeoutError:
        deadline = "None"
        await ctx.send("No deadline was added, deadline was set to none.")
    write({
        "id": str(ctx.author.id),
        "title": title,
        "description": description,
        "deadline": deadline
    })
    embed = discord.Embed(title="Task successfully added!", colour=discord.Color.green())
    embed.set_thumbnail(url=embed_picture)
    await ctx.send(embed=embed)


@bot.command(aliases=["rt", "remove"])
async def removetask(ctx, title):
    # query db and remove task
    task = query_entry(title)
    # should be the contents of the query
    embed = discord.Embed(title=f"You are about to remove {task['title']}", description=task['description'])
    embed.set_thumbnail(url=embed_picture)
    if task['deadline'] != 0:
        embed.add_field(name="Deadline", value=task['deadline'], inline=False)
    embed_msg = await ctx.message.reply(embed=embed)
    await embed_msg.add_reaction("❌")
    await embed_msg.add_reaction("✅")
    try:
        def check(reaction, user):
            return user != bot.user and str(reaction) in ["❌", "✅"]

        r = await bot.wait_for("reaction_add", check=check, timeout=60)
        if str(r[0].emoji) == "❌":
            edit_embed = discord.Embed(title="Cancelled", color=discord.Color.red())
            edit_embed.set_thumbnail(url=embed_picture)
            await embed_msg.edit(embed=edit_embed)
            return
        elif str(r[0].emoji) == "✅":
            delete_entry(title)
            edit_embed = discord.Embed(title="Successfully deleted task", color=discord.Color.green())
            edit_embed.set_thumbnail(url=embed_picture)
            await embed_msg.edit(embed=edit_embed)
            return
    except asyncio.TimeoutError:
        await embed_msg.edit(content="Took too long, cancelled")

@bot.command(aliases=["c"])
async def complete(ctx, title):
    # query db and remove task
    task = query_entry(title)
    # should be the contents of the query
    embed = discord.Embed(title=f"You are about to mark {task['title']} as complete", description=task['description'])
    embed.set_thumbnail(url=embed_picture)
    if task['deadline'] != 0:
        embed.add_field(name="Deadline", value=task['deadline'], inline=False)
    embed_msg = await ctx.message.reply(embed=embed)
    await embed_msg.add_reaction("❌")
    await embed_msg.add_reaction("✅")
    try:
        def check(reaction, user):
            return user != bot.user and str(reaction) in ["❌", "✅"]

        r = await bot.wait_for("reaction_add", check=check, timeout=60)
        if str(r[0].emoji) == "❌":
            edit_embed = discord.Embed(title="Cancelled", color=discord.Color.red())
            edit_embed.set_thumbnail(url=embed_picture)
            await embed_msg.edit(embed=edit_embed)
            return
        elif str(r[0].emoji) == "✅":
            delete_entry(title)
            edit_embed = discord.Embed(title="Successfully completed task", color=discord.Color.green())
            edit_embed.set_thumbnail(url=embed_picture)
            await embed_msg.edit(embed=edit_embed)
            return
    except asyncio.TimeoutError:
        await embed_msg.edit(content="Took too long, cancelled")

@bot.command(aliases=["all", "allt"])
async def alltasks(ctx):
    records = get_all_db()
    relevant_tasks = [i for i in records if i["id"] == str(ctx.author.id)]
    if not relevant_tasks:
        await ctx.reply("No tasks")
    chunked_tasks = [relevant_tasks[i:i + 5] for i in range(0, len(relevant_tasks), 5)]

    index = 0
    desc = ""
    for task in chunked_tasks[index]:
        desc += f"{task['title']} - {task['description']}\n"
    embed = discord.Embed(title="Tasks", description=f"All tasks\n```\n{desc}```")
    embed.set_thumbnail(url=embed_picture)
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

            desc = ""
            it = sorted(chunked_tasks[index], key=lambda x: len(x['title']))
            for task in it:
                desc += f"{task['title']} - {task['description']}\n"
            edit_embed = discord.Embed(title="Tasks", description=f"All tasks\n```\n{desc}```")
            edit_embed.set_thumbnail(url=embed_picture)
            await msg_embed.edit(embed=edit_embed)
        except asyncio.TimeoutError:
            return
        except:
            pass

async def run_blocking(blocking_func: typing.Callable, *args):
    func = functools.partial(blocking_func, *args)
    return await bot.loop.run_in_executor(None, func)

@bot.command(aliases=["tasks", "order"])
async def sendtasks(ctx):
    reply_msg = await ctx.reply("Please wait...")
    content_list = [i.content.strip("\n").strip() async for i in ctx.channel.history(limit=500)]
    id_list = [str(i.author.id) async for i in ctx.channel.history(limit=500)]
    relevant_tasks = await run_blocking(cohere_semantic_extraction.main_sent_extract, content_list, id_list)
    tasks = [i for i in relevant_tasks if i["id"] == str(ctx.author.id)]
    if not tasks:
        await ctx.reply("No tasks")
    if (len(tasks) < 5):
        chunked_tasks = [tasks]
    else:
        chunked_tasks = [tasks[i:i + 5] for i in range(0, len(tasks), 5)]

    index = 0
    desc = ""
    for task in chunked_tasks[index]:
        desc += f"{task['title']} - {task['description']}\n"
    embed = discord.Embed(title="Tasks", description=f"All tasks\n```\n{desc}```")
    embed.set_thumbnail(url=embed_picture)
    await reply_msg.delete()
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

            desc = ""
            it = sorted(chunked_tasks[index], key=lambda x: len(x['title']))
            for task in it:
                desc += f"{task['title']} - {task['description']}\n"
            edit_embed = discord.Embed(title="Tasks", description=f"All tasks\n```\n{desc}```")
            edit_embed.set_thumbnail(url=embed_picture)
            await msg_embed.edit(embed=edit_embed)
        except asyncio.TimeoutError:
            return
        except:
            pass

@bot.event
async def on_message(message):
    global messages
    if (message.author.id != bot.user.id):
        if not (message.content.startswith(".")):
            messages.append(message)
            if len(messages) > 5:
                messages.pop(0)
            if len(messages) == 5:
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
                    dm_embed.set_thumbnail(url=embed_picture)
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
                                    "description": "None",
                                    "deadline": "None"
                                })
                                confirmed_embed = discord.Embed(title="Confirmed",
                                                                description=f"{embed.title}\n{', '.join(goodtasks)}",
                                                                colour=discord.Color.green())
                                embed.set_thumbnail(url=embed_picture)
                                confirmed_embed.set_footer(text=f"{r[0].count - 1} users have joined")
                                await embed_msg.edit(embed=confirmed_embed)
                        except asyncio.TimeoutError:
                            await embed_msg.delete()
                            break
        else:
            await bot.process_commands(message)


bot.run(token)
