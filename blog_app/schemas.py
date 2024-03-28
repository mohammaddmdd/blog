# app_name/schemas.py
from ninja import Schema

class PostSchema(Schema):
    id: int
    title: str
    content: str
    # Add more fields as necessary