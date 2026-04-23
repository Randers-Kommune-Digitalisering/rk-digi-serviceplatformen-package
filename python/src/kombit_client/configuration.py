import os

# Constants
CVR_NUMBER = os.environ.get('CVR_NUMBER')

# Certificates
_CERT_BASE_PATH = os.environ.get('CERT_BASE_PATH')
CLIENT_CERT_PATH = os.path.join(_CERT_BASE_PATH, os.environ['CLIENT_CERT']) if (_CERT_BASE_PATH and (env := os.environ.get('CLIENT_CERT'))) else None
CLIENT_CERT_BASE64 = os.environ.get('CLIENT_CERT_BASE64', None)
CLIENT_CERT_PASS = os.environ.get('CLIENT_CERT_PASS', None)
ROOT_CERT_PATH = os.path.join(_CERT_BASE_PATH, os.environ.get('ROOT_CERT', 'CA-Den Danske Stat OCES rod-CA.cer'))
ACCESS_CONTROL_CERT_PATH = os.path.join(_CERT_BASE_PATH, os.environ.get('ACCESS_CONTROL_CERT', 'ADG_PROD_Adgangsstyring_2.cer'))
SIGNING_CERT_PATH = os.path.join(_CERT_BASE_PATH, os.environ.get('SIGNING_CERT', 'new_SP_PROD_Signing_1.cer'))
YDELSESINDEKS_CERT_PATH = os.path.join(_CERT_BASE_PATH, os.environ.get('YDELSESINDEKS_CERT', 'YDI_PROD_Ydelsesindeks_2.cer'))

# Endpoints
STS_ENDPOINT_ADDRESS = os.environ.get('STS_ENDPOINT_ADDRESS', 'https://n2adgangsstyring.stoettesystemerne.dk/runtime/services/kombittrust/14/certificatemixed')
STS_ENDPOINT_ID = os.environ.get('STS_ENDPOINT_ID', 'http://saml.n2adgangsstyring.stoettesystemerne.dk/runtime')
