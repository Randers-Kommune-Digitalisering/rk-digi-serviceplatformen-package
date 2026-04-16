import json

from kombit_client.dotnet._bridge import CPRPersonLookup


class CPRLookup(CPRPersonLookup):
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

    def lookup(self, cpr_number: str) -> dict:
        """Lookup a CPR number and return the result as a dictionary."""
        res = self.Lookup(cpr_number).Result
        return json.loads(res)
