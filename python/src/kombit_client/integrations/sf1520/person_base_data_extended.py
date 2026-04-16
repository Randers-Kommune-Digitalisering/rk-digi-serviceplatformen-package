import json

from kombit_client.dotnet._bridge import _PersonBaseDataExtendedClient

__all__ = ["PersonBaseDataExtendedClient"]


class PersonBaseDataExtendedClient(_PersonBaseDataExtendedClient):
    """A Python wrapper around the CPRPersonLookup service from the KombitServiceClient .NET library."""
    def __init__(
        self,
        stsCertificateFilePath: str,
        stsEndpointAddress: str,
        stsEntityIdentifier: str,
        serviceCertificatePath: str,
        serviceEndpoint: str,
        serviceEndpointId: str,
        clientCertificateFilePath: str,
        cvr: str,
        debugMode: bool = False,
    ) -> None:
        super().__init__(
            stsCertificateFilePath=stsCertificateFilePath,
            stsEndpointAddress=stsEndpointAddress,
            stsEntityIdentifier=stsEntityIdentifier,
            serviceCertificatePath=serviceCertificatePath,
            serviceEndpoint=serviceEndpoint,
            serviceEndpointId=serviceEndpointId,
            clientCertificateFilePath=clientCertificateFilePath,
            cvr=cvr,
            debugMode=debugMode,
        )

    def person_lookup(self, pnr: str) -> dict:
        """Lookup a CPR number and return the result as a dictionary."""
        res = self.PersonLookup(PNR=pnr).Result
        return json.loads(res)
