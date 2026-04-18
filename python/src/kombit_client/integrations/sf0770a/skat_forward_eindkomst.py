import json

from kombit_client.configuration import (
    ACCESS_CONTROL_CERT_PATH,
    CLIENT_CERT_PATH,
    CLIENT_CERT_PASS,
    SIGNING_CERT_PATH,
    STS_ENDPOINT_ADDRESS,
    STS_ENDPOINT_ID
)
from kombit_client.dotnet._bridge import SKATForwardEIndkomstClient as _SKATForwardEIndkomstClient


class SKATForwardEIndkomstClient(_SKATForwardEIndkomstClient):
    """A Python wrapper around the SKATForwardEIndkomstClient from the KombitServiceClient .NET library."""
    def __init__(
        self,
        cvr: str,
        virksomhed_se_nummer_identifikator: str,
        abonnement_type_kode: str,
        abonnent_type_kode: str,
        adgang_formaal_type_kode: str,
        sts_certificate_file_path: str = ACCESS_CONTROL_CERT_PATH,
        sts_endpoint_address: str = STS_ENDPOINT_ADDRESS,
        sts_entity_identifier: str = STS_ENDPOINT_ID,
        service_certificatefile_file_path: str = SIGNING_CERT_PATH,
        service_endpoint: str = "https://prod.serviceplatformen.dk/service/SKAT/EIndkomst/4",
        service_endpoint_id: str = "http://entityid.kombit.dk/service/sp/skatforwardeindkomstservice/4",
        client_certificate_file_path: str = CLIENT_CERT_PATH,
        client_certificate_password: str | None = CLIENT_CERT_PASS,
        debug_mode: bool = False,
    ) -> None:
        super().__init__(
            virksomhedSENummerIdentifikator=virksomhed_se_nummer_identifikator,
            abonnementTypeKode=abonnement_type_kode,
            abonnentTypeKode=abonnent_type_kode,
            adgangFormaalTypeKode=adgang_formaal_type_kode,
            stsCertificateFilePath=sts_certificate_file_path,
            stsEndpointAddress=sts_endpoint_address,
            stsEntityIdentifier=sts_entity_identifier,
            serviceCertificateFilePath=service_certificatefile_file_path,
            serviceEndpoint=service_endpoint,
            serviceEndpointId=service_endpoint_id,
            clientCertificateFilePath=client_certificate_file_path,
            clientCertificatePassword=client_certificate_password,
            cvr=cvr,
            debugMode=debug_mode,
        )

    def indkomstoplysninger_laes(
            self,
            person_civil_registration_identifier: str,
            soege_aar_maaned_fra_kode: str,
            soege_aar_maaned_til_kode: str
    ) -> dict:
        res = self.IndkomstoplysningerLaes(
            PersonCivilRegistrationIdentifier=person_civil_registration_identifier,
            SoegeAarMaanedFraKode=soege_aar_maaned_fra_kode,
            SoegeAarMaanedTilKode=soege_aar_maaned_til_kode
        ).Result
        return json.loads(res)
