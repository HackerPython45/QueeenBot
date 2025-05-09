import disnake

from datetime import datetime, timedelta

from disnake.ext import commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='ban', description='Забанить участника')
    async def ban(self, inter, участник: disnake.Member = commands.Param(description='Участник которого хотите забанить'), причина: str = commands.Param(description='Причина бана')):
        if участник.bot: return await inter.response.send_message('Вы не можете заблокировать бота', ephemeral=True)
        if участник.id == inter.author.id: return await inter.response.send_message('Вы не можете заблокировать самого себя', ephemeral=True)
        if inter.author.guild_permissions.administrator:
            embed = disnake.Embed(title='Блокирова')
            embed.add_field(name='Администратор: ', value=f"{inter.author.mention} - заблокировал")
            embed.add_field(name='Заюлокированный: ', value=участник.mention, inline=False)
            embed.add_field(name='Причина: ', value=f'`{причина}`')
            await участник.ban(reason=причина)
        else:
            await inter.response.send_message('Вы не admin', ephemeral=True)



def setup(bot):
    bot.add_cog(Ban(bot))