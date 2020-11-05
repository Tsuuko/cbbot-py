import inspect
import logging
from pprint import pprint

import coloredlogs


def getLogger() -> logging.Logger:
    logger = None

    # 呼び出し元ファイル名からloggerを取得する
    stack = inspect.stack()
    for s in stack[1:]:
        m = inspect.getmodule(s[0])
        if m:
            logger = logging.getLogger(m.__name__)
            break

    # 呼び出し元ファイル名が見つからない場合はbot logger
    if not logger:
        logger = logging.getLogger("bot")

    # 書式等の設定をセット
    _set_logger_settings(logger)

    return logger


def _set_logger_settings(logger) -> None:
    coloredlogs.install(
        logger=logger,
        level="INFO",
        fmt="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        milliseconds=True,
    )


def printLoggers() -> None:
    pprint(logging.Logger.manager.loggerDict)  # type: ignore
