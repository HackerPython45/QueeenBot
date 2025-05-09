import disnake

from disnake.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='unban', description='Разбанить участника')
    async def unban(self, inter, участник: disnake.Member = commands.Param(description='Выберите участника'), причина: str = commands.Param(description='Укажите причину')):
        await участник.unban(reason=причина)
        await inter.response.send_message(f'Вы успешно разбанили - {участник.mention}', ephemeral=True)

def setup(bot):
    bot.add_cog(Unban(bot))