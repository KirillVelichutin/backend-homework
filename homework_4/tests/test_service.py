import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from schemas import TaskAddingSchema
from service.tasks import TasksService


def test_create_task(get_test_task):
    repository = Mock()
    users_repository = Mock()

    author = SimpleNamespace(id=1, username="author")
    responsible = SimpleNamespace(id=2, username="responsible")
    created_task = SimpleNamespace(id=1)

    users_repository.get_by_id = AsyncMock(return_value=responsible)
    users_repository.get_by_username = AsyncMock(return_value=author)
    repository.create = AsyncMock(return_value=created_task)

    service = TasksService(repository=repository, users_repository=users_repository)
    payload = TaskAddingSchema(**get_test_task)
    result = asyncio.run(service.create_task(payload, author_username=author.username))

    assert repository.create.called
    assert result == created_task
