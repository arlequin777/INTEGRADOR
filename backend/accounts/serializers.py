from rest_framework import serializers
from .models import CustomUser, Rol

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        role = validated_data.get('role', 'OPERADOR')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["role"]

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError("Rol inválido.")
        return value

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id", "nombre"]

class UserSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), source="rol", write_only=True, required=False
    )

    class Meta:
        model = CustomUser
        fields = ["id", "nombre", "email", "rol", "rol_id", "fecha_creacion"]