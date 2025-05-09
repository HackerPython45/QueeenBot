import disnake

from disnake.ext import commands

from database.guild import Guild


class Unwarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()


    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='unwarn', description='Снять предупреждение')
    async def unwarn(self, inter, участник: disnake.Member = commands.Param(description='Выберите учасника'), причина: str = commands.Param(description='Укажите причину')):
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        users = guild_info['economy']['users']
        member = users.get(str(участник.id), {})
        if участник.bot: return await inter.response.send_message('Вы не можете снять warn боту', ephemeral=True)
        check_warn = self.db.get_warn(inter.guild.id, участник.id)
        if check_warn == 0: return await inter.response.send_message(f'{участник.mention} - у данного участника нету предупреждений', ephemeral=True)
        new_warn = check_warn - 1
        self.db.dell_warn(inter.guild.id, участник.id)
        embed = disnake.Embed(title='⚠️ Снятие warn')
        embed.add_field(name='Администратор: ', value=f'> {inter.author.mention}')
        embed.add_field(name='Снял учаснику: ', value=f'> {участник.mention}')
        embed.add_field(name='Причина: ', value=f'> `{причина}`', inline=False)
        embed.add_field(name='Кол-во (warn): ', value=f'⚠️ `{new_warn}`')
        await inter.response.send_message(embed=embed)

        embedm = disnake.Embed(title='Уведомление (warn)',
            description=f'Администратор: {inter.author.mention}, снял вам 1 предупреждение по причине: `{причина}`\n{new_warn}/4'                      
        )
        await участник.send(embed=embedm)

def setup(bot):
    bot.add_cog(Unwarn(bot))