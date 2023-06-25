##
# mongoDB操作
##

from urllib.parse import urlparse

from pymongo import MongoClient

import load_settings

MONGODB_URI = load_settings.MONGODB_URI
DB_NAME = urlparse(MONGODB_URI).path[1:]
client = MongoClient(MONGODB_URI + "?retryWrites=false")
db = client[DB_NAME]


def init_data():
    """
    prefix設定がなかった時に`!`をprefixとして設定する
    """
    collection = db["settings"]
    result = collection.find_one({"item": "prefix"})
    if result == None:
        collection.create_index("item", unique=True)
        data = {"item": "prefix", "data": "!"}
        collection.insert_one(data)


def get_prefix():
    """
    DBからprefixを読み取り
    """
    collection = db["settings"]
    result = collection.find_one({"item": "prefix"})
    if result is not None:
        return result["data"]
    else:
        return None


def set_prefix(prefix):
    """
    DBにprefixを保存
    """
    collection = db["settings"]
    collection.update_one(
        {"item": "prefix"}, {"$set": {"item": "prefix", "data": prefix}}
    )
    if get_prefix() == prefix:
        return True
    else:
        return False


if __name__ == "__main__":
    # init()
    print(get_prefix())
    a = set_prefix("!")
    print(a)
    print(get_prefix())
