import disnake

from datetime import datetime, timedelta

from disnake.ext import commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='ban', description='Забанить участника')
    async def ban(self, inter, участник: disnake.Member = commands.Param(description='Участник которого хотите забанить'), причина: str = commands.Param(description='Причина бана')):
        try:
            if участник.bot: return await inter.response.send_message('❌ Вы не можете заблокировать бота', ephemeral=True)
            if участник.id == inter.author.id: return await inter.response.send_message('❌ Вы не можете заблокировать самого себя', ephemeral=True)
            if inter.author.top_role.position <= участник.top_role.position: return await inter.response.send_message('❌ Вы не можете кикнуть участника с равной или более высокой ролью', ephemeral=True)
            embed = disnake.Embed(title='Блокирова')
            embed.add_field(name='Администратор: ', value=f"{inter.author.mention} - заблокировал")
            embed.add_field(name='Заюлокированный: ', value=участник.mention, inline=False)
            embed.add_field(name='Причина: ', value=f'`{причина}`')
            await участник.ban(reason=причина)
        except:
            await inter.response.send_message('❌ Вы не являетесь администратором', ephemeral=True)




def setup(bot):
    bot.add_cog(Ban(bot))