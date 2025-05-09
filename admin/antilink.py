import disnake
import asyncio

from disnake.ext import commands
from datetime import datetime

from database.guild import Guild

black_list = ['discord.gift', 'discordapp.gift', 'discordnitro.com', 'discord-nitro.com', 'steamcommumity.com', 'steamcomunnity.com', 'free-nitro.ru',
'discord.freegift.ru', 'claim-discord.com', 'discordl.com', 'dlscord.com', 'dicsord-nitro.xyz', 'discrod-gift.site', 'gift-steam.com', 'steamwallet.com', 'freegiftcodes.com',
'bit.ly', 'tinyurl.com', 'cutt.ly', 'shorturl.at', 'goo.gl', 'ow.ly', 'is.gd', 'adf.ly', 'mediafire.com', 'mega.nz', 'dropbox.com', 'anonfiles.com', 'zippyshare.com', 'uploaded.net',
'discord.gg', '/discord.gg', 'discord.gg/'
]

class AntiLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        guild_info = self.db.find_one({'guild_id': message.guild.id})
        settings_info = guild_info['settings']
        if settings_info.get('antilink', 0) == 1:
            for word in message.content.split():
                if any(domain in word.lower() for domain in black_list):
                    await message.delete()
                    embed = disnake.Embed(title='Система Анти-Линк')
                    embed.add_field(name='Отправил: ', value=f'{message.author.mention}', inline=False)
                    embed.add_field(name='Ссылка: ', value=f'`{word}`', inline=False)
                    embed.add_field(name='Дата:', value=f'{datetime.now().strftime("%Y.%m.%d | %H:%M:%S")}', inline=False)
                    find_channel = message.guild.get_channel(settings_info.get('channel_id_message', 1))
                    await find_channel.send(embed=embed)
        else:
            pass

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(AntiLink(bot))