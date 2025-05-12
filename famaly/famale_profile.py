import disnake

from disnake.ext import commands
from database.famaly import Famaly  # Убедитесь, что название файла и класса правильное

class FamProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Famaly()

    @commands.slash_command(name="fam-profile", description="Профиль семьи")
    async def fam_prof(
        self,
        inter: disnake.ApplicationCommandInteraction,
        семья: str = commands.Param(
            name="семья",
            description="Выберите семью из списка",
            autocomplete=True  # Включаем автодополнение
        )
    ):
        await inter.response.send_message(f"Профиль семьи: **{семья}**")

    # Автодополнение для параметра "семья" (динамическая загрузка из MongoDB)
    @fam_prof.autocomplete("семья")
    async def family_autocomplete(
        self,
        inter: disnake.ApplicationCommandInteraction,
        query: str
    ) -> list[disnake.app_commands.Choice]:
        # Получаем семьи из MongoDB (ищем по частичному совпадению)
        families = await self.db.families.find(
            {"fam_name": {"$regex": f".*{query}.*", "$options": "i"}}
        ).to_list(length=25)
        
        return [
            disnake.app_commands.Choice(name=family["fam_name"], value=family["fam_name"])
            for family in families
        ]
        fam_info = await self.db.find_one({"fam_name": семья})
        if not fam_info:
            return await inter.response.send_message("Семья не найдена!", ephemeral=True)
        
        embed = disnake.Embed(title=f"Профиль семьи {семья}")
        # Добавьте нужные поля в embed
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(FamProfile(bot))