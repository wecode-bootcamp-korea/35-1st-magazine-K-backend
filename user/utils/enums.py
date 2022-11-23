from enum import Enum


class UserEnum(Enum):
    """
    일반 회원와 관리자를 구별하기 위한 Enum

    일반 회원과 관리자가 접근할 수 있는 기능을 구별하기 위해 생성
    """

    USER = "user"
    ADMIN = "admin"
