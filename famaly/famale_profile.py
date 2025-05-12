from typing import Self
import disnake

from disnake.ext import commands
from disnake import app_commands
from database.famaly import Famaly  


class FamilyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Famaly()

    async def get_family_names(self):
        """Асинхронно получаем список всех названий семей"""
        find_fam = self.db.find({})
        return [fam['fam_name'] for fam in find_fam] if find_fam else []

    @commands.slash_command(name='family-profile', description='Профиль семьи')
    async def fam_profile(
        self, 
        inter: disnake.ApplicationCommandInteraction,
        family_name: str = commands.Param(
            name="семьи",  # Только латиница и lowercase
            description="Название семьи"
        )
    ):
        """Просмотр профиля семьи"""
        find_fam = self.db.find_one({"fam_name": family_name})
        
        if not find_fam:
            await inter.response.send_message('Семья не найдена', ephemeral=True)
            return
            
        embed = disnake.Embed(title=f'Профиль семьи {family_name}')
        embed.add_field(name='Лидер', value=f'<@{find_fam.get("leader")}>', inline=False)
        embed.add_field(name='Членов', value=len(find_fam.get('members', [])), inline=False)
        embed.add_field(name='Роль', value=find_fam.get('role', 'Нет'), inline=False)
        await inter.response.send_message(embed=embed)

    @fam_profile.autocomplete("семьи")
    async def family_autocomplete(self, inter: disnake.ApplicationCommandInteraction, string: str):
        """Автодополнение для названий семей"""
        families = await self.get_family_names()
        return [name for name in families if string.lower() in name.lower()][:25]  # Ограничение 25 вариантов


def setup(bot):
    bot.add_cog(FamilyCog(bot))