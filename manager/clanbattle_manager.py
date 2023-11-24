from datetime import datetime
from io import BytesIO

import discord
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from pdf2image import convert_from_bytes
from dateutil.relativedelta import relativedelta

import load_settings

SPREADSHEET_URL = load_settings.SPREADSHEET_URL


def fetch_status():
    # """
    # 解析サイト<https://redive.estertion.win> からクラバト情報を取ってくる

    # return
    # ----
    # ```
    # {
    #     "cb_start": datetime,
    #     "cb_end": datetime,
    #     "cb_days": int
    # }
    # ```
    # """


    # # クラバト開催情報取得
    # r = requests.get(
    #     # FIXME: Issue #122
    #     # "https://redive.estertion.win/ver_log_redive/?page=1&filter=clan_battle"
    #     "https://raw.githubusercontent.com/Tsuuko/cbbot-py/master/tmp/cb_schedule_stub.json"
    # ).json()

    # # クラバト開始日取得
    # cb_start = r["data"][0]["clan_battle"][0]["start"]
    # cb_start = datetime.strptime(cb_start, "%Y/%m/%d %H:%M:%S")

    # # クラバト終了日取得
    # cb_end = r["data"][0]["clan_battle"][0]["end"]
    # cb_end = datetime.strptime(cb_end, "%Y/%m/%d %H:%M:%S")

    # # クラバト開催日数
    # cb_days = (cb_end - cb_start).days + 1


    # 現在の日付を取得
    now = datetime.now()

    # その月の最終日を取得
    end_of_month = now + relativedelta(day=31)

    # 最終日から5日前と1日前の日付を計算
    cb_start = (end_of_month - relativedelta(days=5)).replace(
        hour=5, minute=0, second=0, microsecond=0
    )
    cb_end = (end_of_month - relativedelta(days=1)).replace(
        hour=23, minute=59, second=59, microsecond=0
    )

    return {"cb_start": cb_start, "cb_end": cb_end, "cb_days": 5}


def get_cbday():
    """
    クラバト日時確認用
    bot本体では未使用

    return
    ----
    ```
    None
    ```
    """
    cb_status = fetch_status()
    # cb_status = {
    #    'cb_start': datetime.strptime('2020/02/23 5:00:00',
    #                                  '%Y/%m/%d %H:%M:%S'),
    #    'cb_end': datetime.strptime('2020/02/28 23:59:59',
    #                                '%Y/%m/%d %H:%M:%S'),
    #    'cb_days': 6
    # }
    now_datetime = datetime.now()
    # now = "2020-02-29 15:00:00"
    # now_datetime = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    now_cbday = (now_datetime - cb_status["cb_start"]).days + 1

    print("現在日時：", now_datetime)
    print("開始日時：", cb_status["cb_start"])
    print("終了日時：", cb_status["cb_end"])
    print("開催期間：", cb_status["cb_days"])
    print(cb_status["cb_days"] - now_cbday)
    print(cb_status["cb_end"])
    if now_cbday <= 0:
        print(f"クラバト開催まであと{now_cbday+1}日")
    elif (
        (now_cbday >= 1)
        and (now_cbday <= cb_status["cb_days"])
        and now_datetime < cb_status["cb_end"]
    ):
        print(f"クラバト開催中！　{now_cbday}/{cb_status['cb_days']}日目")
    else:
        print(f"クラバトは終了しています。{now_cbday-cb_status['cb_days']}日経過")

    # print(now_cbday)


def set_cbstatus(status):
    """
    クランバトル開催情報と日数を設定する。

    params
    ----
    fetch_status()の結果を引数に指定する。
    ```
    {"cb_start": datetime,"cb_end": datetime,"cb_days": int}
    ```

    return
    ----
    ```
    cb_is_open:bool, # クラバトが開催中の場合はTrueを返す
    cb_remaining_days:int, # 当日を含めない残日数を返す（最終日は0が返される）
    now_cbday:int # 現在の日数（開催当日は1）
    ```
    """
    # 現在日時
    now_datetime = datetime.now()
    # クラバト何日目か
    now_cbday = (now_datetime - status["cb_start"]).days + 1
    # 残り何日か（最終日は0が返される）
    remaining_days = status["cb_days"] - now_cbday

    # 1日目以上&開催日数以下の場合（開催中）
    # if now_cbday >= 1 and now_cbday <= status["cb_days"]:
    if (
        (now_cbday >= 1)
        and (now_cbday <= status["cb_days"])
        and now_datetime < status["cb_end"]
    ):
        return True, remaining_days, now_cbday
    # 最終日の5時を回った場合
    if remaining_days == 0 and now_datetime > status["cb_end"]:
        return False, remaining_days - 1, now_cbday - 1
    # それ以外（非開催中）
    else:
        return False, remaining_days, now_cbday


def shot_capture():
    """
    スプレッドシート1枚目のキャプチャを取る。

    return
    ---
    ```
    f:io.BytesIO # pngファイル
    ```
    """
    r = requests.get(
        SPREADSHEET_URL
        + "export?format=pdf&size=executive&portrait=false&scale=4&top_margin=0.10&bottom_margin=0.00&left_margin=0.10&right_margin=0.00&horizontal_alignment=CENTER&vertical_alignment=MIDDLE"
    )
    images = convert_from_bytes(r.content)
    f = BytesIO()
    images[0].save(f, "PNG")
    f.seek(0)
    return f


