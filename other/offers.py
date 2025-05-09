import disnake 

from disnake.ext import commands
from datetime import datetime, timedelta

class Offers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='offers', description='Предложить идею для бота разрабодчику')
    async def offers(self, inter, текст: str = commands.Param(description='Опишите свою идею')):
        guild_developer = self.bot.get_guild(1367450430124195900)
        channel = guild_developer.get_channel(1368264811984715877)

        embed = disnake.Embed(title='Новое предложение')
        embed.add_field(name='Отправитель: ', value=f'{inter.author.mention}')
        embed.add_field(name='', value=f'Сервер: {inter.guild.name}')
        embed.add_field(name='', value=f'```{текст}```', inline=False)
        await channel.send(embed=embed)
        await inter.response.send_message('Вы успешно отправили предложения об улучшение', ephemeral=True)


def setup(bot):
    bot.add_cog(Offers(bot))