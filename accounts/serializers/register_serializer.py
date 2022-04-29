from rest_framework import serializers

from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['username','password','password2','first_name','last_name','email','avatar','phone_num']

    def validate(self, attrs):
        if attrs['password'] == attrs['password2']:
            return super().validate(attrs)
        raise serializers.ValidationError({"password":"passwords do not match"})
    
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user