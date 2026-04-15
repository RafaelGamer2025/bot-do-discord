import discord
from discord.ext import commands
import json
import random
import asyncio

TOKEN = "COLE_SEU_TOKEN_AQUI"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= MEMÓRIA ================= #

try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except:
    memoria = {}

def salvar():
    with open("memoria.json", "w") as f:
        json.dump(memoria, f, indent=4)

# ================= IA ================= #

def encontrar_resposta(msg):
    msg = msg.lower()

    # procura algo parecido
    for pergunta in memoria:
        if pergunta in msg or msg in pergunta:
            return random.choice(memoria[pergunta])

    return None

# ================= EVENTOS ================= #

@bot.event
async def on_ready():
    print(f"🤖 Bot aprendendo como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    async with message.channel.typing():
        await asyncio.sleep(random.uniform(0.5, 1.5))

    resposta = encontrar_resposta(msg)

    if resposta:
        await message.reply(resposta)

    else:
        await message.reply("Não sei responder ainda... me ensina? 👀")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            resposta_usuario = await bot.wait_for("message", timeout=30.0, check=check)

            if msg not in memoria:
                memoria[msg] = []

            memoria[msg].append(resposta_usuario.content)
            salvar()

            await message.channel.send("Aprendi 😎")

        except:
            await message.channel.send("Demorou demais 😴")

    await bot.process_commands(message)

# ================= COMANDOS ================= #

@bot.command()
async def memoria(ctx):
    await ctx.send(f"Eu sei {len(memoria)} coisas 😎")

@bot.command()
async def limpar(ctx):
    memoria.clear()
    salvar()
    await ctx.send("Memória apagada 🧠💥")

# ================= START ================= #

bot.run(TOKEN)