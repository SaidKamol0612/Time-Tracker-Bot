from sqlalchemy import BigInteger, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.enums import UserRoles

from .base import Base


class User(Base):
    tg_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String())
    role: Mapped[UserRoles] = mapped_column(
        Enum(
            UserRoles,
            name="role",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            native_enum=False,
        ),
        default=UserRoles.WORKER,
    )
