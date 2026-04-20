using System.IdentityModel.Tokens;
using System.Text.Json;
using ConnectedServices.SKATForwardEIndkomstService;
using Digst.OioIdws.OioWsTrustCore;
using Digst.OioIdws.WscCore.OioWsTrust;
using static Digst.OioIdws.SoapCore.FederatedChannelFactoryExtensions;


using KombitServiceClient.Configuration;
namespace KombitServiceClient.Integrations.SF0770A;


public class SKATForwardEIndkomstClient : ServiceConfiguration
{
    private readonly string _virksomhedSENummerIdentifikator;
    private readonly string _abonnementTypeKode;
    private readonly string _abonnentTypeKode;
    private readonly string _adgangFormaalTypeKode;

    public SKATForwardEIndkomstClient(
        string virksomhedSENummerIdentifikator,
        string abonnementTypeKode,
        string abonnentTypeKode,
        string adgangFormaalTypeKode,
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
        _virksomhedSENummerIdentifikator = virksomhedSENummerIdentifikator;
        _abonnementTypeKode = abonnementTypeKode;
        _abonnentTypeKode = abonnentTypeKode;
        _adgangFormaalTypeKode = adgangFormaalTypeKode;
    }

    public async Task<string> IndkomstoplysningerLaes(string PersonCivilRegistrationIdentifier, string SoegeAarMaanedFraKode, string SoegeAarMaanedTilKode)
    {
        var token = (GenericXmlSecurityToken)new StsTokenService(StsConfig).GetToken();
        var response = await CreateChannelWithIssuedToken<SKATForwardEIndkomstServiceServicePortType>(token, StsConfig)
            .SF0770_A_IndkomstoplysningerLaes_IndkomstoplysningerLaesAsync(new IndkomstOplysningPersonHent
        {
            IndkomstOplysningPersonHent_I = new IndkomstOplysningPersonHent_I
            {
                HovedOplysninger = new HovedOplysningerType { TransaktionsId = Guid.NewGuid().ToString(), TransaktionsTid = DateTime.UtcNow },
                IndkomstOplysningPersonInddata = new IndkomstOplysningPersonInddataType
                {
                    AbonnentAdgangStruktur = new AbonnentAdgangStrukturType { AbonnementTypeKode = _abonnementTypeKode, AbonnentTypeKode = _abonnentTypeKode, AdgangFormaalTypeKode = _adgangFormaalTypeKode },
                    AbonnentStruktur = new AbonnentStrukturType { AbonnentVirksomhedStruktur = new AbonnentVirksomhedStrukturType { AbonnentVirksomhed = new AbonnentVirksomhedStrukturTypeAbonnentVirksomhed { VirksomhedSENummerIdentifikator = _virksomhedSENummerIdentifikator } } },
                    IndkomstOplysningValg = new IndkomstOplysningPersonInddataTypeIndkomstOplysningValg
                    {
                        Item = new IndkomstOplysningPersonInddataTypeIndkomstOplysningValgIndkomstPersonSamling
                        {
                            PersonIndkomstSoegeStruktur =
                            [
                                new PersonIndkomstSoegeStrukturType { PersonCivilRegistrationIdentifier = PersonCivilRegistrationIdentifier, SoegeAarMaanedLukketStruktur = new SoegeAarMaanedLukketStrukturType { SoegeAarMaanedFraKode = SoegeAarMaanedFraKode, SoegeAarMaanedTilKode = SoegeAarMaanedTilKode}},
                            ]
                        }
                    }
                }
            }
        });
        JsonSerializerOptions options = new() { WriteIndented = true, IncludeFields = true };
        return JsonSerializer.Serialize(response, options);
    }
}