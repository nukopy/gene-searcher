import sys
from io import StringIO
from logging import INFO, Formatter, Logger, StreamHandler

import pytest

from app.logger import create_logger, create_stream_handler


@pytest.fixture
def logger_setup():
    name = "test_logger"
    level = INFO
    output = StringIO()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    return name, level, output, log_format, date_format


def test_create_stream_handler_success(logger_setup: tuple):
    # テスト項目: 正常系: create_stream_handler で StreamHandler が正常に作成される
    # given (前提条件):
    _, level, _, log_format, date_format = logger_setup

    # when (操作):
    handler = create_stream_handler(level, sys.stdout, log_format, date_format)

    # then (期待する結果):
    assert isinstance(handler, StreamHandler)
    assert handler.stream == sys.stdout
    assert handler.level == level
    assert isinstance(handler.formatter, Formatter)
    assert handler.formatter._fmt == log_format
    assert handler.formatter.datefmt == date_format


def test_create_logger_with_empty_handlers_success(logger_setup: tuple):
    # テスト項目: 正常系: create_logger で handlers として何も渡さなかったとき、StreamHandler(sys.stdout) をハンドラとして設定した Logger が正常に作成される
    # given (前提条件):
    name, level, _, log_format, date_format = logger_setup

    # when (操作):
    logger = create_logger(name, level, [], log_format, date_format)

    # then (期待する結果):
    assert isinstance(logger, Logger)
    assert logger.name == name
    assert logger.level == level
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert isinstance(handler, StreamHandler)
    assert handler.stream == sys.stdout
    assert handler.level == level
    assert isinstance(handler.formatter, Formatter)
    assert handler.formatter._fmt == log_format
    assert handler.formatter.datefmt == date_format
    assert not logger.propagate


def test_create_logger_with_custom_handler_success(logger_setup: tuple):
    # テスト項目: 正常系: create_logger で handlers として StreamHandler を渡したとき、その StreamHandler がハンドラとして設定された Logger が正常に作成される
    # given (前提条件):
    name, level, _, log_format, date_format = logger_setup
    custom_handler = StreamHandler(sys.stderr)

    # when (操作):
    logger = create_logger(name, level, [custom_handler], log_format, date_format)

    # then (期待する結果):
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert isinstance(handler, StreamHandler)
    assert handler.stream == sys.stderr


def test_logger_info_output(logger_setup: tuple):
    # テスト項目: 正常系: ロガーに info メッセージを出力したとき、正しくログメッセージが出力される
    # given (前提条件):
    name, level, output, log_format, date_format = logger_setup
    custome_handler = StreamHandler(output)  # 出力を捕捉するための StreamHandler
    logger = create_logger(name, level, [custome_handler], log_format, date_format)
    message = "This is an info message"

    # when (操作):
    logger.info(message)

    # StringI/O からログメッセージを読み取り
    output.seek(0)
    log_output = output.read()

    # 期待されるログメッセージが含まれていることを検証
    assert message in log_output
