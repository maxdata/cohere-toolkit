import factory

from backend.models import Citation

from .base import BaseFactory


class CitationFactory(BaseFactory):
    class Meta:
        model = Citation

    text = factory.Faker("text")
    user_id = factory.Faker("uuid4")
    message_id = factory.Faker("uuid4")
    start = factory.Faker("random_int")
    end = factory.Faker("random_int")

    documents = []
    document_ids = []
