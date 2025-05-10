import disnake

from disnake.ext import commands

from database.guild import Guild


class CreateProgress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='manager-progress-create', description='Создать новое достижение')
    async def manager_progress_create(self, inter, название: str = commands.Param(description='Введите название')):
        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        try: 
            embed = disnake.Embed(title='Новое достижение', description=f'Вы создали новое достижение -> {название}')
            self.db.create_to_progress_guild(inter.guild.id, название)
            print(f'Успешно создано новое достижение -> {название}')
            await inter.response.send_message(embed=embed, ephemeral=True)
        except:
            print('Ошибка')




def setup(bot):
    bot.add_cog(CreateProgress(bot))