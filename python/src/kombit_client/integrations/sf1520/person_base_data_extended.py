import json
from kombit_client.configuration import (
    CVR_NUMBER,
    ACCESS_CONTROL_CERT_PATH,
    CLIENT_CERT_PATH,
    CLIENT_CERT_PASS,
    SP_SIGNING_CERT_PATH,
    STS_ENDPOINT_ADDRESS,
    STS_ENDPOINT_ID
)
from kombit_client.dotnet._bridge import PersonBaseDataExtendedClient as _PersonBaseDataExtendedClient


class PersonBaseDataExtendedClient(_PersonBaseDataExtendedClient):
    """A Python wrapper around the PersonBaseDataExtendedClient from the KombitServiceClient .NET library."""
    def __init__(
        self,
        cvr: str = CVR_NUMBER,
        sts_certificate_file_path: str = ACCESS_CONTROL_CERT_PATH,
        sts_endpoint_address: str = STS_ENDPOINT_ADDRESS,
        sts_entity_identifier: str = STS_ENDPOINT_ID,
        service_certificate_file_path: str = SP_SIGNING_CERT_PATH,
        service_endpoint: str = "https://prod.serviceplatformen.dk/service/CPR/PersonBaseDataExtended/5",
        service_endpoint_id: str = "http://cpr.serviceplatformen.dk/service/personbasedataextended/5",
        client_certificate_file_path: str = CLIENT_CERT_PATH,
        client_certificate_password: str | None = CLIENT_CERT_PASS,
        debug_mode: bool = False,
    ) -> None:
        if not all([cvr, sts_certificate_file_path, sts_endpoint_address, sts_entity_identifier, service_certificate_file_path, service_endpoint, service_endpoint_id, client_certificate_file_path]):
            raise ValueError("Missing required configuration for PersonBaseDataExtendedClient.")
        super().__init__(
            stsCertificateFilePath=sts_certificate_file_path,
            stsEndpointAddress=sts_endpoint_address,
            stsEntityIdentifier=sts_entity_identifier,
            serviceCertificateFilePath=service_certificate_file_path,
            serviceEndpoint=service_endpoint,
            serviceEndpointId=service_endpoint_id,
            clientCertificateFilePath=client_certificate_file_path,
            clientCertificatePassword=client_certificate_password,
            cvr=cvr,
            debugMode=debug_mode,
        )

    def person_lookup(self, pnr: str) -> dict:
        """Lookup a CPR number and return the result as a dictionary."""
        res = self.PersonLookup(PNR=pnr).Result
        return json.loads(res)
