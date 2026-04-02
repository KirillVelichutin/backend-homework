import asyncio
from unittest.mock import AsyncMock, Mock, patch

from service.storage import StorageService


def test_upload_task_avatar_returns_url():
    storage = StorageService(client=Mock())

    file = Mock()
    file.filename = "avatar.png"
    file.content_type = "image/png"
    file.read = Mock()
    file.close = Mock()

    async def read():
        return b"file-content"

    async def close():
        return None

    file.read = read
    file.close = close

    mocked_to_thread = AsyncMock(return_value=None)

    with patch("service.storage.asyncio.to_thread", new=mocked_to_thread):
        result = asyncio.run(storage.upload_task_avatar(1, file))

    assert result.endswith(".png")
    assert "/task-avatars/tasks/1/avatars/" in result
    mocked_to_thread.assert_awaited_once()
    assert mocked_to_thread.await_args.args[0] == storage.client.put_object
