import disnake

from disnake.ext import commands

from database.guild import Guild


class ProgressMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.slash_command(name='progress', description='Посмотреть достижение')
    async def progress(self, inter, участник: disnake.Member = None):
        

        embed = disnake.Embed(title='Достижения')
        embed.add_field(name='Пока', value="Нету")
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(ProgressMenu(bot))