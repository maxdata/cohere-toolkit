import pytest

from backend.crud import file as file_crud
from backend.models.file import File
from backend.schemas.file import UpdateFile
from backend.tests.factories import get_factory


@pytest.fixture(autouse=True)
def conversation(session, user):
    return get_factory("Conversation", session).create(id="1", user_id=user.id)


def test_create_file(session, user):
    file_data = File(
        file_name="test.txt",
        file_path="/tmp/test.txt",
        file_size=100,
        conversation_id="1",
        user_id="1",
    )

    file = file_crud.create_file(session, file_data)
    assert file.file_name == file_data.file_name
    assert file.file_path == file_data.file_path
    assert file.file_size == file_data.file_size
    assert file.conversation_id == file_data.conversation_id
    assert file.user_id == file_data.user_id

    file = file_crud.get_file(session, file.id, user.id)
    assert file.file_name == file_data.file_name
    assert file.file_path == file_data.file_path
    assert file.file_size == file_data.file_size
    assert file.conversation_id == file_data.conversation_id
    assert file.user_id == file_data.user_id


def test_get_file(session, user):
    _ = get_factory("File", session).create(
        id="1", file_name="test.txt", conversation_id="1", user_id=user.id
    )

    file = file_crud.get_file(session, "1", user.id)
    assert file.file_name == "test.txt"
    assert file.id == "1"


def test_fail_get_nonexistent_file(session, user):
    file = file_crud.get_file(session, "123", user.id)
    assert file is None


def test_list_files(session, user):
    _ = get_factory("File", session).create(
        file_name="test.txt", conversation_id="1", user_id=user.id
    )

    files = file_crud.get_files(session, user.id)
    assert len(files) == 1
    assert files[0].file_name == "test.txt"


def test_list_files_empty(session, user):
    files = file_crud.get_files(session, user.id)
    assert len(files) == 0


def test_list_files_with_pagination(session, user):
    for i in range(10):
        _ = get_factory("File", session).create(
            file_name=f"test.txt {i}", conversation_id="1", user_id=user.id
        )

    files = file_crud.get_files(session, user.id, offset=5, limit=5)
    assert len(files) == 5

    for i, file in enumerate(files):
        assert file.file_name == f"test.txt {i + 5}"


def test_list_files_by_conversation_id(session, user):
    for i in range(10):
        _ = get_factory("File", session).create(
            file_name=f"test.txt {i}", conversation_id="1", user_id=user.id
        )

    files = file_crud.get_files_by_conversation_id(session, "1", user.id)
    assert len(files) == 10

    for i, file in enumerate(files):
        assert file.file_name == f"test.txt {i}"
        assert file.conversation_id == "1"


def test_list_files_by_conversation_id_empty(session, user):
    files = file_crud.get_files_by_conversation_id(session, "1", user.id)
    assert len(files) == 0


def test_update_file(session, user):
    file = get_factory("File", session).create(
        file_name="test.txt", conversation_id="1", user_id=user.id
    )

    new_file_data = UpdateFile(
        file_name="new_name.txt",
    )

    updated_file = file_crud.update_file(session, file, new_file_data)
    assert updated_file.file_name == new_file_data.file_name
    assert updated_file.file_path == file.file_path
    assert updated_file.file_size == file.file_size
    assert updated_file.conversation_id == file.conversation_id
    assert updated_file.user_id == file.user_id


def test_delete_file(session, user):
    file = get_factory("File", session).create(
        file_name="test.txt", conversation_id="1", user_id=user.id
    )

    file_crud.delete_file(session, file.id, user.id)
    assert file_crud.get_file(session, file.id, user.id) is None
