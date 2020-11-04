import glob
from typing import List


def get_extension_path_list() -> List[str]:
    # cogのload用ファイル読み込み
    path = glob.glob("**/load_*.py", recursive=True)

    # bot.load_extension()で読み込む書式に変換
    path = list(map(lambda v: v.replace("\\", ".").replace(".py", ""), path))

    return path
