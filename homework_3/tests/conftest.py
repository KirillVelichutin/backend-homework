import pytest
from datetime import datetime
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

os.environ.setdefault("db_host", "localhost")
os.environ.setdefault("db_port", "5432")
os.environ.setdefault("db_user", "test")
os.environ.setdefault("db_pass", "test")
os.environ.setdefault("db_name", "test")
os.environ.setdefault("secret_key", "test-secret-key")


@pytest.fixture
def get_test_user():
    return {
        "username": f"User{datetime.now().strftime('%H%M%S')}",
        "email": f"User{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "1234566436",
    }

@pytest.fixture
def get_test_task():
    return {
        "name": "task",
        "about": "text",
        "importance": "Must do",
        "responsible_id": 2,
        "deadline": "2026-03-30",
        "is_done": False,
    }
