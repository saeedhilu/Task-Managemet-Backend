from rest_framework import serializers
from users.models import CustomUser
from tasks.models import Task,Tag
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="confirm Password")
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='member')
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email',  'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role= validated_data['role'],
            password = validated_data['password']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    def validate(self, attrs):
        user = CustomUser.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError({"email": "Invalid credentials."})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": "Invalid credentials."})
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)
    created_by = serializers.ReadOnlyField(source='created_by.username')  
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        partial = self.context.get('partial', False)
        
        if partial:
            for field, value in validated_data.items():
                setattr(instance, field, value)
        else:
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.status = validated_data.get('status', instance.status)
            instance.priority = validated_data.get('priority', instance.priority)
            instance.due_date = validated_data.get('due_date', instance.due_date)
            instance.assigned_to.set(validated_data.get('assigned_to', instance.assigned_to.all()))
            instance.project = validated_data.get('project', instance.project)
            instance.tags.set(validated_data.get('tags', instance.tags.all()))
        
        instance.save()
        return instance
