import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption
import json
import datetime
import os
from .saveedit_modals import ItemInputModal_Single
import sys
import BCSFE_Python_Discord as BCSFE_Python
from BCSFE_Python_Discord import *

async def main_cb(interaction: Interaction, save_stats, path):
	select = ui.Select(placeholder="에디터 메뉴 선택")
	select.add_option(label="세이브 관리",value="save_management",description="세이브 데이터를 관리합니다.")
	select.add_option(label="아이템",value="item",description="아이템을 에딧합니다.")
	select.add_option(label="가마토토/오토토",value="gm_ot",description="가마토토/오토토를 에딧합니다.")
	select.add_option(label="캐릭터",value="cats",description="캐릭터를 에딧합니다.")
	view=ui.View(timeout=300.0)
	view.add_item(select)
	
	async def main_cb_if(interaction: Interaction):
		await interaction.user.send(content=f"selected manu: {select.values[0]}\npath: {path}")
		if select.values[0] == "save_management":
			select1 = ui.Select(placeholder="세이브 관리 메뉴 선택")
			select1.add_option(label="세이브 저장 및 업로드", value="savenupload", description="세이브를 저장 후 업로드합니다.")
			view1 = ui.View(timeout=60.0)
			view1.add_item(select1)
			#await interaction.user.send(content="1분 안에 메뉴를 선택하세요.", view=view1)
			async def savemanage(interaction: Interaction):
				edits.save_management.save.save_save1(save_stats, path)
				save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
				save_data = BCSFE_Python.helper.write_save_data(
			        save_data, save_stats["version"], path, False
			    )
				upload_data = BCSFE_Python.server_handler.upload_handler(save_stats, path)
				transfer_code = upload_data['transferCode']
				confirmation_code = upload_data['pin']
				await interaction.user.send(content=f"기종변경 코드: {transfer_code}\n인증번호: {confirmation_code}\n이용해주셔서 감사합니다.")
			
			select1.callback=savemanage
			savemanagemsg = await interaction.user.send(view=view1)
		elif select.values[0] == "item":
			select1 = ui.Select(placeholder="아이템 메뉴 선택")
			select1.add_option(label="통조림", value="catfood", description="통조림")
			view1 = ui.View(timeout=300.0)
			view1.add_item(select1)
			#await interaction.user.send(content="메뉴를 선택하세요.", view=view1)
			async def itemshit(interaction: Interaction):
				if select1.values[0] == "catfood":
					await interaction.response.send_modal(modal=ItemInputModal_Single("통조림", save_stats, 45000))
				#save_stats["catfood"]["Value"] = 2101 test
				#await itemmsg.edit(content=f"통조림 테스트")
			
			select1.callback=itemshit
			itemmsg = await interaction.user.send(content="5분 안에 메뉴를 선택하세요.", view=view1)
	
	select.callback=main_cb_if
	mainmenumsg = await interaction.user.send(content="5분 안에 메뉴를 선택하세요.", view=view)

