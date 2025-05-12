import disnake

from disnake.ext import commands
from disnake import app_commands
from database.famaly import Famaly  # Убедитесь, что название файла и класса правильное

class FamilyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Famaly()
    
    # Autocomplete для выбора семьи
    async def family_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        # Ищем семьи, которые начинаются с введенного текста
        family_names = self.db.find(
            {"fam_name": {"$regex": f"^{current}", "$options": "i"}},
            {"fam_name": 1}
        ).limit(25)
        
        return [
            app_commands.Choice(name=family["fam_name"], value=family["fam_name"])
            for family in family_names
        ]
    
    # Команда family-profile
    @app_commands.command(
        name="family-profile",
        description="Просмотр профиля семьи"
    )
    @app_commands.autocomplete(family=family_autocomplete)
    @app_commands.describe(family="Выберите семью для просмотра")
    async def family_profile(
        self, 
        interaction: disnake.Interaction, 
        family: str
    ):
        # Получаем данные о семье из базы данных
        family_data = self.db.find_one({"fam_name": family})
        
        if not family_data:
            await interaction.response.send_message(
                "Семья не найдена!",
                ephemeral=True
            )
            return
        
        # Создаем embed с информацией о семье
        embed = disnake.Embed(
            title=f"Профиль семьи {family_data['name']}",
            color=disnake.Color.blurple()
        )
        
        # Добавляем информацию в embed
        embed.add_field(name="Основатель", value=f"<@{family_data['founder_id']}>")
        embed.add_field(name="Участники", value=str(len(family_data['members'])))
        embed.add_field(name="Дата создания", value=family_data['created_at'].strftime("%d.%m.%Y"))
        
        # Отправляем embed
        await interaction.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(Famaly(bot))