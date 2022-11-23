from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    # All user
    def create_user(self, username, nickname, password=None, **extra_fields):

        if username is None:
            raise TypeError('Users must have a username.')

        if nickname is None:
            raise TypeError('Users must have a nickname.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(
            username=username,
            nickname=nickname,
            # 중복 최소화를 위한 정규화
            **extra_fields
        )

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()

        return user

    # admin user
    def create_superuser(self, username, nickname, password, **extra_fields):

        if password is None:
            raise TypeError('Superuser must have a password.')

        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(username, nickname, password, **extra_fields)
        # 관리자로 지정
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
