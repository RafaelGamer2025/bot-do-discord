import discord
from discord.ext import commands
import random
import asyncio
import requests
import os
import urllib.request
import json
import time

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
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

TOKEN = "cole seu token aqui"

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
ID_CANAL_SAUDACAO = None
id_canal = None # Coloque aqui o ID do canal onde o bot deve enviar a mensagem de saudação
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    
    # Tenta enviar a mensagem no canal específico do Discord
    if ID_CANAL_SAUDACAO != 0:
        canal = bot.get_channel(ID_CANAL_SAUDACAO)
        if canal:
            await canal.send("👋 **Oi, eu estou aqui para ajudar!**\nMais informações em `!ajuda`")
        else:
            print(f"ERRO: Não consegui encontrar o canal com ID {ID_CANAL_SAUDACAO}")
    if id_canal != 0:
        canal = bot.get_channel(id_canal)
        if canal:
            await canal.send("👋 **Oi, eu estou aqui para ajudar!**\nMais informações em `!ajuda`")
        else:
            print(f"ERRO: Não consegui encontrar o canal com ID {id_canal}")
    else:
        print("AVISO: Você não configurou o ID_CANAL_SAUDACAO no código.")

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
            time.sleep(3)
            await message.channel.send("Demorou demais 😴")

        await bot.process_commands(message)  # ✅ ISSO RESOLVE
        return

    await bot.process_commands(message)

# ================= COMANDOS ================= #



@bot.command(name="qual")
async def seu_nome(ctx, *, resto_da_pergunta):
    # Se o usuário digitar "!qual seu nome", o 'resto_da_pergunta' será "seu nome"
    if "seu nome" in resto_da_pergunta.lower():
        await ctx.send(f"Meu nome é {bot.user.name}, o bot mais legal deste servidor!")
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
async def poluir(ctx):
    await ctx.send("Poluindo o chat... 🌪️💨")
    for _ in range(5):
        await ctx.send("Poluição! 🌪️💨")
        await asyncio.sleep(1) 
@bot.command()
async def limpar_poluição(ctx):
    await ctx.send("Limpando a poluição... 🧹✨")
    for _ in range(5):
        await ctx.send("Limpeza! 🧹✨")
        await asyncio.sleep(1)
@bot.command()
async def o_que_e_poluição(ctx):
    await ctx.send("Poluição é a presença de substâncias ou agentes no ambiente que causam danos à saúde humana ou ao ecossistema.")
@bot.command()
async def o_que_e_limpeza(ctx):
    await ctx.send("Limpeza é o processo de remover sujeira, impurezas ou poluentes de um ambiente para torná-lo mais saudável e agradável.")
@bot.command()
async def o_que_e_meme(ctx):
    await ctx.send("Meme é uma ideia, comportamento ou estilo que se espalha de pessoa para pessoa dentro de uma cultura, muitas vezes com o objetivo de transmitir um fenômeno, tema ou significado específico.")
@bot.command()
async def ver_memoria(ctx):
    await ctx.send(f"Eu sei {len(memoria)} coisas 😎")
@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def limpar(admin: str, ctx):
    if admin == "admin":
        memoria.clear()
        salvar()
        await ctx.send("Memória apagada 🧠💥")
    else:
        await ctx.send("Você não tem permissão para fazer isso.")
@bot.command(name='jogar')
async def jogar(ctx):
    """Envia o arquivo do jogo para o usuário"""
    nome_arquivo = "eco_missao.py"
    
    if os.path.exists(nome_arquivo):
        embed = discord.Embed(
            title="🎮 Eco-Missão: Limpeza Total",
            description=(
                "Olá! Que bom que você quer ajudar a salvar o planeta! 🌍\n\n"
                "**Como jogar:**\n"
                "1. Baixe o arquivo em anexo.\n"
                "2. Certifique-se de ter o Python instalado.\n"
                "3. Instale o Pygame com o comando: `pip install pygame`.\n"
                "4. Execute o jogo: `python eco_missao.py`.\n\n"
                "Divirta-se!"
            ),
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
        await ctx.send(file=discord.File(nome_arquivo))
    else:
        await ctx.send("❌ Erro: O arquivo do jogo não foi encontrado no servidor do bot.")

@bot.command(name='info')
async def info(ctx):
    """Informações sobre o projeto"""
    await ctx.send("🌱 **Projeto Eco-Missão**: Um jogo feito em Pygame para conscientização ambiental.")
@bot.command()
async def aprender(ctx, *, pergunta_resposta):
    try:
        pergunta, resposta = pergunta_resposta.split(":", 1)
        pergunta = pergunta.strip().lower()
        resposta = resposta.strip()

        if pergunta not in memoria:
            memoria[pergunta] = []

        memoria[pergunta].append(resposta)
        salvar()

        await ctx.send("Aprendi algo novo! 😎")
    except:
        await ctx.send("Formato inválido. Use `!aprender pergunta:resposta`.")
@bot.command()
async def ajuda(ctx):
    comandos = """
    **Comandos disponíveis:**
    `!jogar` - Baixe o jogo Eco-Missão e as instruções para jogar.
    `!info` - Saiba mais sobre o projeto Eco-Missão.
    `!qual seu nome` - Descubra meu nome.
    `!memes` - Envie um meme aleatório (local ou da API).
    `!poluir` - Polua o chat com mensagens engraçadas "apenas admin".
    `!limpar_poluição` - Limpe a poluição do chat.
    `!o_que_e_poluição` - Saiba o que é poluição.
    `!o_que_e_limpeza` - Saiba o que é limpeza.
    `!o_que_e_meme` - Saiba o que é um meme.
    `!ver_memoria` - Veja quantas coisas eu sei.
    `!aprender pergunta:resposta` - Me ensine algo novo (ex: `!aprender O que é Python?:Uma linguagem de programação.`).
    `!duck` - Envie uma imagem aleatória de pato.
    `!limpar` - Apague minha memória "apenas admin".
    """
    await ctx.send(comandos)
# ================= START ================= #

bot.run(TOKEN)