import disnake 
import asyncio

from datetime import datetime
from disnake.ext import commands

from database.guild import Guild


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if not member.bot or member.id == self.bot.user.id:
            return
        guild_info = self.db.find_one({"guild_id": member.guild.id})
        settings_info = guild_info['settings']
        if settings_info.get('welcome_channel_id', 1):
            find_channel = member.guild.get_channel(settings_info.get('welcome_channel_id', 1))
            embed = disnake.Embed(title='Приветствие')
            embed.add_field(name='Зашел ', value=f'{member.name} | {member.mention}', inline=False)
            embed.add_field(name='Время', value=f'Дата: {datetime.now().strftime("%Y.%m.%d | %H:%M:%S")}', inline=False)
            await find_channel.send(embed=embed)
        else:
            pass
    


def setup(bot):
    bot.add_cog(Welcome(bot))