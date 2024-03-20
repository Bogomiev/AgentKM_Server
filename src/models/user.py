from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from src.db.postgresdb import SqlBase
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, SqlBase):
    username = mapped_column(String(50), nullable=False, index=True, comment='Имя пользователя')
