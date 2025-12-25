from tortoise import Model, fields


class Ingredient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    calories_per_100g = fields.FloatField()
    protein_per_100g = fields.FloatField()
    fat_per_100g = fields.FloatField()
    carbs_per_100g = fields.FloatField()
    category = fields.ForeignKeyField("models.Category", related_name="ingredients")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "ingredients"
