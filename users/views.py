"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import coreapi
import coreschema
from django.contrib.auth import authenticate
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema

# JWT Authentication is used to handle account activation
# https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication
from rest_framework_simplejwt.tokens import RefreshToken
# https://londonappdeveloper.com/json-web-tokens-vs-token-authentication/


from users.serializers import LoginSerializer, ChangePasswordSerializer


class LoginViewAPI(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Custom login view to authenticate user and return JWT tokens.
    """
    serializer_class = LoginSerializer
    schema = ManualSchema(
        description="Log in to get the access token",
        fields=[
            coreapi.Field(
                name="email",
                required=True,
                location="form",
                schema=coreschema.String(),
                description="User email"
            ),
            coreapi.Field(
                name="password",
                required=True,
                location="form",
                schema=coreschema.String(),
                description="User password"
            ),
        ])

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "user": {
                "email": user.email,
                "full_name": user.full_name,
            }
        }, status=status.HTTP_200_OK)


class ChangePasswordViewAPI(generics.GenericAPIView):
    """
    Change the password by providing email, old password, and new password.
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Authenticate the user with the old password
        user = authenticate(request, email=email, password=old_password)

        if not user:
            return Response({"error": "Invalid email or old password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate and set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
