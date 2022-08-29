from django.contrib.auth import get_user_model


UserModel = get_user_model()
class UserBackend(object):

    def authenticate(self, auth_input=None, password=None):
        try:
            user = UserModel.objects.get(username=auth_input)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=auth_input)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            except UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(phone=auth_input)
                    if user.check_password(password) and self.user_can_authenticate(user):
                        return user
                except:
                    print("1")
                    return None
            print("2")
            return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None) # 유저가 활성화 되었는지
        return is_active or is_active is None # 유저가 없는 경우 is_active는 None이므로 True

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id) # 유저를 pk로 가져온다
        except UserModel.DoesNotExist:
            return None