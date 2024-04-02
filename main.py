import discord
from discord.ext import commands
from discord.ui import Button, TextInput
from discord import app_commands,Interaction,ui,ButtonStyle,SelectOption, SyncWebhook
import json
import os
from enum import Enum
import sys
import numpy
import pandas as pd
import csv
from os import walk
from modules import *
from modules.modalclass import TCInputModal, loadsave, makeinfo

class CashUse(Enum):
  활성화="True"
  비활성화="False"
  
async def SendDisallowedMsg(interaction: Interaction):
  embed = discord.Embed(title="사용금지됨", description="서버가 봇 개발자에 의해 사용금지처리되었습니다.\n개발자에게 문의해주새요.")
  await interaction.response.send_message(embed=embed)

def serverpath(id: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), id))

def srvmemberpath(srvid: str, memid: str):
      return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers"), srvid), memid))

def loadsrvset_all():
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj
  
def savesrvset_all(data):
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(data))

def loadsrvset(srvid: str):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  return setobj[srvid]
  
def savesrvset(srvid: str, newset):
  with open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "r", encoding="utf-8") as setreader:
    setreader_str = setreader.read()
  setobj = json.loads(setreader_str)
  setobj[srvid] = newset
  open(os.path.join(os.path.join(os.path.curdir, "modules"), "serversettings.json"), "w+", encoding="utf-8").write(json.dumps(setobj))
  
def chksrvallowed(id: str):
  set = loadsrvset(id)
  if set["UsingAllowed"] == "True":
    return True
  else:
    return False

class MyClient(discord.Client):
  async def on_ready(self):
    await self.wait_until_ready()
    await tree.sync()
    if not os.path.exists(os.path.abspath(os.path.join(os.path.curdir, "bc_saves"))):
      os.mkdir(os.path.abspath(os.path.join(os.path.curdir, "bc_saves")))
      os.mkdir(os.path.abspath(os.path.join(os.path.join(os.path.curdir, "bc_saves"), "servers")))
    print(f"{self.user} 에 로그인하였습니다!")
intents= discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name='명령어', description="명령어 리스트")
async def CommandHelp(interaction: Interaction):
	text_title = "냥코에딧봇 v2"
	text_dev = "Developed by PULSErvice"
	text_body = """
`서버등록`: [필수] 서버를 봇 시스템에 등록합니다.
`sendb`: [관리자] 에딧시작 버튼을 보냅니다. 버판기처럼 사용합니다.
`정보`: 봇에 등록된 유저의 정보를 확인합니다.
`가입`: [필수] 유저가 봇 시스템에 가입합니다.
`유저서버밴`: [관리자] 유저가 서버에서 봇사용하는것을 금지시킵니다.
`유저서버밴해제`: [관리자] 유저가 서버애서 봇사용하는것을 허용합니다.
`재화사용`: [관리자] 서버에서 에딧할때의 재화(사용료)를 사용|비사용 설정합니다.
`재화이름`: [관리자] 서버재화시스템의 재화의 이름을 설정합니다.
`재화가격`: [관리자] 서버재화시스템의 1회 에딧가격을 설정합니다.
`구매로그설정`: [관리자] 유저가 에딧시 구매로그 또는 이용로그를 웹후크로 보냅니다.
"""
	embed = discord.Embed(title=text_title, description=text_body)
	embed.set_footer(text=text_dev)
	await interaction.response.send_message(embed=embed)

