import disnake

from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='help', description='Помощь по командам')
    async def help(self, inter):
        embed = disnake.Embed(title='Информация по командам')
        embed.add_field(name='💰 | Экономика', value=f'</profile:1368622931252350988> - Посмотреть профиль\n </bank:1368622931252350989> - Положить на банковский счет\n</pay:1368622931252350990> - Передать участнику денег\n</timely:1368622931252350991> - Получить ежедневную награду\n</work:1368622931252350992> - Работа')
        embed.add_field(name='🛡️ | Для администрации', value=f'</ban:1368622931797737482> - Забанить пользователя\n</unban:1368622931797737483> - Разбанить пользователя\n</kick:1368622931797737484> - Выгнать участника\n</warn:1368622931797737485> - Выдать предупреждение\n</unwarn:1368622931797737486> - Снять предупреждение\n</add_meney:1368622931797737488> - Выдать деньги\n</remove-money:1368622931797737489> - Забрать деньги\n</system-ticket> - Система тикетов (доступно только создателю) (В разработке)\n</antibot-enable:1369734837312815186> - Включить систему Анти-Бота\n</antibot-disable:1369722879356305541> - Выключить систему Анти-Бота\n'
                        f'</antilink-enable:1369733203434274958> - Включить систему Анти-Линк\n</antilink-disable:1369733203434274959> - Выключить систему Анти-Линк'
                        , inline=False)
        embed.add_field(name='💡 | Другое', value=f'</offers:1368622931252350994> - Предложить идею об улучшение\n</info:1368622931252350996> - Информация о боте', inline=False)
        embed.add_field(name='🎫 | Подписка premiun', value='В разработке. Тут будет список команда с premium подпиской', inline=False)
        embed.set_footer(text=f"{self.bot.user.name} - Кол-во команд 14", icon_url=self.bot.user.display_avatar.url)
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))