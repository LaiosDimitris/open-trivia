"""
Discord Bot that uses Open Trivia API for trivia questions.

"""
from discord.ext import commands
import discord
import asyncio
import json
import quiz

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='-', intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await get_servers()

@client.event
async def on_guild_join():
    await get_servers()


async def get_servers():
    with open(r'..\data\info.json', 'r', encoding='utf-8') as json_file:
        info = json.load(json_file)

    for guild in client.guilds:
        info['servers'].append(guild.name)

    with open(r'..\data\info.json', 'w') as json_file:
        json.dump(info, json_file, indent=4)


@client.command()
async def startquiz(ctx, quest_amount: int):
    if not ctx.channel.id in [818405723594555402, 820324323205316608]:
        return

    try:
        quest_amount = int(quest_amount)
    except:
        await ctx.channel.send("**:x: The amount of questions needs to be a number!**")

    members = [{
        "name": member.name,
        "id": member.id,
        "score": 0,
        "answer": 0
    }
    for member in ctx.guild.members if not member.bot]

    for i in range(quest_amount):
        question = quiz.get_question()
        correct_answer = None

        embed = discord.Embed()
        embed.title = question['question']
        embed.set_author(name=f"Question {i+1}/{quest_amount}")
        embed.description = f"Category: `{question['category']}`  Difficulty: `{question['difficulty'].title()}`"
        embed.colour = 0xa200d4
        file = discord.File(question['category_image'], filename='image.png')
        embed.set_thumbnail(url="attachment://image.png")

        for i, answer in enumerate(question['answers']):
            embed.add_field(name=i+1, value=f'`{answer}`', inline=False)
            if answer == question['correct_answer']:
                correct_answer = i+1
    
        question_message = await ctx.channel.send(file=file, embed=embed)

        await asyncio.sleep(2)

        timer = await ctx.channel.send(embed=discord.Embed(
            title=':alarm_clock: Time Left: 20"',
            colour=0xa200d4
        ))

        await asyncio.sleep(1)

        for s in reversed(range(1, 20)):
            await timer.edit(embed=discord.Embed(
                title=f':alarm_clock: Time Left: {s}"',
                colour=0xa200d4
            ))
            await asyncio.sleep(1)

        await timer.edit(embed=discord.Embed(
                title=f":alarm_clock: Time's Up!",
                colour=0xa200d4
            ))

        for j, member in enumerate(members):
            answer = await ctx.channel.history().find(lambda message: message.author.id == member['id'])
            if answer is None:
                continue
            
            if question_message.created_at > answer.created_at:
                continue
            
            if not str(answer.content).isdigit():
                continue
            else:
                members[j]['answer'] = int(answer.content)

            if int(answer.content) == correct_answer:
                members[j]['score'] += 1

        await ctx.channel.send(embed=discord.Embed(
            title=f"{correct_answer}. {question['correct_answer']}",
            colour=0xa200d4
        ))

        await asyncio.sleep(2)

        leadeboard = discord.Embed()
        leadeboard.title = "Leaderboard"
        leadeboard.colour = colour=0xa200d4

        for r, member in enumerate(sorted(members, key=lambda k: k['score'], reverse=True)):
            if str(r + 1).endswith('1'):
                suffix = 'st'
            elif str(r + 1).endswith('2'):
                suffix = 'nd'
            else:
                suffix = 'th'

            value_str = f':white_check_mark: `{member["name"]}`: `{member["score"]}`' if correct_answer == member['answer'] else f':x: `{member["name"]}`: `{member["score"]}`'
            
            leadeboard.add_field(name=f'{r+1}{suffix}', value=value_str, inline=False)

        await ctx.channel.send(embed=leadeboard)

        await asyncio.sleep(5)

    ranked_members = sorted(members, key=lambda k: k['score'], reverse=True)

    if ranked_members[0]['score'] == ranked_members[1]['score']:
        await ctx.channel.send(embed=discord.Embed(
            title=f"Draw",
            colour=0xa200d4
        ))
        return

    winner = ctx.channel.guild.get_member(ranked_members[0]['id'])

    await ctx.channel.send(embed=discord.Embed(
        title=f":first_place: {winner.name} is the winner!",
        colour=0xa200d4
    ).set_thumbnail(url=winner.avatar_url))


@client.command()
async def quizhelp(ctx):
    await ctx.channel.send(embed=discord.Embed(
        title='Commands',
        colour=0xa200d4
    ).add_field(name='`-startquiz`', value='Starts the game. `(Parameters: 1.Amount of questions)`'))
        

with open(r'..\data\info.json', 'r') as json_file:
    client.run(json.load(json_file)['token'])