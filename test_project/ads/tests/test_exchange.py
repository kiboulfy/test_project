import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_exchangeproposal(api_client, user, ad, ad2):
    api_client.force_authenticate(user=user)
    url = reverse('exchangeproposalcreateview')
    data = {
        "ad_sender": ad.id,
        "ad_receiver": ad2.id,
        "comment": "Предлагаю обмен"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["comment"] == "Предлагаю обмен"
    

@pytest.mark.django_db
def test_update_exchangeproposal_status(api_client, user2, exchangeproposal):
    api_client.force_authenticate(user=user2)
    url = reverse('exchangeproposalupdateview', args=[exchangeproposal.id])
    data = {
        "status": "accepted"
    }
    response = api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["status"] == "accepted"

@pytest.mark.django_db
def test_exchangeproposal_list_only_user_related(api_client, user, ad, exchangeproposal):
    api_client.force_authenticate(user=user)
    url = reverse('exchangeproposallist')
    response = api_client.get(url)
    assert response.status_code == 200
    for item in response.data['results']:
        assert item['ad_sender'] == ad.id or item['ad_receiver'] == ad.id

@pytest.mark.django_db
def test_exchangeproposal_create_invalid_sender(api_client, user2, ad, ad2):
    api_client.force_authenticate(user=user2)
    url = reverse('exchangeproposalcreateview')
    data = {
        "ad_sender": ad.id,  
        "ad_receiver": ad2.id,
        "comment": "go trade"
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert "Вы можете использовать только свои объявления" in str(response.data)