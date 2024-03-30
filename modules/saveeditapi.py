import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption
import json
import datetime
import os
import sys
import BCSFE_Python_Discord as BCSFE_Python
from BCSFE_Python_Discord import *

def CatFoodEdit(save_stats, value):
	save_stats["cat_food"]["Value"] = value
