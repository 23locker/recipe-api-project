from pydoc import describe

from tortoise import Model, fields


class Subtitute(Model):
    id = fields.IntField(pk=True)
    original_ingridient: fields.ForeignKeyRelation["Ingredient"] = (
        fields.ForeignKeyField(
            "models.Ingridient",
            related_name="subtitues",
        )
    )
    subtitutes_ingridient_id: fields.ForeignKeyRelation["Ingredient"] = (
        fields.ForeignKeyField("models.ingridient")
    )
    coefficient = fields.FloatField(description="Коэффициент замены от 0 до 3")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "subtitutes"
        unique_together = (("original_ingridient", "subtitute_ingridient"),)
