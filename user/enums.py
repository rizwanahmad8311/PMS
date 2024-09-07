from enum import Enum, IntEnum


class UserStatusChoices(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"


class UserRoleChoices(IntEnum):
    SUPER_ADMIN = 1
    DOCTOR = 2
    PATIENT = 3


class UserGenderChoices(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