### あきらめた
# def is_need_send_last_day_notification(remaining_days:int,notification_hour:list):
#    """
#    notification_hourで指定した時間の場合にembedを返す。
#    それ以外はNoneを返す。
#
#    params
#    ----
#    remaining_days:int # クラバト残り時間（最終日は0）
#    notification_hour:list # 指定する時間を6から24のリストで返す(小数点OK)
#        # 例
#        notification_hour=[12,17,20,23] # 12,17,20,23時にTrueを返す
#        notification_hour=[12.5,20.5] # 12時半,20時半にTrueを返す
#
#    return
#    ---
#    ```
#    - 指定した時間:discord.Embed
#    - それ以外:None
#    ```
#    """
#    # 現在日時
#    now_datetime = datetime.now()


class spreadsheet:
    # def __init__(self):
    #    self._authorize()

    def _authorize(self):
        """
        spreadsheetにログインする。
        1時間位経つと期限が切れる。

        return
        ----
        ```
        None
        ```

        set
        ----
        ```
        self.sheet:Spreadsheet #スプレッドシートクラス
        ```
        """
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credential = load_settings.SHEETS_CREDENTIAL
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credential, scope
        )
        gc = gspread.authorize(credentials)
        self.sheet = gc.open_by_url(load_settings.SPREADSHEET_URL)

    def _chk_registered_user(self, user_id):
        """
        ユーザーがスプレッドシートに登録されているか確認する。

        params
        ----
        ```
        username:str # 確認するユーザー名
        ```
        return
        -----
        - 登録済み：True
        - 未登録：False
        """
        ws = self.sheet.worksheet("main")
        result = ws.range(2, 1, ws.row_count, 1)
        # result=ws.findall(username)
        count = len([i.value for i in result if i.value == str(user_id)])
        if count == 0:
            return False
        else:
            return True

    def add_user(self, user: discord.User):
        """
        ユーザーをスプレッドシートに登録する。

        params
        ----
        ```
        username:str # 登録するユーザー名
        ```
        return
        ----
        ```
        result["updates"]["updatedColumns"]:int # よくわかりません。つかってない。
        ```
        """
        self._authorize()
        if not self._chk_registered_user(user.id):
            ws = self.sheet.worksheet("main")
            cell_range = f"B{ws.row_count+1}:K{ws.row_count+1}"
            result = ws.append_row(
                [
                    f"'{user.id}",
                    user.display_name,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    f'=COUNTIF({cell_range},"3凸")+COUNTIF({cell_range},"2凸")+COUNTIF({cell_range},"1凸")+COUNTIF({cell_range},"報忘")',
                    f'=COUNTIF({cell_range},"報忘")',
                ],
                value_input_option="USER_ENTERED",
            )
            print("add_user", result)
            return result["updates"]["updatedColumns"]
        else:
            raise Exception("ユーザーはすでに存在します。")

    def delete_user(self, user_id):
        """
        ユーザーをスプレッドシートから削除する。

        params
        ----
        ```
        username:str # 削除するユーザー名

        ```
        return
        ----
        ```
        None
        ```
        """
        self._authorize()
        if self._chk_registered_user(user_id):
            ws = self.sheet.worksheet("main")
            result = ws.range(2, 1, ws.row_count, 1)
            user_list = [i for i in result if i.value == str(user_id)]
            if len(user_list) == 1:
                result = ws.delete_row(user_list[0].row)
                print("delete_user", result)

            else:
                raise Exception("同名ユーザーが2人以上登録されています。")
        else:
            raise Exception("ユーザーが存在しません。")

    def set_attack(self, user: discord.User, count, cbday):
        """
        凸登録する。

        params
        ----
        ```
        user:discord.User # 登録するユーザー名
        count:int # 凸回数
        cbday:int # クラバト何日目か
        ```

        return
        ----
        ```
        None
        ```
        """
        self._authorize()
        if self._chk_registered_user(user.id):
            ws = self.sheet.worksheet("main")
            result = ws.range(2, 1, ws.row_count, 1)
            user_list = [i for i in result if i.value == str(user.id)]
            if len(user_list) == 1:
                result = ws.update_cell(
                    user_list[0].row, cbday + 2, ["", "1凸", "2凸", "3凸"][count]
                )
                print("set_attack", result)

            else:
                raise Exception("同名ユーザーが2人以上登録されています。")
        else:
            raise Exception("ユーザーが存在しません。")

    def clear_all_attack(self):
        """
        スプレッドシートの凸欄とメモ欄1を削除

        return
        ----
        ```
        None
        ```
        """
        self._authorize()
        ws = self.sheet.worksheet("main")
        # 1日目から10日目を削除
        self.sheet.values_clear(f"{ws.title}!C2:L{ws.row_count}")
        # メモ欄1を削除
        self.sheet.values_clear(f"{ws.title}!O2:O{ws.row_count}")


if __name__ == "__main__":
    get_cbday()
