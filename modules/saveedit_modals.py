import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption
import json
import datetime
import os
from . import saveeditapi
import sys
import BCSFE_Python_Discord as BCSFE_Python
from BCSFE_Python_Discord import *

class ItemInputModal_Single(ui.Modal):
    inputvalue = ui.TextInput(label=f"{itemname} 값 입력", style=discord.TextStyle.short, placeholder=f"현재값: {self.cv['cat_food']['Value']} | 최댓값: {self.mv}", default="")
    def __init__(self, itemname, currentvalue, maxvalue, save_stats):
        self.itemname = itemname
        self.cv = currentvalue
        self.mv = maxvalue
        self.sv = save_stats
        super().__init__(title="값 입력")
        
    async def on_submit(self, interaction: Interaction):
        saveeditapi.CatFoodEdit(self.sv, self.inputvalue.value)
        await interaction.user.send(content=f"Set CF to {self.inputvalue}")
