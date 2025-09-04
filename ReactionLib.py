import discord
from discord.ext import commands
from discord import app_commands, Interaction, ui
from reactions import reaction_data

class ReactionSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=key.replace("_", " ").title(), value=key)
            for key in reaction_data
        ]
        super().__init__(placeholder="Choose a reaction :) ", min_values=1, max_values=1, options=options)
        self.selected_value = None

    async def callback(self, interaction: Interaction):
        self.selected_value = self.values[0]
        await interaction.response.defer()

class SendReactionButton(ui.Button):
    def __init__(self, select: ReactionSelect):
        super().__init__(label="Send", style=discord.ButtonStyle.blurple)
        self.select = select

    async def callback(self, interaction: Interaction):
        stamp = self.select.selected_value
        if not stamp:
            await interaction.response.send_message("you havnt picked anything dw", ephemeral=True)
            return
        
        url = reaction_data.get(stamp)
        if url:
            embed = discord.Embed(color=discord.Color.random())
            embed.set_image(url=url)
            embed.set_footer(text=f"{interaction.user.display_name} reaction was {stamp.replace('_', ' ').title()}")
            #ye {stamp.replace('_', ' ').title()} was meant for stamp name incase i forgot
            await interaction.channel.send(embed=embed)
            await interaction.message.delete()
        else:
            await interaction.response.send_message("What did you pick?, it is invalid", ephemeral=True)

class ReactionMenu(ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.user = user
        self.select = ReactionSelect()
        self.add_item(self.select)
        self.add_item(SendReactionButton(self.select))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("This menu aint for you dwg", ephemeral=True)
            return False
        return True

class ReactionMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="get-reaction", description="Pick and send a PJSK reaction")
    async def get_reaction(self, interaction: Interaction):
        view = ReactionMenu(user=interaction.user)
        await interaction.response.send_message("Choose a reaction", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReactionMenuCog(bot))
