from pydoc import describe

from tortoise import Model, fields


class Substitute(Model):
    id = fields.IntField(pk=True)
    original_ingredient = fields.ForeignKeyField(
        "models.Ingredient", related_name="substitutes_from"
    )
    substitute_ingredient = fields.ForeignKeyField(
        "models.Ingredient", related_name="substitutes_to"
    )
    coefficient = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "substitutes"
        unique_together = (("original_ingredient", "substitute_ingredient"),)
