# 0---------1---------2---------3---------4---------5---------6---------7---------8
    import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
import asyncio

# --- 第一部分：防休眠網頁系統 (給 UptimeRobot 監控用) ---
app = Flask('')

@app.route('/')
def home():
    return "Music Bot Status: Online"

def run_web_server():
    # Replit 必須使用 8080 端口
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

class MyMusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # 讀取訊息內容權限
        intents.voice_states = True     # 語音連線權限
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 啟動時同步斜線指令到 Discord
        await self.tree.sync()
        print("✅ 同步完成")

    async def on_ready(self):
        print(f"✅ 機器人 {self.user} 已成功上線並登入！")

bot = MyMusicBot()

# --- 第三部分：音樂功能指令區 ---

@bot.tree.command(name="join", description="將機器人召喚至您的語音頻道")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("🎶 | 我來了！準備好播放音樂了。")
    else:
        await interaction.response.send_message("❌ | 你必須先進入一個語音頻道！", ephemeral=True)

@bot.tree.command(name="play", description="查詢並播放音樂 (YouTube)")
@app_commands.describe(search="請輸入歌名或 YouTube 網址")
async def play(interaction: discord.Interaction, search: str):
    # 解決 10062 錯誤：立即讓 Discord 進入「思考中」狀態，爭取更多時間
    await interaction.response.defer(thinking=True)
    
    # 這裡暫時模擬查詢邏輯，實際播放需配置音訊庫 (如 yt-dlp)
    await asyncio.sleep(2) 
    
    # 使用 followup 發送查詢結果
    await interaction.followup.send(f"🔍 | 正在搜尋：**{search}**\n⚠️ | 播放引擎載入中，請稍候。")

@bot.tree.command(name="pause", description="暫停目前播放的音樂")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("⏸️ | 音樂已暫停。")
    else:
        await interaction.response.send_message("❌ | 目前沒有音樂正在播放。", ephemeral=True)

@bot.tree.command(name="resume", description="恢復播放暫停中的音樂")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶️ | 音樂已恢復播放。")
    else:
        await interaction.response.send_message("❌ | 沒有被暫停的音樂。", ephemeral=True)

@bot.tree.command(name="leave", description="讓機器人離開當前語音頻道")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("📤 | 已退出語音頻道，下次見！")
    else:
        await interaction.response.send_message("❌ | 我目前不在任何頻道中。", ephemeral=True)

# --- 第四部分：啟動入口 ---
if __name__ == "__main__":
    # 1. 啟動防休眠網頁
    keep_alive()
    
    # 2. 從 Replit Secrets 抓取 Token (請確保 Key 叫 DISCORD_TOKEN)
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if TOKEN:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ 啟動錯誤：{e}")
    else:
        print("❌ 錯誤：找不到 DISCORD_TOKEN，請檢查 Replit 的 Secrets 設定！")
# 0---------1---------2---------3---------4---------5---------6---------7---------8








