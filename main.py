# 0---------1---------2---------3---------4---------5---------6---------7---------8
import discord
from discord.ext import commands

# 這裡整合了我們之前討論的所有優化邏輯
class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f"✅ 機器人 {self.user} 已成功上線！")

    # 優化後的動態狀態訊息
    def get_status_embed(self, reason: str, user: discord.Member = None):
        mapping = {
            "timeout": "| 因機器人已閒置過久，自動退出頻道",
            "command": "| 已離開語音/舞台頻道",
            "finish": "| 歌曲已全部播放完畢"
        }
        text = mapping.get(reason, "播放結束")
        embed = discord.Embed(description=text, color=0x2b2d31)
        if user:
            embed.set_footer(text=f"操作者: {user.display_name}")
        return embed

# 提醒：啟動需要 Token，我們下一步會處理
# bot = MusicBot()
# bot.run("YOUR_TOKEN_HERE")
# 0---------1---------2---------3---------4---------5---------6---------7---------8
