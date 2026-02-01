# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
import asyncio

# --- 1. 防休眠網頁 ---
app = Flask('')
@app.route('/')
def home(): return "Music Bot is Alive!"

def run_web(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run_web).start()

# --- 2. 機器人核心 ---
class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ 斜線指令同步完成")

bot = MusicBot()

# --- 3. 音樂指令集 (全部回歸！) ---

@bot.tree.command(name="join", description="召喚機器人進入語音頻道")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message("🎵 | 已就位，隨時可以播放音樂！")
    else:
        await interaction.response.send_message("❌ | 你必須先加入語音頻道", ephemeral=True)

@bot.tree.command(name="play", description="播放音樂 (請輸入歌曲名稱或網址)")
@app_commands.describe(search="歌曲名稱或 YouTube 網址")
async def play(interaction: discord.Interaction, search: str):
    await interaction.response.defer() # 搜尋需要時間，先讓 Discord 等一下
    # 注意：這裡需要配合 wavelink 或 yt-dlp 邏輯，目前先以基礎提示替代
    # 建議後續整合 wavelink 實現高品質播放
    await interaction.followup.send(f"🔍 | 正在搜尋: **{search}** (此功能需配置 Lavalink 伺服器)")

@bot.tree.command(name="pause", description="暫停音樂")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("⏸️ | 音樂已暫停")
    else:
        await interaction.response.send_message("❌ | 目前沒有音樂在播放", ephemeral=True)

@bot.tree.command(name="resume", description="恢復播放")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶️ | 繼續播放音樂")
    else:
        await interaction.response.send_message("❌ | 音樂並未處於暫停狀態", ephemeral=True)

@bot.tree.command(name="stop", description="停止播放並清空隊列")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ | 已停止播放並離開頻道")
    else:
        await interaction.response.send_message("❌ | 我目前不在語音頻道中", ephemeral=True)

# 0---------1---------2---------3---------4---------5---------6---------7---------8
if __name__ == "__main__":
    keep_alive()
    
    # 從 Replit Secrets 抓取鑰匙
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("X 請設置 DISCORD_TOKEN 環境變數")
# 0---------1---------2---------3---------4---------5---------6---------7---------8







