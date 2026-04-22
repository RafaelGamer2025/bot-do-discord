# 🤖 Eco-Meme & Environmental Assistant

Este bot para Discord é uma ferramenta multifuncional que une **conscientização ambiental**, entretenimento (memes e patos) e um sistema de **aprendizado dinâmico** baseado em JSON. Ele foi desenvolvido para ser interativo, educativo e fácil de expandir.

---

## 🚀 Funcionalidades Principais

* 🌱 **Educação Ambiental:** Comandos informativos sobre poluição e o projeto "Eco-Missão".
* 🎮 **Distribuição de Jogos:** Entrega o arquivo do jogo `eco_missao.py` diretamente pelo chat.
* 🧠 **Sistema de Memória (IA Local):**
    * **Aprendizado por Texto:** Ensine respostas personalizadas ao bot.
    * **Aprendizado por Imagem:** O bot identifica anexos e pergunta ao usuário o que são, salvando a resposta na memória.
* 🖼️ **Mídia Aleatória:**
    * Busca memes de APIs externas ou de uma pasta local (`/images`).
    * Busca fotos fofas de patos via API.
* 🧹 **Moderação e Limpeza:** Comandos para limpar a memória do bot e gerenciar o chat.

---

## 🛠️ Pré-requisitos

Antes de rodar o bot, você precisa ter o **Python 3.8+** instalado e as seguintes bibliotecas:

```bash
pip install discord.py requests