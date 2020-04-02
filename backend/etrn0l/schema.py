from marshmallow import Schema, fields, post_load
from .model import FlashLoop


class FlashLoopSchema(Schema):
    id = fields.String()
    number = fields.Integer(required=True)
    source_video = fields.String(allow_none=True)
    source_audio = fields.String(allow_none=True)
    tags = fields.List(fields.String(), required=True)

    @post_load
    def make_loop(self, data, **kwargs):
        """Convert to dataclass after load."""
        return FlashLoop(tags=data["tags"],
                         id=data.get("id"),
                         number=data.get("number"),
                         source_audio=data.get("source_audio"),
                         source_video=data.get("source_video"))


class FlashLoopRequestSchema(FlashLoopSchema):
    id = fields.String(dump_only=True)
    number = fields.Integer(dump_only=True)

