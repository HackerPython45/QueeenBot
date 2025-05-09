import disnake
import platform
import time
import pymongo

from disnake.ext import commands
from datetime import datetime


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()


    @commands.slash_command(name='info', description='Информация о боте')
    async def info(self, inter):
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]

        before = time.monotonic()
        await inter.response.defer()
        ping = round((time.monotonic() - before) * 1000)

        embed = disnake.Embed(title='Информация о боте')
        embed.add_field(name='> Основное', value=f"• Имя: `{self.bot.user.name}`\n"
                        f"• ID: `{self.bot.user.id}`\n"
                        f"• Создан: `{self.bot.user.created_at.strftime('%d.%m.%Y')}`\n"
                        f"• Префикс: `!`", inline=False)
        embed.add_field(name='> Техническое', value=f"• Язык: `Python {platform.python_version()}`\n"
                        f"• Библиотека: `Disnake: {disnake.__version__}\n`"
                        f"• База данных: `Pymongo: {pymongo.__version__}\n`"
                        f"• OC: `{platform.system()} {platform.release()}`\n"
                        f"• Пинг: `{ping}mc`",
                        inline=False)
        embed.add_field(name='> Статистика', value=f"• Серверов: `{len(self.bot.guilds)}`\n"
                        f"• Пользователей: `{len(self.bot.users)}`\n"
                        f"• Аптайм: `{uptime_str}`\n"
                        f"• [Сервер](https://discord.gg/BxV65djvMS)",
                        inline=False)
        embed.set_footer(text=f'Запрошено: {inter.author.name} * {datetime.now().strftime("%d.%d.%Y | %H:%M:%S")}', icon_url=inter.author.display_avatar.url)
        await inter.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))