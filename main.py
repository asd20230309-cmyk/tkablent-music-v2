# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord import app_commands
from discord.ext import commands
from enum import Enum
import os

# 1. 狀態與訊息定義
class BotStatus(Enum):
    JOINED = "✅ | 已成功加入語音頻道，準備好為您播放音樂！"
    LEAVE_CMD = "📤 | 已根據指令退出頻道，下次見！"
    PAUSED = "⏸️ | 歌曲已暫停。"
    RESUMED = "▶️ | 歌曲已恢復播放。"

# 2. 機器人核心類別設定 (整合斜線指令同步功能)
class MyMusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 這會將斜線指令同步到 Discord
        await self.tree.sync()
        print(f"✅ 已同步斜線指令到所有伺服器")

    async def on_ready(self):
        print(f"✅ 機器人 {self.user} 已成功上線！")

bot = MyMusicBot()

# --- 斜線指令部分 (Slash Commands) ---

@bot.tree.command(name="join", description="將機器人召喚至您所在的語音頻道")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        embed = discord.Embed(description=BotStatus.JOINED.value, color=0x2b2d31)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ 你必須先進入一個語音頻道！", ephemeral=True)

@bot.tree.command(name="leave", description="讓機器人離開當前語音頻道")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        embed = discord.Embed(description=BotStatus.LEAVE_CMD.value, color=0x2b2d31)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ 機器人目前不在任何語音頻道中。", ephemeral=True)

@bot.tree.command(name="pause", description="暫停目前播放的音樂")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message(BotStatus.PAUSED.value)
    else:
        await interaction.response.send_message("❌ 無法暫停：目前沒有音樂在播放或已暫停。", ephemeral=True)

@bot.tree.command(name="resume", description="恢復播放暫停中的音樂")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message(BotStatus.RESUMED.value)
    else:
        await interaction.response.send_message("❌ 無法續播：目前沒有被暫停的歌曲。", ephemeral=True)

# --- 啟動入口 ---
# 請在 Replit 的 Secrets 中設定 DISCORD_TOKEN
if __name__ == "MTQ2NDcwMDE4MDg2MjYwMzI2NA.G3r5gj.HsF5ZHtabgjYaTKcFtHqCu32nYH1Dv3Lt6PSoY":
    TOKEN = os.getenv("DISCORD_TOKEN") or "您的_TOKEN_貼在這裡"
    bot.run(TOKEN)
# 0---------1---------2---------3---------4---------5---------6---------7---------8



