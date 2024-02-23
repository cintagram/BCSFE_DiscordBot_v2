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

def serverpath(id: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), id))

def srvmemberpath(srvid: str, memid: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), srvid), memid))

async def bcedit(interaction: Interaction):
      pass

async def loadsave(interaction: Interaction, filepath):
      if os.stat(filepath).st_size == 0:
            await interaction.response.send_message(content="세이브파일이 유효하지 않습니다")
      else:
            data = helper.load_save_file(filepath)
            save_stats = data["save_stats"]
            save_data: bytes = data["save_data"]
            country_code = save_stats["version"]
            save_data = patcher.patch_save_data(save_data, country_code)
            save_stats = parse_save.start_parse(save_data, country_code)
            edits.save_management.save.save_save1(save_stats, filepath)
            await interaction.response.send_message(content="load complete")
      

class TCInputModal(ui.Modal):
            tccode = ui.TextInput(
                  label="기종변경 코드",
                  style=discord.TextStyle.short,
                  placeholder="기종변경코드 입력",
                  default=""
            )
            cccode = ui.TextInput(
                  label="인증번호",
                  style=discord.TextStyle.short,
                  placeholder="인증번호 입력",
                  default=""
            )
            gv_input = ui.TextInput(
                  label="게임버전",
                  style=discord.TextStyle.short,
                  placeholder="게임버전 | 예시: 13.0.0",
                  default=""
            )
            
            def __init__(self, country):
                  self.country = country
                  super().__init__(title="계정정보 입력")
            
            async def mainmenu_cb(self, interaction: Interaction):
                  if self.mainselect.values[0] == "save_management":
                        interaction.response.edit_message(content="save_management menu")
            
            async def on_submit(self, interaction: Interaction):
                  async def mainmenu_cb(self, interaction: Interaction):
                        if self.mainselect.values[0] == "save_management":
                              interaction.response.edit_message(content="save_management menu")
                  await interaction.response.send_message(content="DM을 확인해주세요.", ephemeral=True)
                  processingmsg = await interaction.user.send("세이브 데이터를 받아오는 중입니다.\n잠시만 기다려주세요.")
                  await processingmsg.delete()
                  userid = str(interaction.user.id)
                  serverid = str(interaction.guild_id)
                  if not os.path.exists(serverpath(serverid)):
                        os.mkdir(serverpath(serverid))
                  if not os.path.exists(srvmemberpath(serverid, userid)):
                        os.mkdir(srvmemberpath(serverid, userid))
                  now = datetime.datetime.now()
                  savetime = str(now).split(".")[0].replace(":", "-").replace(" ", "-")
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
                        self.save_stats = save_stats
                        select = ui.Select(placeholder="에디터 메뉴 선택")
                        select.add_option(label="세이브 관리",value="save_management",description="세이브 데이터를 관리합니다.")
                        select.add_option(label="아이템",value="item",description="아이템을 에딧합니다.")
                        select.add_option(label="가마토토/오토토",value="gm_ot",description="가마토토/오토토를 에딧합니다.")
                        select.add_option(label="캐릭터",value="cats",description="캐릭터를 에딧합니다.")
                        view=ui.View()
                        view.add_item(select)
                        self.mainselect = select
                        select.callback=mainmenu_cb
                        await interaction.user.send(content="메뉴를 선택하세요.", view=view) 
            
      
