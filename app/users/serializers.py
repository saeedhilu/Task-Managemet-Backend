from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import Comment, Mention, Notification


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, label="confirm Password"
    )
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default="member")

    class Meta:
        model = CustomUser
        fields = ("username", "password", "password2", "email", "role")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        if CustomUser.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
            password=validated_data["password"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    def validate(self, attrs):
        user = CustomUser.objects.filter(email=attrs["email"]).first()
        print(user.password)
        if not user:
            raise serializers.ValidationError({"email": "Invalid credentials."})
        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Invalid credentials."})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "username"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention
        fields = "__all__"
        read_only_fields = ["mentioned_by", "created_at"]

    def create(self, validated_data):
        validated_data["mentioned_by"] = self.context["request"].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]
