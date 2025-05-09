import disnake
import asyncio

from disnake.ext import commands

from database.guild import Guild

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()


    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='warn', description='Выдать предупреждение пользователю')
    async def warn(self, inter, участник: disnake.Member = commands.Param(description='Участник'), причина: str = commands.Param(description='Причина')):
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        users = guild_info['economy']['users']
        member = users.get(str(участник.id), {})
        if участник.bot: return await inter.response.send_message('Вы не можете выдать warn боту', ephemeral=True)
        if inter.author.guild_permissions.administrator:
            check_warn = self.db.get_warn(inter.guild.id, участник.id)
            new_warn = check_warn + 1
            self.db.set_warn(inter.guild.id, участник.id)
            embed = disnake.Embed(title='Предупреждение', description='Данный пользователь получил предупреждение')
            embed.add_field(name='Администратор: ', value=f'> {inter.author.mention}')
            embed.add_field(name='Нарушитель: ', value=f'> {участник.mention}')
            embed.add_field(name='Причина: ', value=f'`{причина}`', inline=False)
            embed.add_field(name='Кол-во предупреждений: ', value=f'`{new_warn}`/4', inline=False)

            await inter.response.send_message(embed=embed)

        

        if new_warn == 3:
            embed = disnake.Embed(title='Уведомление',
                description=f'У вас на данный момент 3/3 предупреждений, свяжитесь с администрацией что бы снять 1 пред и наче вы будете кикнуты с сервера {inter.guild.name}'
            )
            await участник.send(embed=embed)
        if new_warn == 4:
            await участник.kick(reason='4/4 warn')


def setup(bot):
    bot.add_cog(Warn(bot))