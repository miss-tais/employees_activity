import requests

from employees_activity.settings import settings_loader
from employees_activity.exceptions import HubstaffAuthenticationError


class HubstaffAuth(object):
    """
    Hubstaff authentication
    """

    def __init__(self):
        self.request_headers = {'App-Token': settings_loader.hubstaff_app_token}

    def auth(self, email, password):
        """
        Hubstaff authentication with hubstaff api

        :param email: User email
        :param password: User password
        :return: Hubstaff authentication token
        """
        url = '{api_url}/auth'.format(api_url=settings_loader.hubstaff_api_url)
        r = requests.post(url, {'email': email, 'password': password}, headers=self.request_headers)

        if r.status_code == requests.codes.ok:
            return r.json()['user']['auth_token']
        else:
            raise HubstaffAuthenticationError(r.json().get('error', ''))


class HubstaffAPI(object):
    """
    Hubstaff API
    """

    def __init__(self, auth_token):
        self.request_headers = {
            'App-Token': settings_loader.hubstaff_app_token,
            'Auth-Token': auth_token
        }

    def process_api_call(self, url, params):
        url = '{api_url}{url}'.format(api_url=settings_loader.hubstaff_api_url, url=url)
        response = requests.get(url, params=params, headers=self.request_headers)

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise HubstaffAuthenticationError(response.json().get('error', ''))

    def fetch_custom_team_report_by_date(self, start_date, end_date, **kwargs):
        """
        Hubstaff custom team report grouped by date

        :param start_date: Report start date
        :param end_date: Report end date
        :param kwargs: Additional arguments
        :return: Result of Hubstaff '/custom/by_date/team' API request
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        params.update(kwargs)
        return self.process_api_call('/custom/by_date/team', params)