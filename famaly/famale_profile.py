import disnake

from disnake.ext import commands
from database.famaly import Famaly

class FamProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Famaly()

    async def update_family_names(self):
        """Обновляем кэш названий семей"""
        self._family_names = await self.get_family_names()

    @commands.slash_command(name='fam-profile', description='Профиль семьи')
    async def fam_prof(
        self,
        inter: disnake.ApplicationCommandInteraction,
        семья: str = commands.Param(
            name="семья",
            description="Выберите семью из списка",
            choices=lambda: [disnake.OptionChoice(name=name) for name in self._family_names]
        )
    ):
        """Обработчик команды /fam-profile"""
        fam_info = await self.db.find_one({"fam_name": семья})
        if not fam_info:
            return await inter.response.send_message("Семья не найдена!", ephemeral=True)
        
        # Создаем embed с информацией о семье
        embed = disnake.Embed(title=f"Профиль семьи {семья}")
        # Добавляем остальные поля...
        
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(FamProfile(bot))