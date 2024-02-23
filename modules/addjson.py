import json

def adddata(settings, srvids):
            THIS_JSON = '''
{
  "UsingAllowed": "True",
  "CmdChannel": "undefined",
  "NoticeWebhook": "undefined",
  "SrvAdminRole": "undefined",
  "CashSystemSetting": {
    "Use": "False",
    "CashName": "undefined",
    "PricePerUse": 0,
    "UseAttendReward": {
      "Use": "False",
      "Amount": 0
    }
  }
}
'''
            try:
                this_data = json.loads(THIS_JSON)
            except json.JSONDecodeError:
                print("Invalid JSON format.")
            else:
                settings[str(srvids)] = this_data
                return settings