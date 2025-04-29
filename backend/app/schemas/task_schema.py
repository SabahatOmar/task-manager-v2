from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    priority = fields.Str()
    deadline = fields.Date()
    is_completed = fields.Boolean()
    user_id = fields.Int(required=True)
