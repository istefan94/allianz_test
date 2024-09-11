import requests
import urllib.parse
from logger import setup_logger

logger = setup_logger(__name__)

class ApiClient:

    def __init__(self) -> None:
        self.url = "https://wps-interview.azurewebsites.net/api/v1/user"

    def _handle_response(self, response):
        """
        Handle the response, raise an error if the request failed, and return the JSON content.

        :param response: The response object from the requests library.
        :return: Parsed JSON response or the raw text if not JSON.
        """
        try:
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response content: {response.text}")
            return None

        try:
            return response.json()  # Return JSON response if possible
        except ValueError:
            return response.text  # If response is not JSON, return raw text

    def get_users(self):
        response = self._handle_response(requests.get(self.url))
        logger.info(response)
        return response

    def get_user(self, user_id: int):
        url = f"{self.url}/{user_id}"
        response = self._handle_response(requests.get(url))
        logger.info(response)
        return response
    
    def create_user(self, first_name: str, last_name: str, email: str, company: str, external: bool):
        params = {
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "company": company,
            "is_external": external
            }
        params = urllib.parse.urlencode(params)
        response = self._handle_response(requests.post(self.url, params=params))
        logger.info(response)
        return response

    def update_user(self, 
                    user_id: int, 
                    first_name=None,
                    last_name=None, 
                    email=None, 
                    company=None, 
                    external=None):
        url = f"{self.url}/{user_id}"
        params = {"id": user_id}
        if first_name:
            params["firstname"] = first_name
        if last_name:
            params["lastname"] = last_name
        if email:
            params["email"] = email
        if company:
            params["company"] = company
        if external:
            params["is_external"] = external
        params = urllib.parse.urlencode(params)
        response = self._handle_response(requests.put(url=url, params=params))
        logger.info(response)
        return response

            
