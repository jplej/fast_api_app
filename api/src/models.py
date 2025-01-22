from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_id = fields.IntField(pk=True, generated=True)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=150, unique=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    hashed_password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    role = fields.CharField(max_length=50)
    phone_number = fields.CharField(max_length=20, null=True)

    class Meta:
        table = "users"


class EnrichedStocks(Model):
    symbol = fields.CharField(pk=True, max_length=10, unique=True)
    name = fields.CharField(max_length=255, null=True)
    currency = fields.CharField(max_length=10, null=True)
    founding_year = fields.IntField(null=True)
    country = fields.CharField(max_length=100, null=True)
    founder = fields.CharField(max_length=255, null=True)
    current_ceo = fields.CharField(max_length=255, null=True)
    market_cap = fields.CharField(max_length=50, null=True)
    url_website = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    industry = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "enriched_stocks"