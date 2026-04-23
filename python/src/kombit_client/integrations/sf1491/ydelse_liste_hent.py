import json

from kombit_client.configuration import (
    CVR_NUMBER,
    ACCESS_CONTROL_CERT_PATH,
    CLIENT_CERT_PATH,
    CLIENT_CERT_PASS,
    YDELSESINDEKS_CERT_PATH,
    STS_ENDPOINT_ADDRESS,
    STS_ENDPOINT_ID,
)
from kombit_client.dotnet._bridge import YdelseListHentClient as _YdelseListHentClient


class YdelseListeHentClient(_YdelseListHentClient):
    """Python wrapper around the YdelseListHentClient from the KombitServiceClient .NET library."""

    def __init__(
        self,
        cvr: str = CVR_NUMBER,
        sts_certificate_file_path: str = ACCESS_CONTROL_CERT_PATH,
        sts_endpoint_address: str = STS_ENDPOINT_ADDRESS,
        sts_entity_identifier: str = STS_ENDPOINT_ID,
        service_certificate_file_path: str = YDELSESINDEKS_CERT_PATH,
        service_endpoint: str = "https://ydelsesindeks.stoettesystemerne.dk/ydelselistehent/2",
        service_endpoint_id: str = "http://entityid.kombit.dk/service/ydelselistehent/1",
        client_certificate_file_path: str = CLIENT_CERT_PATH,
        client_certificate_password: str | None = CLIENT_CERT_PASS,
        debug_mode: bool = False,
    ) -> None:
        if not all([cvr, sts_certificate_file_path, sts_endpoint_address, sts_entity_identifier, service_certificate_file_path, service_endpoint, service_endpoint_id, client_certificate_file_path]):
            raise ValueError("Missing required configuration for YdelseListeHentClient.")
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

    def effektuering_hent(
        self,
        cpr: str,
        start_dato: str | None = None,
        slut_dato: str | None = None,
    ) -> dict:
        """
        Calls the .NET EffektueringHent method and returns the parsed JSON as dict.

        Expected date format (if provided): 'yyyy-MM-dd' (e.g. '2026-04-22').
        """
        res = self.EffektueringHent(
            cpr=cpr,
            startDato=start_dato,
            slutDato=slut_dato,
        ).Result
        return json.loads(res)
