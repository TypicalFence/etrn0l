"""Service classes implementation using MongoDB."""

from typing import Optional, List
from mongoengine import Document, StringField  # type: ignore
from mongoengine import connect, ListField, SequenceField
from . import FlashLoop, FlashLoopService
from ..schema import FlashLoopSchema


class FlashLoopDocument(Document):
    """Represents a flash loop."""

    # maybe we should not replicate the number url scheme
    # it doesn't quite fit mongodb and we might run into problems
    # currently the goal is it replicate z0r and r0z as close as possible
    number = SequenceField()
    source_video = StringField()
    source_audio = StringField()
    tags = ListField(StringField(), required=True)

    def to_model(self) -> FlashLoop:
        """Converts the Document to the Common model.
        Which used everywhere else in the app.
        """
        schema = FlashLoopSchema()
        data = dict(id=str(self.id),
                    number=self.number,
                    source_audio=self.source_audio,
                    source_video=self.source_video,
                    tags=self.tags)
        return schema.load(data)


class MongoFlashLoopService(FlashLoopService):
    """Implements the FlashLoopService using MongoDB."""

    def __init__(self, db):
        connect(db)

    def add_loop(self, loop: FlashLoop) -> str:
        model = FlashLoopDocument(tags=loop.tags,
                                  source_video=loop.source_video,
                                  source_audio=loop.source_audio)
        model = model.save()
        return str(model.id)

    def remove_loop(self, loop_id) -> bool:
        try:
            loop = FlashLoopDocument.objects.get(id=loop_id)
            loop.delete()
            return True
        except FlashLoopDocument.DoesNotExist:
            return False

    def get_loop_by_id(self, loop_id) -> Optional[FlashLoop]:
        try:
            loop = FlashLoopDocument.objects.get(id=loop_id)
            return loop.to_model()
        except FlashLoopDocument.DoesNotExist:
            return None

    def get_random_loop(self) -> FlashLoop:
        objects = FlashLoopDocument.objects
        loop = list(objects.aggregate([{"$sample": {"size": 1}}]))[0]
        loop["id"] = loop["_id"]
        del loop["_id"]
        return FlashLoopDocument(**loop).to_model()

    def get_loop_count(self) -> int:
        return FlashLoopDocument.objects.count()

    def list_loops(self, start, count) -> List[FlashLoop]:

        if start != 0:
            start = start - 1

        models = FlashLoopDocument.objects.skip(start).limit(count)
        return list(map(lambda x: x.to_model(), models))

    def get_loop_by_number(self, loop_number: int) -> Optional[FlashLoop]:
        try:
            loop = FlashLoopDocument.objects.get(number=loop_number)
            return loop.to_model()
        except FlashLoopDocument.DoesNotExist:
            return None

    def update_loop(self, loop: FlashLoop) -> Optional[FlashLoop]:
        try:
            db_loop = FlashLoopDocument.objects.get(id=loop.id)
        except FlashLoopDocument.DoesNotExist:
            return None

        db_loop.tags = loop.tags
        db_loop.source_audio = loop.source_audio
        db_loop.source_video = loop.source_video
        db_loop.save()

        return db_loop.to_model()
