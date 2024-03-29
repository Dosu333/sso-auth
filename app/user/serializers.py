from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import PermissionDenied
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from email_validator import validate_email, EmailNotValidError
from boxin.models import BoxinHero
from wallet.models import Wallet
from .models import Token, User
from .tasks import send_new_user_email, send_password_reset_email
from wallet.vba import VirtualBankAccount


def resend_mail(user):
    token = Token.objects.filter(user=user).first()
    user_data = {'id': user.id, 'email': user.email, 'fullname': f"{user.lastname} {user.firstname}",
                    'url': f"{settings.CLIENT_URL}/signup/?token={token.token}"}
    send_new_user_email(user_data)


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'firstname', 'lastname', 'email', 'phone','roles',
                  'businessname','image', 'verified', 'referred_by','last_login', 'created_at', 'address', 'state']


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'firstname', 'lastname', 'verified',
                  'phone', 'image', 'roles', 'referred_by','last_login', 'created_at', 'businessname', 'address', 'state')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'last_login': {'read_only': True}}

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email:
            email = attrs['email'].lower().strip()
            if get_user_model().objects.filter(email=email).exists():
                raise serializers.ValidationError('Email already exists')
            try:
                valid = validate_email(attrs['email'])
                attrs['email'] = valid.email
                return super().validate(attrs)
            except EmailNotValidError as e:
                raise serializers.ValidationError(e)
        return super().validate(attrs)

    def create(self, validated_data):
        user = None
        referral =  validated_data.pop('referred_by')
        
        if referral:
            if  BoxinHero.objects.filter(code=referral).exists():
                hero = BoxinHero.objects.get(code=referral)
                user = User.objects.create_user(referred_by_hero=hero.fullname, **validated_data)
            else:
                store = User.objects.get(id=str(referral))
                user = User.objects.create_user(referred_by_user=store,**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        acct_no = VirtualBankAccount(first_name=user.firstname, last_name=user.lastname, phone=user.phone, email=user.email).create_virtual_bank_account()
        Wallet.objects.create(owner=user, virtual_account_number=acct_no['account_no'], virtual_bank=acct_no['bank'], virtual_bank_account_name=acct_no['account_name'], customer_code=acct_no['customer'])

        token, _ = Token.objects.update_or_create(
            user=user, token_type='ACCOUNT_VERIFICATION',
            defaults={'user': user, 'token_type': 'ACCOUNT_VERIFICATION', 'token': get_random_string(120)})
        user_data = {'id': user.id, 'email': user.email, 'fullname': str(user.firstname).capitalize(),
                     'url': f"{settings.CLIENT_URL}/signup/?token={token.token}"}
        send_new_user_email.delay(user_data)
        return user

    def update(self, instance, validated_data):
        # user = self.context['request'].user
        instance = super().update(instance, validated_data)
        if validated_data.get('password', False):
            instance.set_password(validated_data.get('password'))
            instance.save()
        return instance


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        if not user.verified:
            resend_mail(user)
            raise exceptions.AuthenticationFailed(
                _('Account not yet verified.'), code='authentication')
        token = super().get_token(user)
        # Add custom claims
        token.id = user.id
        token['email'] = user.email
        token['roles'] = user.roles
        token['businessname'] = user.businessname
        token['address'] = user.address
        token['state'] = user.state
        if user.firstname and user.lastname:
            token['firstname'] = user.firstname
            token['lastname'] = user.lastname
            token['fullname'] = user.firstname + ' ' + user.lastname
        if user.image:
            token['image'] = user.image.url
        token['phone'] = user.phone
        user.save_last_login()
        return token


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email:
            user = authenticate(
                request=self.context.get('request'),
                username=email.lower().strip(),
                password=password
            )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs


class VerifyTokenSerializer(serializers.Serializer):
    """Serializer for token verification"""
    token = serializers.CharField(required=True)


class InitializePasswordResetSerializer(serializers.Serializer):
    """Serializer for sending password reset email to the user"""
    email = serializers.CharField(required=True)


class CreatePasswordSerializer(serializers.Serializer):
    """Serializer for password change on reset"""
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
