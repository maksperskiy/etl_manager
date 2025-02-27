from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from .forms import LoginForm, SignUpForm


class UserLoginView(APIView):
    def post(self, request):
        try:
            form = LoginForm(data=json.loads(request.body))
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return Response(
                        {
                            "message": "Login successful",
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "message": "Invalid credentials or User doesn't exist.",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(
                    {
                        "message": "Invalid params",
                        "details": json.loads(form.errors.as_json()),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                    {
                        "message": "Bad request"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                ) 


class UserSignUpView(APIView):
    def post(self, request):
        try:
            form = SignUpForm(data=json.loads(request.body))
            if form.is_valid():
                user = form.save()
                login(request, user)
                return Response(
                    {
                        "message": "Login successful",
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": f"Invalid params",
                        "details": json.loads(form.errors.as_json()),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                    {
                        "message": "Bad request"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                ) 

class UserLogoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
