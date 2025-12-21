from tortoise import Model, fields


class Ingridient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_lenght=100, unique=True)
    calories_per_100g = fields.FloatField()
    protein_per_100g = fields.FloatField()
    fat_per_100g = fields.FloatField()
    carbs_per_100g = fields.FloatField()
    category: fields.ForeignKeyRelation["Category"] = fields.ForeignKeyField(
        "models.Category", related_name="ingridients"
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "ingridients"
