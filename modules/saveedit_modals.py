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

class ItemInputModal_Single(ui.Modal):
            def __init__(self, itemname, currentvalue, maxvalue):
				self.itemname = itemname
				self.cv = currentvalue
				self.mv = maxvalue
				super().__init__(title="값 입력")
				self.inputvalue = ui.TextInput(
					label=f"{self.itemname} 값 입력",
					style=discord.TextStyle.short,
					placeholder=f"현재값: {self.cv} | 최댓값: {self.mv}",
					default=""
				)
            async def mainmenu_cb(self, interaction: Interaction):
                  if self.mainselect.values[0] == "save_management":
                        interaction.response.edit_message(content="save_management menu")
            
            async def on_submit(self, interaction: Interaction):
                  async def mainmenu_cb(self, interaction: Interaction):
                        if self.mainselect.values[0] == "save_management":
                              interaction.response.edit_message(content="save_management menu")
                  #await interaction.response.send_message(content="DM을 확인해주세요.", ephemeral=True)
                  processingmsg = await interaction.user.send("세이브 데이터를 받아오는 중입니다.\n잠시만 기다려주세요.")
                  await processingmsg.delete()
                  userid = str(interaction.user.id)
                  serverid = str(interaction.guild_id)
                  if not os.path.exists(srvmemberpath(serverid, userid)):
                        os.mkdir(srvmemberpath(serverid, userid))
                        with open(os.path.join(srvmemberpath(serverid, userid), "usrinfo.csv"), "w+", encoding="utf-8") as infowrite:
                              infowrite.write(makeinfo(userid))
                  now = datetime.datetime.now()
                  savetime = str(now).split(".")[0].replace(":", "_").replace(" ", "_")
                  savefile = "SD_{}".format(savetime)
                  path = os.path.join(srvmemberpath(serverid, userid), savefile)
                  country_code = self.country
                  transfer_code = self.tccode.value
                  confirmation_code = self.cccode.value
                  game_version = self.gv_input.value
                  game_version = helper.str_to_gv(game_version)
                  save_data = BCSFE_Python.server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)
                  save_data = patcher.patch_save_data(save_data, country_code)
                  
                  save_stats = parse_save.start_parse(save_data, country_code)
                  if save_stats == 0:
                        await interaction.user.send("입력한 정보가 잘못되었습니다.")
                  elif save_stats != 0:
                        edits.save_management.save.save_save1(save_stats, path)
                        await saveedit.main_cb(interaction, save_stats, path)