@tree.command(name="sendb", description="에딧시작 버튼을 보냅니다.")
@app_commands.checks.has_permissions(administrator=True)
async def sendbtn(interaction:Interaction):
  button = ui.Button(style=ButtonStyle.green,label="에딧시작",disabled=False)
  view = ui.View(timeout=None)
  view.add_item(button)
  embed = discord.Embed(title="냥코대전쟁 세이브 에딧봇 v2", description="아래 버튼을 눌러 에딧을 시작하세요.").set_footer(text="Developed by PULSErvice")
  async def loadfile_cb(interaction:Interaction):
    select = ui.Select(placeholder="세이브파일 선택")
    userid = str(interaction.user.id)
    serverid = str(interaction.guild_id)
    mypath = srvmemberpath(serverid, userid)
    i = -1
    num = 0
    filelist = ""
    text = ""
    filenames=os.listdir(mypath)
    filenamesnum=len(filenames)
    print(filenamesnum)
    k = False
    while i <= filenamesnum:
      i += 1
      if i == filenamesnum or filenames[i] == None:
        print("i is None")
        text1 = "현재 서버에서 저장한 세이브파일이 없습니다."
        #select.add_option(label=text1, value=str(i+1), description="기능사용불가")
        break
      else:
        if not filenames[i] == "userdata.csv":
          text1 = str(i+1) + ". " + filenames[i] + "\n"
          k = True
          select.add_option(label=text1, value=str(i+1), description="세이브 파일입니다.")
    view = ui.View()
    view.add_item(select)
    if k:
    	await interaction.response.send_message(ephemeral=True, view=view, delete_after=120.0, content="2분 안에 파일을 선택해주세요.")
    else:
      await interaction.response.send_message(ephemeral=True, content=text1, delete_after=30.0)
    async def loadfile_select_cb(interaction:Interaction):
      filenum = int(select.values[0])
      selectedfile = filenames[filenum-1]
      savefilepath = os.path.join(mypath, selectedfile)
      await loadsave(interaction, savefilepath, interaction.guild_id)
    select.callback=loadfile_select_cb

  async def button_callback(interaction:Interaction):
    set = loadsrvset(str(interaction.guild_id))
    if not chksrvallowed(str(interaction.guild_id)):
      await SendDisallowedMsg(interaction)
    else:
      usr = int(interaction.user.id)
      userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
      if not os.path.exists(userpath):
        embed = discord.Embed(title="처리불가", description="서버DB에 가입되지 않은 사용자입니다.\n</가입:123> 명령어로 가입 후 사용해주세요.")
        await interaction.response.send_message(embed=embed)
      else:
        df = pd.read_csv(userpath, sep=",")
        if df["IsBanned"].values[0] == True:
          embed = discord.Embed(title="기능 사용 불가", description="서버 관리자에 의해 사용이 차단된 사용자입니다.\n서버 관리자에게 문의해주세요.")
          await interaction.response.send_message(embed=embed)
        else:
          if set["CashSystemSetting"]["Use"] == "True":
            if set["CashSystemSetting"]["CashName"] == "undefined":
              cashname = "재화"
            else:
              cashname = set["CashSystemSetting"]["CashName"]
            price = int(set["CashSystemSetting"]["PricePerUse"])
            usr = int(interaction.user.id)
            userpath = os.path.join(srvmemberpath(str(interaction.guild_id), str(usr)), "userdata.csv")
            df = pd.read_csv(userpath, sep=",")
            if df["IsBanned"].values[0] == True:
              embed = discord.Embed(title="기능 사용 불가", description="서버 관리자에 의해 사용이 차단된 사용자입니다.\n서버 관리자에게 문의해주세요.")
              await interaction.response.send_message(embed=embed)
            else:
              usrbalance = df.loc[df["UserId"] == usr, "CashAmount"].values[0]
              if usrbalance < price:
                await interaction.response.send_message(content=f"{cashname} 이(가) 부족합니다.", ephemeral=True)
              else:
                df.loc[df["UserId"] == usr, "CashAmount"] -= price
                df.to_csv(userpath, index=None)
                if set["NoticeWebhook"] != "undefined":
                	webhookobj = SyncWebhook.from_url(set["NoticeWebhook"])
                	embed1 = discord.Embed(title="💜 구매로그", description=f"{interaction.user.mention}님이 {price}{cashname}을(를) 사용하여 에딧하셨습니다! 💜")
                	webhookobj.send(embed=embed1, username="BC EDITBOT v2", avatar_url="https://i.imgur.com/8GnT3ZH.png")
            typeselect = ui.Select(placeholder="메뉴를 선택해주세요.")
            typeselect.add_option(label="기종변경 코드로 시작", value="tc", description="기종변경 코드로 에딧을 시작합니다.")
            typeselect.add_option(label="기존 파일로 시작", value="lf", description="기존 파일로 에딧을 시작합니다.")
            view_m = ui.View()
            view_m.add_item(typeselect)
            async def type_cb(interaction: Interaction):
              if typeselect.values[0] == "lf":
                await loadfile_cb(interaction)
              elif typeselect.values[0] == "tc":
                select = ui.Select(placeholder="국가 코드 선택")
                select.add_option(label="kr",value="kr",description="한국판")
                select.add_option(label="en",value="en",description="영미판")
                select.add_option(label="jp",value="jp",description="일본판")
                select.add_option(label="tw",value="tw",description="타이완판")
                view=ui.View()
                view.add_item(select)
                async def select_callback(interaction:Interaction):
                  country = select.values[0]
                  print(country)
                  await interaction.response.send_modal(TCInputModal(country, interaction.guild_id))
                select.callback=select_callback
                await interaction.response.send_message(ephemeral=True,view=view,delete_after=30.0,content="30초 안에 국가코드를 선택해주세요.")
            typeselect.callback=type_cb
            await interaction.response.send_message(view=view_m, delete_after=30.0, ephemeral=True, content="30초 안에 메뉴를 선택해주세요.")
			
  button.callback=button_callback
  await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="정보", description="유저의 서버정보를 표시합니다.")
