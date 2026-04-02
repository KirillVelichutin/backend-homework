import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from api.tasks import create_task
from core.security import create_access_token
from schemas import TaskAddingSchema


def test_create_task(get_test_task):
    service = Mock()
    request = Mock()
    request.cookies = {"access_token": asyncio.run(create_access_token({"sub": "author"}))}

    service.create_task = AsyncMock(return_value=SimpleNamespace(
        id=1,
        name="task",
        about="text",
        importance="Must do",
        author_id=1,
        responsible_id=2,
        deadline=date(2026, 3, 30),
        is_done=False,
    ))

    response = asyncio.run(create_task(TaskAddingSchema(**get_test_task), request, service))

    assert response.status_code == 201
