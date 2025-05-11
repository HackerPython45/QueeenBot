import disnake

from disnake.ext import commands
from database.famaly import Famaly  # Убедитесь, что название файла и класса правильное

class FamProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Famaly()
        self.family_names = []  # Кэш для хранения названий семей

    async def update_family_cache(self):
        """Обновляет кэш с названиями семей"""
        families = await self.db.find({}, {"fam_name": 1}).to_list(None)
        self.family_names = [fam["fam_name"] for fam in families]

    @commands.slash_command(name='fam-profile', description='Профиль семьи')
    async def fam_prof(
        self,
        inter: disnake.ApplicationCommandInteraction,
        семья: str = commands.Param(
            name="семья",
            description="Выберите семью из списка",
            # Используем лямбду для доступа к self
            choices=lambda: [disnake.OptionChoice(name=name) for name in self.family_names]
        )
    ):
        """Обработчик команды профиля семьи"""
        fam_info = await self.db.find_one({"fam_name": семья})
        if not fam_info:
            return await inter.response.send_message("Семья не найдена!", ephemeral=True)
        
        embed = disnake.Embed(title=f"Профиль семьи {семья}")
        # Добавьте нужные поля в embed
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        """Обновляем кэш при запуске бота"""
        await self.update_family_cache()

def setup(bot):
    bot.add_cog(FamProfile(bot))