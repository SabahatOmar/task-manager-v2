from app.services.tag_service import TagService
import pytest
from app.models.tag_model import Tag

@pytest.fixture
def sample_tags(app):
    with app.app_context():
        tag1 = Tag(name='urgent')
        tag2 = Tag(name='home')
        return [tag1,tag2]



