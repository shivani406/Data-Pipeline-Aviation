import requests
import time
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

load_dotenv()  # Load environment variables from .env file

class DataSubscriber(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

class open_sky_api(DataSubscriber):
    def __init__(self):
        self.api_url = "https://opensky-network.org/api/states/all"
        self.token_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
        
        self.client_id = os.getenv('OPEN_SKY_CLIENT_ID')
        self.client_secret = os.getenv('OPEN_SKY_CLIENT_SECRET')
        
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self):
        """Exchanges Client ID/Secret for an Access Token (Step 1)."""

        print("Fetching new Access Token...")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data['access_token']

        # Set expiry (usually 300 seconds)
        self.token_expires_at = time.time() + token_data.get('expires_in', 300)
        return self.access_token

    def fetch_data(self):
            """Uses the token to get the actual flight data (Step 2)."""
            try:
                # Refresh token if it doesn't exist or is expired
                if not self.access_token or time.time() >= self.token_expires_at:
                    self.get_access_token()

                headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }
                
                response = requests.get(self.api_url, headers=headers)
                response.raise_for_status()
                return response.json()
                
            except Exception as e:
                print(f"Error in Oauth : {e}")
                
                # Optional: Fallback to anonymous if OAuth fails
                return None
# ADD Further API sources as needed by creating new classes that inherit from DataSubscriber and implement the fetch_data method.

def get_source(source_name):
    sources = {
        "opensky": open_sky_api()
    }
    return sources.get(source_name)




