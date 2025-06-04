import requests
import urllib3
import logging
import os
import dotenv

# Disable SSL warnings if necessary
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv()

class VSphereClient:
    def __init__(self, vsphere_uri, username, password, verify_ssl=True):
        self.vsphere_uri = vsphere_uri
        self.auth = (username, password)
        self.verify_ssl = verify_ssl
        self.session = self._init_session()
        self.is_authenticated = False

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        session.verify = self.verify_ssl
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        return session

    def _authenticate(self):
        response = self.session.post(f"{self.vsphere_uri}/rest/com/vmware/cis/session", auth=self.auth)
        if response.status_code == 200:
            # session_token = response.json()["value"]
            # self.session.headers.update({"vmware-api-session-id": session_token})
            LOGGER.debug("Authentication successful.")
            self.is_authenticated = True
        else:
            LOGGER.error("Failed to authenticate. Status code: %s", response.status_code)
            self.is_authenticated = False
    
    def get_vms(self):
        response = self.session.get(f"{self.vsphere_uri}/rest/vcenter/vm")
        if response.status_code == 200:
            return response.json()
        else:
            LOGGER.error("Failed to retrieve VMs. Status code: %s", response.status_code)
            return None
    
# Example usage
if __name__ == "__main__":
    vsphere_uri = os.getenv("VSPHERE_URI")
    username = os.getenv("VSPHERE_USERNAME")
    password = os.getenv("VSPHERE_PASSWORD")
    
    client = VSphereClient(vsphere_uri, username, password, verify_ssl=False)
    client._authenticate()
    vm_list = client.get_vms()
    print(vm_list)
