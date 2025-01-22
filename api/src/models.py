from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_id = fields.IntField(pk=True)
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


class QuestradeApiKeys(Model):
    key_id = fields.IntField(pk=True)  # Explicit primary key
    user_id = fields.ForeignKeyField("models.Users", related_name="questrade_api_keys", on_delete=fields.CASCADE)
    api_key = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "questrade_api_keys"