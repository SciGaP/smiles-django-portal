# smiles/airavata_portal_service.py
import requests
from django.urls import reverse

class AiravataPortalAPIService:
    def __init__(self, request):
        self.request = request
        self.api_root = request.build_absolute_uri("/api")

    def get_user_profiles(self):
        """
        /api/user-profiles/
        """
        url = f"{self.api_root}/user-profiles/"
        return self._get(url)

    def get_groups(self):
        """
         /api/groups/
        """
        url = f"{self.api_root}/groups/"
        return self._get(url)

    def get_one_group(self, group_id):
        """
        /api/groups/<group_id>/
        """
        url = f"{self.api_root}/groups/{group_id}/"
        return self._get(url)

    def _get(self, url):
        session = requests.Session()
        if self.request.COOKIES:
            cookie_dict = {k: v for k, v in self.request.COOKIES.items()}
            session.cookies.update(cookie_dict)

        resp = session.get(url)
        resp.raise_for_status()
        return resp.json()
