# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord.ext import commands
from enum import Enum

# 1. 狀態定義 (優化 commit 64d2be3 中的 LeaveType 與訊息邏輯)
class BotStatus(Enum):
    JOINED = "✅ | 已成功加入語音頻道"
    LEAVE_CMD = "📤 | 已根據指令退出頻道"
    LEAVE_TIMEOUT = "🕗 | 因機器人已閒置 10 分鐘，已自動退出"
    PLAYING = "🎵 | 正在播放歌曲"
    PAUSED = "⏸️ | 歌曲已暫停"

# 2. 機器人核心類別
class MyMusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # 2026 年必備權限
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f"✅ 機器人 {self.user.name} 已上線")

# 實作機器人實例
bot = MyMusicBot()

# --- 語音指令部分 ---

@bot.command()
async def join(ctx):
    """將機器人加入語音頻道"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        # 使用優化後的 Embed 顯示狀態
        embed = discord.Embed(description=BotStatus.JOINED.value, color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ 你必須先加入一個語音頻道！")

@bot.command()
async def leave(ctx):
    """使機器人離開語音頻道 (參考 commit 64d2be3 優化)"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        # 顯示由指令退出的訊息
        embed = discord.Embed(description=BotStatus.LEAVE_CMD.value, color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ 機器人目前不在任何語音頻道中。")

@bot.command()
async def pause(ctx):
    """暫停音樂 (修正 commit 64d2be3 中的報錯邏輯)"""
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        embed = discord.Embed(description=BotStatus.PAUSED.value, color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        # 修正後的錯誤提示：確保當前是否已處於暫停狀態
        await ctx.send("❌ 無法暫停：目前沒有音樂在播放，或歌曲已處於暫停狀態。")

@bot.command()
async def resume(ctx):
    """續播音樂"""
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ | 歌曲已恢復播放")
    else:
        await ctx.send("❌ 無法續播：目前沒有被暫停的歌曲。")

# 這裡填入你的 Token
# bot.run("YOUR_TOKEN_HERE")
# 0---------1---------2---------3---------4---------5---------6---------7---------8

