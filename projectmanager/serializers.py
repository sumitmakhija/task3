from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, ProjectMember, Task, Comment

User = get_user_model()

# ---------------------------
# User Serializer
# ---------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


# ---------------------------
# Register Serializer
# ---------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# ---------------------------
# Project Serializer
# ---------------------------
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        read_only_fields = ['id', 'created_at']


# ---------------------------
# Project Member Serializer
# ---------------------------
class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='project', write_only=True
    )

    class Meta:
        model = ProjectMember
        fields = ['id', 'project_id', 'user_id', 'user', 'role']


# ---------------------------
# Task Serializer
# ---------------------------
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, allow_null=True, required=False
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assigned_to', 'assigned_to_id', 'project', 'created_at', 'due_date'
        ]
        read_only_fields = ['id', 'created_at']


# ---------------------------
# Comment Serializer
# ---------------------------
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source='task', write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'user_id', 'task_id', 'created_at']
        read_only_fields = ['id', 'created_at']
