from backend.tests.factories.citation import CitationFactory
from backend.tests.factories.conversation import ConversationFactory
from backend.tests.factories.document import DocumentFactory
from backend.tests.factories.file import FileFactory
from backend.tests.factories.message import MessageFactory
from backend.tests.factories.user import UserFactory

FACTORY_MAPPING = {
    "User": UserFactory,
    "File": FileFactory,
    "Conversation": ConversationFactory,
    "Citation": CitationFactory,
    "Message": MessageFactory,
    "Document": DocumentFactory,
}


def get_factory(model_name, session=None):
    factory = FACTORY_MAPPING[model_name]
    factory._meta.sqlalchemy_session = session
    return factory
