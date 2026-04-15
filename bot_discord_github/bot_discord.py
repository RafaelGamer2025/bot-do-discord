import discord
from discord.ext import commands
import random
import asyncio
import requests
import os
import urllib.request
import json

def get_meme():
    url = "https://meme-api.com/gimme"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    return data["url"]

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
    if message.author == bot.user:
        return

    if message.attachments:
        await message.reply("📷 Não sei o que é essa imagem... me ensina? 👀")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            resposta_usuario = await bot.wait_for("message", timeout=30.0, check=check)

            nome_imagem = message.attachments[0].filename.lower()

            if nome_imagem not in memoria:
                memoria[nome_imagem] = []

            memoria[nome_imagem].append(resposta_usuario.content)
            salvar()

            await message.channel.send("Aprendi sobre essa imagem 😎")

        except:
            await message.channel.send("Demorou demais 😴")

        await bot.process_commands(message)  # ✅ ISSO RESOLVE
        return

    await bot.process_commands(message)

# ================= COMANDOS ================= #
@bot.command()
async def memes(ctx):
    escolha = random.choice(["local", "api"])

    if escolha == "local":
        pasta = "images"
        arquivos = os.listdir(pasta)
        imagens = [f for f in arquivos if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

        if imagens:
            caminho = os.path.join(pasta, random.choice(imagens))
            with open(caminho, "rb") as f:
                await ctx.send(file=discord.File(f))
        else:
            await ctx.send("Sem memes locais 😢")

    else:
        meme_url = get_meme()
        await ctx.send(meme_url)

@bot.command()
async def ver_memoria(ctx):
    await ctx.send(f"Eu sei {len(memoria)} coisas 😎")

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def limpar(ctx):
    memoria.clear()
    salvar()
    await ctx.send("Memória apagada 🧠💥")

# ================= START ================= #

bot.run(TOKEN)