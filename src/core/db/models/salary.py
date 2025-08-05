from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Salary(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total: Mapped[int] = mapped_column(Integer, default=0)
    last_entered: Mapped[int] = mapped_column(Integer, default=0)
    
    user: Mapped["User"] = relationship(back_populates="salary")