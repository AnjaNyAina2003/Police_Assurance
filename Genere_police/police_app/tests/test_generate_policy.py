import datetime
import jwt
import pytest
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.db import connection
from django.urls import reverse
from rest_framework.test import APIClient

from agence_app.models import Agence_assurance
from auth_app.models import User
from branch_app.models import Branche_assurance
from client_app.models import Clients


@pytest.mark.django_db(transaction=True)
def test_generate_policy_concurrently():
    agence = Agence_assurance.objects.create(nom_agence='Agence test', ville='Tana')
    user = User.objects.create_user(username='testuser', email='test@example.com',
                                    password='testpass123', agence=agence, role='user')
    branche = Branche_assurance.objects.create(nom_branche='Auto', prefixe='AU')
    cli = Clients.objects.create(nom_client='Doe', prenom_client='John',
                                 telephone='0340000000', adresse='Tana')

    token = jwt.encode(
        {'id': user.id, 'role': user.role,
         'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)},
        settings.JWT_SECRET, algorithm='HS256')
    url = reverse('Generer une police assurance')

    def create_policy():
        try:
            api = APIClient()
            api.cookies['jwt'] = token
            r = api.post(url, {'branche_id': branche.id,
                               'num_compte_client': cli.num_compte_client,
                               'duree_couverture': 12}, format='json')
            assert r.status_code == 201, r.data
            return r.data['num_police']
        finally:
            connection.close()

    with ThreadPoolExecutor(max_workers=3) as ex:
        results = [f.result() for f in [ex.submit(create_policy) for _ in range(5)]]

    assert len(results) == len(set(results))