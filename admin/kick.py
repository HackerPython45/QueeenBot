import disnake

from disnake.ext import commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='kick', description='Выгнать пользователя')
    async def kick(self, inter, участник: disnake.Member = commands.Param(description='Участник'), причина: str = commands.Param(description='Причина')):
        if участник.bot: return await inter.response.send_message(f'Вы не можете кикнуть бота', ephemeral=True)
        if участник.id == inter.author.id: return await inter.response.send_message('Вы не можете заблокировать самого себя', ephemeral=True)
        if inter.author.has_permissions.administrator:
            embed = disnake.Embed(title='KICK')
            embed.add_field(name='Администратор: ', value=f'> {inter.author.mention}', inline=False)
            embed.add_field(name='Кикнутый: ', value=f'> {участник.mention}')
            embed.add_field(name='Причина: ', value=f'> `{причина}`')
            await участник.kick(reason=причина)
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message('Вы не являетесь администратором', ephemeral=True)

def setup(bot):
    bot.add_cog(Kick(bot))