async def userinfosend(interaction: Interaction, usr: discord.User):
  srvid = str(interaction.guild_id)
  memid = str(usr.id)
  if os.path.exists(srvmemberpath(srvid, memid)):
    csvpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
    df = pd.read_csv(csvpath, sep=",", encoding="utf-8")
	set = loadsrvset(srvid)
    cash = str(df["CashAmount"].values[0])
	if set["CashSystemSetting"]["Use"] == "True":
		cash += set["CashSystemSetting"]["CashName"]
	else:
		cash = "사용되지 않음"
    banned = str(df["IsBanned"].values[0])
	if banned == "False":
		banned = "사용가능"
	else:
		banned = "사용불가"
    data = f"""
유저아이디: {memid}
재화: {cash}
서버봇 사용금지: {banned}
 """
    embed = discord.Embed(title="서버 유저정보입니다.", description=data)
  else:
    embed = discord.Embed(title="서버DB에 가입되지 않은 유저입니다.")
  await interaction.response.send_message(embed=embed)
  
@tree.command(name="가입", description="[필수] 이 서버에서 유저가 가입합니다.")
async def RegisterMem(interaction: Interaction):
  srvid = str(interaction.guild_id)
  memid = str(interaction.user.id)
  if not os.path.exists(srvmemberpath(srvid, memid)):
    os.mkdir(srvmemberpath(srvid, memid))
    csvdata = makeinfo(memid)
    csvpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
    with open(csvpath, "w+", encoding="utf-8") as csvwriter:
      csvwriter.write(csvdata)
    embed = discord.Embed(title="서버 멤버 가입 성공", description="서버DB에 성공적으로 가입되었습니다.")
  else:
    embed = discord.Embed(title="서버DB에 이미 가입되어 있습니다.")
  await interaction.response.send_message(embed=embed)

