import disnake

from disnake.ext import commands

from database.guild import Guild


class SetReputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()


    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='set-reputations', description='Выдать репутацию')
    async def set_rep(self, inter, участник: disnake.Member = commands.Param(description='Выберите участника'), сколько: str = commands.Param(description='Сколько выдать')):
        guild_info = self.db.find_one({"guil_id": inter.guild.id})
        if int(сколько) <= 0: return await inter.response.send_message('Вы не можете выдать 0 или меньше 0 репутации', ephemeral=True)

        self.db.set_give_reputation_user(inter.guild.id, участник.id, int(сколько))
        await inter.response.send_message(f'**Репутация** ({сколько}) было устоновлено {участник.mention}', ephemeral=True)



def setup(bot):
    bot.add_cog(SetReputation(bot))