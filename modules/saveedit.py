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

async def main_cb(interaction: Interaction, save_stats, path):
	select = ui.Select(placeholder="에디터 메뉴 선택")
	select.add_option(label="세이브 관리",value="save_management",description="세이브 데이터를 관리합니다.")
	select.add_option(label="아이템",value="item",description="아이템을 에딧합니다.")
	select.add_option(label="가마토토/오토토",value="gm_ot",description="가마토토/오토토를 에딧합니다.")
	select.add_option(label="캐릭터",value="cats",description="캐릭터를 에딧합니다.")
	view=ui.View()
	view.add_item(select)
	
	async def main_cb_if(interaction: Interaction):
		await interaction.user.send(content=f"selected manu: {select.values[0]}\npath: {path}")
		if select.values[0] == "save_management":
			select1 = ui.Select(placeholder="세이브 관리 메뉴 선택")
			select.add_option(label="세이브 저장 및 업로드", value="savenupload", description="세이브를 저장 후 업로드합니다.")
			view1 = ui.View()
			view1.add_item(select1)
			
			async def savemanage(interaction: Interaction):
				edits.save_management.save.save_save1(save_stats, path)
				save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
				save_data = BCSFE_Python.helper.write_save_data(
			        save_data, save_stats["version"], path, False
			    )
				upload_data = BCSFE_Python.server_handler.upload_handler(save_stats, path)
				transfer_code = upload_data['transferCode']
				confirmation_code = upload_data['pin']
				await savemanagemsg.edit(content=f"기종변경 코드: {transfer_code}\n인증번호: {confirmation_code}")
			
			select1.callback=savemanage
			savemanagemsg = await mainmenumsg.edit(view=view1)
	
	select.callback=main_cb_if
	mainmenumsg = await interaction.user.send(content="메뉴를 선택하세요.", view=view)

