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

def srvmemberpath(srvid: str, memid: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), srvid), memid))

def CatFoodEdit(save_stats, value, userid, srvid):
	save_stats["cat_food"]["Value"] = int(value)
	open(os.path.join(srvmemberpath(str(srvid), str(userid)), "save_json_temp.json"), "w+", encoding="utf-8").write(json.dumps(save_stats))
