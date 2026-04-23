using System.IdentityModel.Tokens;
using System.Text.Json;
using ConnectedServices.YdelseListeHentService;
using Digst.OioIdws.OioWsTrustCore;
using System.Globalization;
using static Digst.OioIdws.SoapCore.FederatedChannelFactoryExtensions;

using KombitServiceClient.Configuration;

namespace KombitServiceClient.Integrations.SF1491;

public class YdelseListHentClient : ServiceConfiguration
{
    public YdelseListHentClient(
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
            includeLibertyHeader: false, // SF1491 kræver ikke Liberty-header
            wspSoapVersion: "1.2", // SF1491 bruger SOAP 1.2
            debugMode: debugMode)
    {
    }

    public async Task<string> EffektueringHent(string cpr, string? startDato = null, string? slutDato = null)
    {
        static bool TryParseDate(string? s, out DateTime date)
        {
            if (string.IsNullOrWhiteSpace(s))
            {
                date = default;
                return false;
            }

            return DateTime.TryParseExact(
                s,
                "yyyy-MM-dd",
                CultureInfo.InvariantCulture,
                DateTimeStyles.None,
                out date);
        }

        var hasStart = TryParseDate(startDato, out var start);
        if (!string.IsNullOrWhiteSpace(startDato) && !hasStart)
            throw new ArgumentException("startDato skal være 'yyyy-MM-dd' (fx 2026-03-01).", nameof(startDato));

        var hasSlut = TryParseDate(slutDato, out var slut);
        if (!string.IsNullOrWhiteSpace(slutDato) && !hasSlut)
            throw new ArgumentException("slutDato skal være 'yyyy-MM-dd' (fx 2026-04-15).", nameof(slutDato));

        var token = (GenericXmlSecurityToken)new StsTokenService(StsConfig).GetToken();

        var response = await CreateChannelWithIssuedToken<YdelseListeHentServicePortType>(token, StsConfig)
            .EffektueringHentAsync(new EffektueringHentRequest
            {
                EffektueringHent_I = new EffektueringHent_I
                {
                    HovedOplysninger = new HovedOplysningerType
                    {
                        TransaktionsId = Guid.NewGuid().ToString(),
                        TransaktionsTid = DateTime.UtcNow
                    },
                    Kriterie = new EffektueringHent_ITypeKriterie
                    {
                        Item = cpr,
                        ItemElementName = ItemChoiceType1.PartCPRNummer
                    },

                    RettighedListe = [ new EffektueringHent_ITypeBevillingDataAfgrGruppe() ],

                    OekonomiskEffektueringDispositionsDatoFra = hasStart ? start : default,
                    OekonomiskEffektueringDispositionsDatoFraSpecified = hasStart,
                    OekonomiskEffektueringDispositionsDatoTil = hasSlut ? slut : default,
                    OekonomiskEffektueringDispositionsDatoTilSpecified = hasSlut,
                }
            });

        JsonSerializerOptions options = new() { WriteIndented = true, IncludeFields = true };
        return JsonSerializer.Serialize(response, options);
    }
}