@tree.command(name="재화지급", description="재화를 유저에게 지급합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def GiveCash(interaction: Interaction, usr: discord.User, amount: int):
  srvid = str(interaction.guild_id)
  memid = str(usr.id)
  set = loadsrvset(srvid)
  if not chksrvallowed(str(interaction.guild_id)):
    await SendDisallowedMsg(interaction)
  else:
    if set["CashSystemSetting"]["Use"] == "True":
      if os.path.exists(srvmemberpath(srvid, memid)):
        userpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
        df = pd.read_csv(userpath, sep=",")
        if df['IsBanned'].values[0] == True:
          embed = discord.Embed(title="재화 지급 실패", description=f"수신 유저 {usr.mention}는 이 서버에서 봇을 사용할 수 없습니다.\n밴 해제 후 사용해주세요.")
        else:
          if (int(df.loc[df["UserId"] == int(memid), "CashAmount"]) + amount) < 0:
            embed = discord.Embed(title="재화 지급 실패", description="총 재화는 음수가 될 수 없습니다.")
          else:
            df.loc[df["UserId"] == int(memid), "CashAmount"] += amount
            df.to_csv(userpath, index=None)
            embed = discord.Embed(title="재화 지급 완료", description=f"{usr.mention}에게 재화를 {amount}만큼 지급하였습니다.\n{usr.mention}의 총 재화량은 {df['CashAmount'].values[0]} 입니다.")
      else:
        embed = discord.Embed(title="재화 지급 실패", description="수신 유저가 서버DB에 가입되어있지 않습니다.")
    else:
      embed = discord.Embed(title="재화 지급 실패", description="서버의 재화사용이 비활성화되어 있습니다.\n활성화 후 사용해주세요.")
    await interaction.response.send_message(embed=embed)
  
@tree.command(name="유저서버밴", description="멤버를 서버에서 봇을 사용금지시킵니다.")
@app_commands.checks.has_permissions(administrator=True)
async def SetBan(interaction: Interaction, usr: discord.User):
  srvid = str(interaction.guild_id)
  memid = str(usr.id)
  set = loadsrvset(srvid)
  if os.path.exists(srvmemberpath(srvid, memid)):
      userpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
      df = pd.read_csv(userpath, sep=",")
      df.loc[df["UserId"] == int(memid), "IsBanned"] = "True"
      df.to_csv(userpath, index=None)
      embed = discord.Embed(title="유저 서버봇 사용금지 성공", description=f"{usr.mention}을 서버봇 사용금지 시켰습니다.")
  else:
      embed = discord.Embed(title="작업 실패", description="해당 유저가 서버DB에 가입되어있지 않습니다.")
  await interaction.response.send_message(embed=embed)
      
@tree.command(name="유저서버밴해제", description="멤버를 서버에서 봇을 사용금지해제시킵니다.")
@app_commands.checks.has_permissions(administrator=True)
async def SetUnban(interaction: Interaction, usr: discord.User):
  srvid = str(interaction.guild_id)
  memid = str(usr.id)
  set = loadsrvset(srvid)
  if os.path.exists(srvmemberpath(srvid, memid)):
      userpath = os.path.join(srvmemberpath(srvid, memid), "userdata.csv")
      df = pd.read_csv(userpath, sep=",")
      df.loc[df["UserId"] == int(memid), "IsBanned"] = "False"
      df.to_csv(userpath, index=None)
      embed = discord.Embed(title="유저 서버봇 사용금지해제 성공", description=f"{usr.mention}을 서버봇 사용금지해제 시켰습니다.")
  else:
      embed = discord.Embed(title="작업 실패", description="해당 유저가 서버DB에 가입되어있지 않습니다.")
  await interaction.response.send_message(embed=embed)
      
@tree.command(name="서버등록", description="서버를 등록합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def RegisterSrv(interaction: Interaction):
  srvid = str(interaction.guild_id)
  if not os.path.exists(serverpath(srvid)):
    os.mkdir(serverpath(srvid))
    curset = loadsrvset_all()
    newdata = addjson.adddata(curset, srvid)
    savesrvset_all(newdata)
    embed = discord.Embed(title="서버등록 성공", description="서버가 성공적으로 등록되었습니다.\n꼭 봇 설정을 해주세요.")
  else:
    embed = discord.Embed(title="서버가 이미 등록되어 있습니다.")
  await interaction.response.send_message(embed=embed)

@tree.command(name="재화사용", description="에딧에 재화사용 활성화/비활성화")
@app_commands.checks.has_permissions(administrator=True)
async def UseCash(interaction: Interaction, use: CashUse):
  if use.value == "True":
    set = loadsrvset(str(interaction.guild_id))
    set["CashSystemSetting"]["Use"] = "True"
    savesrvset(str(interaction.guild_id), set)
    embed = discord.Embed(title="재화 사용이 활성화되었습니다.")
  elif use.value == "False":
    set = loadsrvset(str(interaction.guild_id))
    set["CashSystemSetting"]["Use"] = "False"
    savesrvset(str(interaction.guild_id), set)
    embed = discord.Embed(title="재화 사용이 비활성화되었습니다.")
  await interaction.response.send_message(embed=embed)
  
@tree.command(name="재화이름", description="에딧에 필요한 재화 이름")
@app_commands.checks.has_permissions(administrator=True)
async def cashname(interaction: Interaction, name: str):
  if chksrvallowed(str(interaction.guild_id)):
      set = loadsrvset(str(interaction.guild_id))
      if set["CashSystemSetting"]["Use"] == "True":
        set["CashSystemSetting"]["CashName"] = name
        savesrvset(str(interaction.guild_id), set)
        embed = discord.Embed(title=f"재화 가격을 {name}(으)로 설정했습니다.")
      else:
        embed = discord.Embed(title="재화 사용이 비활성화되어있습니다.\n활성화 후 설정해주세요.")
      await interaction.response.send_message(embed=embed)
  else:
    await SendDisallowedMsg(interaction)
  
@tree.command(name="재화가격", description="에딧에 필요한 재화 가격")
@app_commands.checks.has_permissions(administrator=True)
async def CashAmount(interaction: Interaction, amount: int):
  if chksrvallowed(str(interaction.guild_id)):
    set = loadsrvset(str(interaction.guild_id))
    if set["CashSystemSetting"]["Use"] == "True":
      set["CashSystemSetting"]["PricePerUse"] = amount
      savesrvset(str(interaction.guild_id), set)
      embed = discord.Embed(title=f"재화 가격을 {amount}로 설정했습니다.")
    else:
      embed = discord.Embed(title="재화 사용이 비활성화되어있습니다.\n활성화 후 설정해주세요.")
    await interaction.response.send_message(embed=embed)
  else:
    await SendDisallowedMsg(interaction)
    
@tree.command(name="구매로그설정", description="에딧시 구매로그를 보냅니다.")
@app_commands.checks.has_permissions(administrator=True)
async def sendcashlog(interaction: Interaction):
  if chksrvallowed(str(interaction.guild_id)):
    set = loadsrvset(str(interaction.guild_id))
    if set["CashSystemSetting"]["Use"] == "True":
      try:
		embed = discord.Embed(title="1️⃣ 이 채널에 웹후크를 생성합니다.\n2️⃣ 웹후크를 수동으로 입력합니다.")
		view = ui.View(timeout=30.0)
		button = ui.Button(style=ButtonStyle.green,label="1️⃣",disabled=False)
		button2 = ui.Button(style=ButtonStyle.green,label="2️⃣",disabled=False)
		view.add_item(button)
		view.add_item(button2)
		async def createit(interaction: Interaction):
			
		button.callback=createit
		button2.callback=typeit
		interaction.response.send(view=view, embed=embed)
		
        webhookobj = SyncWebhook.from_url(webhook)
        webhookobj.send(content="펄스에딧봇 구매로그 테스트 메시지", username="구매로그", avatar_url="https://i.imgur.com/8GnT3ZH.png")
        set["NoticeWebhook"] = webhook
        savesrvset(str(interaction.guild_id), set)
        embed = discord.Embed(title="설정 완료", description="구매로그를 설정 완료했습니다.")
      except:
        embed = discord.Embed(title="유효하지 않은 웹후크", description="웹후크가 유효하지 않습니다.")
        pass
    else:
      embed = discord.Embed(title="재화 사용이 비활성화되어있습니다.\n활성화 후 설정해주세요.")
    await interaction.response.send_message(embed=embed)
  else:
    await SendDisallowedMsg(interaction)
    
@tree.command(name="서버차단", description="???")
async def banserver(interaction: Interaction, srvid: str):
  if str(interaction.user.id) in CONFIG.botdev:
    try:
      int(srvid)
      go = True
    except:
      await interaction.response.send_message("String이 아닌 int서버 아이디를 입력해주세요.")
      go = False
    if go:
      set = loadsrvset(str(srvid))
      set["UsingAllowed"] = "False"
      savesrvset(str(srvid), set)
      guild = client.get_guild(int(srvid))
      embed = discord.Embed(title="차단 완료", description=f"{guild.name} 서버를 차단했습니다.")
      await interaction.response.send_message(embed=embed)
  else:
    await interaction.response.send_message("Access Denied")
    
@tree.command(name="서버차단해제", description="???")
async def unbanserver(interaction: Interaction, srvid: str):
  if str(interaction.user.id) in CONFIG.botdev:
    try:
      int(srvid)
      go = True
    except:
      await interaction.response.send_message("String이 아닌 int서버 아이디를 입력해주세요.")
      go = False
    if go:
      set = loadsrvset(str(srvid))
      set["UsingAllowed"] = "True"
      savesrvset(str(srvid), set)
      guild = client.get_guild(int(srvid))
      embed = discord.Embed(title="차단해제 완료", description=f"{guild.name} 서버를 차단해제했습니다.")
      await interaction.response.send_message(embed=embed)
  else:
    await interaction.response.send_message("Access Denied")

@tree.command(name="invite", description="???")
#서버 아이디로 서버초대링크 생성, 봇이 있는 서버만 가능.
async def invite(interaction: Interaction, guildid: str):
  if str(interaction.user.id) in CONFIG.botdev:
    guild = client.get_guild(int(guildid))
    invitelink = ""
    i = 0
    while invitelink == "":
      channel = guild.text_channels[i]
      link = await channel.create_invite(max_age=300,max_uses=99)
      invitelink = str(link)
      i += 1
    await interaction.response.send_message(invitelink)
  else:
    await interaction.response.send_message("Access Denied")

@tree.command(name="냥코검색", description="냥코 아이디검색")
async def CatSearchCommand(interaction: Interaction, usr_input: str):
	catdb = open("catdb.csv", "r", encoding="utf-8").read().split("\n")
	line_len = len(catdb)
	ctx = []
	for i in range(line_len-1):
		catname = str(catdb[i]).split(",")[0]
		catid = str(catdb[i]).split(",")[1]
		if usr_input in catname:
			ctx.append(str(catname)+": "+str(catid)+"\n")
		else:
			pass
	if len(ctx) == 0:
		embed_body = "검색결과가 없습니다"
	else:
		embed_body = ""
		for k in range(len(ctx)):
			embed_body += ctx[k]
	embed = discord.Embed(title="검색결과", description=embed_body)
	await interaction.response.send_message(embed=embed)

client.run(CONFIG.token)
