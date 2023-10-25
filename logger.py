from __future__ import annotations

from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    FileHandler,
    Formatter,
    Logger,
    StreamHandler,
    getLogger,
)
from typing import TextIO


def create_stream_handler(
    log_format: str, stream_log_level: int
) -> StreamHandler[TextIO]:
    """ストリームハンドラを作成する.

    :param log_format: ログのフォーマット
    :param stream_log_level: ストリームハンドラのログレベル
    :return: ストリームハンドラ
    """
    stream_handler: StreamHandler[TextIO] = StreamHandler()
    formatter = Formatter(log_format)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_log_level)
    return stream_handler


def create_file_handler(log_format: str, log_filename: str) -> FileHandler:
    """ファイルハンドラを作成する.

    :param log_format: ログのフォーマット
    :param log_filename: ファイル名
    :return: ファイルハンドラ.
    """
    file_handler = FileHandler(log_filename)
    formatter = Formatter(log_format)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(NOTSET)
    return file_handler


def set_logger(
    module_name: str,
    stream_log_level: int = INFO,
    file_log_level: int = DEBUG,
    log_filename: str = "scrape.log",
    log_format: str = (
        "[%(asctime)s] [%(levelname)s] "
        "(%(filename)s | %(funcName)s | %(lineno)s) "
        "%(message)s"
    ),
) -> Logger:
    """与えられたモジュール名のloggerを設定する.

    :param module_name: loggerが設定されているモジュールの名前
    :param stream_log_level: ストリームハンドラのログレベル
    :param file_log_level: ファイルハンドラのログレベル
    :param log_filename: ログファイルの名前
    :param log_format: ログのフォーマット
    :return: loggerオブジェクト
    """
    valid_log_levels: list[int] = [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    if (
        stream_log_level not in valid_log_levels
        or file_log_level not in valid_log_levels
    ):
        msg = "無効なログレベルが指定されました。"
        raise ValueError(msg)
    logger: Logger = getLogger(module_name)
    logger.handlers.clear()

    stream_handler = create_stream_handler(log_format, stream_log_level)
    logger.addHandler(stream_handler)

    file_handler = create_file_handler(log_format, log_filename)
    logger.addHandler(file_handler)

    logger.setLevel(min(stream_log_level, file_log_level))

    return logger
