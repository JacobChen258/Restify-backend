from rest_framework import serializers

from accounts.models import User

class EditProfileSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = User
        fields = ['password','password2','first_name','last_name','email','avatar','phone_num']
        extra_kwargs = {
            "password":{'required':False}
        }

    def validate(self, attrs):
        if 'password' in attrs.keys():
            try:
                if attrs['password'] != '':
                    if attrs['password'] != attrs['password2']:
                        raise serializers.ValidationError({"password":"passwords do not match"})
            except:
                raise serializers.ValidationError({"password":"missing second password"})
        return super().validate(attrs)
    
    def pop_password(self):
        if "password" in self.validated_data.keys():
            self.validated_data.pop("password2")
            return self.validated_data.pop("password")
        return ''
    
    def check_avatar(self):
        if "avatar" in self.validated_data.keys():
            return True
        return False

class GetProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','avatar','phone_num']
