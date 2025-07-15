# ads/tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from ads.models import Ad, Category, Condition, ExchangeProposal

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="1234")

@pytest.fixture
def user2(db):
    return User.objects.create_user(username="user2", password="1234")

@pytest.fixture
def category_tech(db):
    return Category.objects.create(name="Электроника")

@pytest.fixture
def category_books(db):
    return Category.objects.create(name="Книги")

@pytest.fixture
def condition_new(db):
    return Condition.objects.create(name="Новое")

@pytest.fixture
def condition_used(db):
    return Condition.objects.create(name="Б/у")

@pytest.fixture
def ad(user, category_tech, condition_used):
    return Ad.objects.create(
        user=user,
        title="Телефон",
        description="Рабочий смартфон",
        category=category_tech,
        condition=condition_used
    )

@pytest.fixture
def ad2(user2, category_books, condition_new):
    return Ad.objects.create(
        user=user2,
        title="Книга",
        description="Фантастика",
        category=category_books,
        condition=condition_new
    )

@pytest.fixture
def exchangeproposal(ad, ad2):
    return ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=ad2,
        comment='Тестовое предложение',
    )