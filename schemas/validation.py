from marshmallow import Schema, fields


# Schemas for validation
class ResumeSchema(Schema):
    resume = fields.Str(required=True)

class JobDescriptionSchema(Schema):
    job_description = fields.Str(required=True)
    callbackUrl = fields.Str(required=True)

class RankResumeSchema(Schema):
    resume = fields.Dict(required=True)
    job_description = fields.Dict(required=True)
    callbackUrl = fields.Str(required=True)

class EmbaddingSchema(Schema):
    data = fields.Str(required=True)
    callbackUrl = fields.Str(required=True)
