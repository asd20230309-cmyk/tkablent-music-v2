# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# ==========================================
# 第一部分：防休眠網頁指令 (給 UptimeRobot 看的)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    # 當監控網站訪問這個路徑時，會看到這行字
    return "Bot Status: Online and Active!"

def run_web_server():
    # 啟動微型網頁
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # 使用 Thread (執行緒) 讓網頁在背景跑，不干擾機器人
    t = Thread(target=run_web_server)
    t.start()

# ==========================================
# 第二部分：Discord 機器人指令 (你在 Discord 輸入的)
# ==========================================
class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 同步斜線指令
        await self.tree.sync()
        print("✅ Discord 指令同步完成")

bot = MusicBot()

@bot.tree.command(name="join", description="加入語音頻道")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message("✅ 機器人已就位！")
    else:
        await interaction.response.send_message("❌ 你必須先加入語音頻道", ephemeral=True)

@bot.tree.command(name="leave", description="離開語音頻道")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("📤 辛苦了，我先離開囉！")
    else:
        await interaction.response.send_message("❌ 機器人目前不在頻道裡", ephemeral=True)

# ==========================================
# 第三部分：啟動開關
# ==========================================
if __name__ == "MTQ2NDcwMDE4MDg2MjYwMzI2NA.G3r5gj.HsF5ZHtabgjYaTKcFtHqCu32nYH1Dv3Lt6PSoY":
    # 1. 先啟動網頁 (分開跑)
    keep_alive()
    
    # 2. 再啟動機器人 (填入你重設後的 Token)
    TOKEN = "在這裡填入你的新TOKEN"
    bot.run(TOKEN)
# 0---------1---------2---------3---------4---------5---------6---------7---------8




