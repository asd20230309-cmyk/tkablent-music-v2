# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord.ext import commands
from enum import Enum

# 1. 狀態與訊息定義 (參考並優化自 commit 64d2be3 的 LeaveType 邏輯)
class BotStatus(Enum):
    JOINED = "✅ | 已成功加入語音頻道，準備好為您播放音樂！"
    LEAVE_CMD = "📤 | 已根據指令退出頻道，下次見！"
    LEAVE_TIMEOUT = "🕗 | 因機器人已閒置過久，已自動退出以節省資源。"
    PAUSED = "⏸️ | 歌曲已暫停。"
    RESUMED = "▶️ | 歌曲已恢復播放。"

# 2. 機器人核心類別設定
class MyMusicBot(commands.Bot):
    def __init__(self):
        # 啟用 2026 年必備的權限 (Intents)
        intents = discord.Intents.default()
        intents.message_content = True  # 讓機器人讀懂 !join 等指令
        intents.voice_states = True     # 語音連線必備
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f"✅ 機器人 {self.user} 已成功上線並準備就緒！")

# 建立機器人實例
bot = MyMusicBot()

# --- 核心語音指令 ---

@bot.command()
async def join(ctx):
    """將機器人召喚至語音頻道"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        embed = discord.Embed(description=BotStatus.JOINED.value, color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ **操作失敗**：你必須先進入一個語音頻道！")

@bot.command()
async def leave(ctx):
    """讓機器人離開頻道 (包含 commit 64d2be3 的 UI 邏輯)"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        # 產生優雅的退出 Embed
        embed = discord.Embed(description=BotStatus.LEAVE_CMD.value, color=0x2b2d31)
        embed.set_footer(text=f"執行者: {ctx.author.display_name}")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ **操作失敗**：機器人目前不在任何語音頻道中。")

@bot.command()
async def pause(ctx):
    """暫停音樂 (優化了 commit 64d2be3 提到的 PAUSEFAIL 判斷)"""
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send(f"{BotStatus.PAUSED.value}")
    else:
        # 這裡修正了原文檔的邏輯錯誤，清楚提示失敗原因
        await ctx.send("❌ **無法暫停**：目前沒有音樂在播放，或歌曲已經是暫停狀態。")

@bot.command()
async def resume(ctx):
    """恢復播放"""
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send(f"{BotStatus.RESUMED.value}")
    else:
        await ctx.send("❌ **無法續播**：目前沒有被暫停的歌曲。")

# --- 啟動入口 ---
if __name__ == "__main__":
    # 重要：請將下方的引號內替換為你私下保存的 Token
    MY_TOKEN = "您的_TOKEN_貼在這裡"
    
    try:
        bot.run(MY_TOKEN)
    except discord.LoginFailure:
        print("❌ 錯誤：Token 無效，請檢查 Discord Developer Portal！")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
# 0---------1---------2---------3---------4---------5---------6---------7---------8


