from datetime import datetime
from unittest.mock import Mock
from page_analyzer.app import lencheck, transform, transform_user, \
    check_transformation, app
import pytest


def test_lencheck():
    text = Mock(text="hello")
    assert lencheck(text) == "hello"
    long_text = Mock(text="x" * 255)
    assert lencheck(long_text) == "is too long, >254"


def test_transform():
    urls = [(1, 'https://example.com', datetime.now(), 200, datetime.now()),
            (2, 'https://google.com', datetime.now(), None, None)]
    expected_result = [
        {"id": 2, "name": "https://google.com"},
        {"id": 1, "name": "https://example.com", "status_code": 200,
         "last_check": datetime.now().strftime("%d/%m/%Y")}]
    assert transform(urls) == expected_result


def test_transform_user():
    url = (1, 'https://example.com', datetime.now())
    expected_result = {"id": 1, "name": "https://example.com",
                       "created_at": datetime.now().strftime("%d/%m/%Y")}
    assert transform_user(url) == expected_result


def test_check_transformation():
    info = [(1, 200, datetime.now(), "H1", "Title", "Description"),
            (2, 400, datetime.now(), "H2", "Other Title", "")]
    expected_result = [
        {"id": 2, "status_code": 400,
         "created_at": datetime.now().strftime("%d/%m/%Y"),
         "h1": "H2", "title": "Other Title", "description": ""},
        {"id": 1, "status_code": 200,
         "created_at": datetime.now().strftime("%d/%m/%Y"),
         "h1": "H1", "title": "Title", "description": "Description"}]
    assert check_transformation(info) == expected_result

