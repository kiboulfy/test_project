import pytest
from django.urls import reverse
from ads.models import Ad

@pytest.mark.django_db
def test_create_ad(api_client, user, category_tech, condition_used):
    api_client.force_authenticate(user=user)
    url = reverse('adapilist')
    data = {
        "title": "Новый телефон",
        "description": "Очень хороший",
        "category": category_tech.id,
        "condition": condition_used.id
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "Новый телефон"
    assert response.data["category"] == category_tech.id

@pytest.mark.django_db
def test_edit_ad(api_client, user, ad):
    api_client.force_authenticate(user=user)
    url = reverse('adapiupdateordestroy', args=[ad.id])
    data = {
        "title": "Отредактированный телефон",
        "description": ad.description,
        "category": ad.category.id,
        "condition": ad.condition.id
    }
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data["title"] == "Отредактированный телефон"

@pytest.mark.django_db
def test_delete_ad(api_client, user, ad):
    api_client.force_authenticate(user=user)
    url = reverse('adapiupdateordestroy', args=[ad.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    with pytest.raises(Ad.DoesNotExist):
        Ad.objects.get(id=ad.id)

@pytest.mark.django_db
def test_search_ads(api_client, user, ad, ad2):
    url = reverse('adapilist') + '?search=Телефон'
    response = api_client.get(url)
    assert response.status_code == 200
    titles = [item['title'] for item in response.data['results']]
    assert "Телефон" in titles
    assert "Книга" not in titles

@pytest.mark.django_db
def test_delete_ad_forbidden_for_not_owner(api_client, user2, ad):
    api_client.force_authenticate(user=user2)
    url = reverse('adapiupdateordestroy', args=[ad.id])
    response = api_client.delete(url)
    assert response.status_code == 403