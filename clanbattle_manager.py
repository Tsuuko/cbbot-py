import requests
from datetime import datetime
import load_settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def fetch_status():
    """
    解析サイト<https://redive.estertion.win> からクラバト情報を取ってくる
    return {
        "cb_start": datetime,
        "cb_end": datetime,
        "cb_days": int
    }
    """
    # クラバト開催情報取得
    r = requests.get(
        "https://redive.estertion.win/ver_log_redive/?page=1&filter=clan_battle"
    ).json()

    # クラバト開始日取得
    cb_start = r["data"][0]["clan_battle"][0]["start"]
    cb_start = datetime.strptime(cb_start, "%Y/%m/%d %H:%M:%S")

    # クラバト終了日取得
    cb_end = r["data"][0]["clan_battle"][0]["end"]
    cb_end = datetime.strptime(cb_end, "%Y/%m/%d %H:%M:%S")

    # クラバト開催日数
    cb_days = (cb_end - cb_start).days + 1

    return {"cb_start": cb_start, "cb_end": cb_end, "cb_days": cb_days}

class spreadsheet:
    def __init__(self):
        self.__authorize()

    def __authorize(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        credential=load_settings.SHEETS_CREDENTIAL
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)
        gc = gspread.authorize(credentials)
        self.sheet = gc.open_by_url(load_settings.SPREADSHEET_URL)

    def __is_registered_user(self,username):
        ws=self.sheet.worksheet("main")
        result=ws.range(2,1,ws.row_count,1)
        #result=ws.findall(username)
        count=len([1 for i in result if i.value==username])
        if count==0:
            return False
        else:
            return True

    def add_user(self,username):
        if not self.__is_registered_user(username):
            ws=self.sheet.worksheet("main")
            cell_range=f"B{ws.row_count+1}:L{ws.row_count+1}"
            result=ws.append_row([username, '', '', '', '', '', '', '', '', '', '', '', f'=COUNTIF({cell_range},"3凸")+COUNTIF({cell_range},"2凸")+COUNTIF({cell_range},"1凸")', f'=COUNTIF({cell_range},"報忘")'],value_input_option='USER_ENTERED')
            return result["updates"]["updatedColumns"]
        else:
            raise Exception("ユーザーはすでに存在します。")

if __name__ == "__main__":
    spreadsheet=spreadsheet()
    print(spreadsheet.is_registered_user("つうこ"))
