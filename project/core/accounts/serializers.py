from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "password"
        ]

    def validate_password(self, password):
        l = len(password)
        if ' ' in password or l < 8 or l > 20 or not password:
            raise serializers.ValidationError(
                ' '.join([
                    "Enter a strong password.",
                    "This value must contain between 8 to 20 characters.",
                    "This value must include a letter, a number, and a special character."
                ])
            )

        alpha = False
        digits = False
        spchar = False
        for c in password:
            if not alpha and c.isalpha():
                alpha = True
            if not digits and c.isdigit():
                digits = True
            if not spchar and not c.isalnum():
                spchar = True

        if alpha and digits and spchar:
            return password
        raise serializers.ValidationError(
            ' '.join([
                "Enter a strong password.",
                "This value must contain between 8 to 20 characters.",
                "This value must include a letter, a number, and a special character."
            ])
        )
