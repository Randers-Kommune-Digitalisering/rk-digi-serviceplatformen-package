using System.IdentityModel.Tokens;
using System.Text.Json;
using ConnectedServices.PersonBaseDataExtendedService;
using Digst.OioIdws.OioWsTrustCore;
using Digst.OioIdws.WscCore.OioWsTrust;
using static Digst.OioIdws.SoapCore.FederatedChannelFactoryExtensions;


using KombitServiceClient.Configuration;
namespace KombitServiceClient.Services;


public class CPRPersonLookup : ServiceConfiguration
{
    public CPRPersonLookup(
        string stsCertificateFilePath,
        string stsEndpointAddress,
        string stsEntityIdentifier,
        string serviceCertificatePath,
        string serviceEndpoint,
        string serviceEndpointId,
        string cvr,
        string clientCertificateFilePath,
        string? clientCertificatePassword = null,
        bool debugMode = false)
        : base(
            stsCertificateFilePath,
            stsEndpointAddress,
            stsEntityIdentifier,
            serviceCertificatePath,
            serviceEndpoint,
            serviceEndpointId,
            cvr,
            clientCertificateFilePath,
            clientCertificatePassword,
            debugMode: debugMode)
    {
    }

    public async Task<string> Lookup(string cprNumber)
    {
        var token = (GenericXmlSecurityToken)new StsTokenService(StsConfig).GetToken();
        var response = await CreateChannelWithIssuedToken<PersonBaseDataExtendedPortType>(token, StsConfig)
            .PersonLookupAsync(new PersonLookupRequest(new PersonLookupRequestType { PNR = cprNumber }));
        var personData = response.PersonLookupResponse1;
        JsonSerializerOptions options = new() { WriteIndented = true, IncludeFields = true };
        return JsonSerializer.Serialize(personData, options);
    }
}