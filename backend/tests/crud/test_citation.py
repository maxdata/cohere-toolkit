import pytest

from backend.crud import citation as citation_crud
from backend.models.citation import Citation
from backend.tests.factories import get_factory


@pytest.fixture(autouse=True)
def conversation(session):
    return get_factory("Conversation", session).create(id="1")


@pytest.fixture(autouse=True)
def message(session, conversation):
    return get_factory("Message", session).create(id="1", conversation_id="1")


@pytest.fixture(autouse=True)
def document(session, conversation, message):
    return get_factory("Document", session).create(
        id="1", conversation_id="1", message_id="1"
    )


def test_create_citation(session):
    citation_data = Citation(
        text="Hello, World!",
        user_id="1",
        start=1,
        end=2,
        message_id="1",
        document_ids=["1"],
    )

    citation = citation_crud.create_citation(session, citation_data)
    assert citation.text == citation_data.text
    assert citation.user_id == citation_data.user_id
    assert citation.start == citation_data.start
    assert citation.end == citation_data.end
    assert citation.message_id == citation_data.message_id
    assert citation.document_ids == citation_data.document_ids

    citation = citation_crud.get_citation(session, citation.id)
    assert citation.text == citation_data.text
    assert citation.user_id == citation_data.user_id
    assert citation.start == citation_data.start
    assert citation.end == citation_data.end
    assert citation.message_id == citation_data.message_id
    assert citation.document_ids == citation_data.document_ids


def test_get_citation(session):
    _ = get_factory("Citation", session).create(
        id="1", text="Hello, World!", user_id="1", message_id="1", document_ids=["1"]
    )

    citation = citation_crud.get_citation(session, "1")
    assert citation.text == "Hello, World!"
    assert citation.id == "1"


def test_fail_get_nonexistent_citation(session):
    citation = citation_crud.get_citation(session, "123")
    assert citation is None


def test_list_citations(session):
    _ = get_factory("Citation", session).create(
        text="Hello, World!", user_id="1", message_id="1", document_ids=["1"]
    )

    citations = citation_crud.get_citations(session)
    assert len(citations) == 1
    assert citations[0].text == "Hello, World!"


def test_list_citations_empty(session):
    citations = citation_crud.get_citations(session)
    assert len(citations) == 0


def test_list_citations_with_pagination(session):
    for i in range(10):
        get_factory("Citation", session).create(
            text=f"Citation {i}", user_id="1", message_id="1", document_ids=["1"]
        )

    citations = citation_crud.get_citations(session, offset=5, limit=5)
    assert len(citations) == 5

    for i, citation in enumerate(citations):
        assert citation.text == f"Citation {i + 5}"


def test_list_citations_by_message_id(session):
    for i in range(10):
        get_factory("Citation", session).create(
            text=f"Citation {i}", user_id="1", message_id="1", document_ids=["1"]
        )

    citations = citation_crud.get_citations_by_message_id(session, "1")
    assert len(citations) == 10

    for i, citation in enumerate(citations):
        assert citation.text == f"Citation {i}"


def test_list_citations_by_message_id_empty(session):
    citations = citation_crud.get_citations_by_message_id(session, "1")
    assert len(citations) == 0


def test_delete_citation(session):
    citation = get_factory("Citation", session).create(
        id="1", text="Hello, World!", user_id="1", message_id="1", document_ids=["1"]
    )

    citation_crud.delete_citation(session, "1")

    citation = citation_crud.get_citation(session, "1")
    assert citation is None


def test_delete_citation_nonexistent(session):
    citation = citation_crud.delete_citation(session, "1")
    assert citation is None
