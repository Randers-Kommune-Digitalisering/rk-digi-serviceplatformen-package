using System.IdentityModel.Tokens;
using System.Text.Json;
using ConnectedServices.PersonBaseDataExtendedService;
using Digst.OioIdws.OioWsTrustCore;
using Digst.OioIdws.WscCore.OioWsTrust;
using static Digst.OioIdws.SoapCore.FederatedChannelFactoryExtensions;


using KombitServiceClient.Configuration;
namespace KombitServiceClient.Integrations.SF1520;


public class PersonBaseDataExtendedClient : ServiceConfiguration
{
    public PersonBaseDataExtendedClient(
        string stsCertificateFilePath,
        string stsEndpointAddress,
        string stsEntityIdentifier,
        string serviceCertificateFilePath,
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
            serviceCertificateFilePath,
            serviceEndpoint,
            serviceEndpointId,
            cvr,
            clientCertificateFilePath,
            clientCertificatePassword,
            debugMode: debugMode)
    {
    }

    public async Task<string> PersonLookup(string PNR)
    {
        var token = (GenericXmlSecurityToken)new StsTokenService(StsConfig).GetToken();
        var response = await CreateChannelWithIssuedToken<PersonBaseDataExtendedPortType>(token, StsConfig)
            .PersonLookupAsync(new PersonLookupRequest(new PersonLookupRequestType { PNR = PNR }));
        var personData = response.PersonLookupResponse1;
        JsonSerializerOptions options = new() { WriteIndented = true, IncludeFields = true };
        return JsonSerializer.Serialize(personData, options);
    }
}