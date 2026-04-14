
using Digst.OioIdws.OioWsTrustCore;
using Digst.OioIdws.WscCore.OioWsTrust;
using static Digst.OioIdws.WscCore.OioWsTrust.TokenServiceConfigurationFactory;

namespace KombitServiceClient.Configuration;

public class ServiceConfiguration
{
    public string StsCertificateFilePath { get; }  // .cer
    public string StsEndpointAddress { get; }
    public string StsEntityIdentifier { get; }
    public string ServiceCertificatePath { get; }  // .cer
    public string ServiceEndpoint { get; }
    public string ServiceEndpointId { get; }
    public string ClientCertificateFilePath { get; }  // .p12
    public string Cvr { get; }
    public bool IncludeLibertyHeader { get; }  // default: true
    public string WspSoapVersion { get; }  // default: "1.1"
    public bool DebugMode { get; }  // default: false

    public ServiceConfiguration(
        string stsCertificateFilePath,
        string stsEndpointAddress,
        string stsEntityIdentifier,
        string serviceCertificatePath,
        string serviceEndpoint,
        string serviceEndpointId,
        string clientCertificateFilePath,
        string cvr,
        bool includeLibertyHeader = true,
        string wspSoapVersion = "1.1",
        bool debugMode = false)
    {
        StsCertificateFilePath = stsCertificateFilePath;
        StsEndpointAddress = stsEndpointAddress;
        StsEntityIdentifier = stsEntityIdentifier;
        ServiceCertificatePath = serviceCertificatePath;
        ServiceEndpoint = serviceEndpoint;
        ServiceEndpointId = serviceEndpointId;
        ClientCertificateFilePath = clientCertificateFilePath;
        Cvr = cvr;
        IncludeLibertyHeader = includeLibertyHeader;
        WspSoapVersion = wspSoapVersion;
        DebugMode = debugMode;
    }

    public StsTokenServiceConfiguration CreateStsConfig() =>
        CreateConfiguration(new OioIdwsWcfConfigurationSection()
        {
            StsCertificate = new Certificate { FilePath = StsCertificateFilePath, FromFileSystem = true },
            StsEndpointAddress = StsEndpointAddress,
            StsEntityIdentifier = StsEntityIdentifier,
            ServiceCertificate = new Certificate { FilePath = ServiceCertificatePath, FromFileSystem = true },
            WspEndpoint = ServiceEndpoint,
            WspEndpointID = ServiceEndpointId,
            ClientCertificate = new Certificate { FilePath = ClientCertificateFilePath, FromFileSystem = true },
            Cvr = Cvr,
            TokenLifeTimeInMinutes = 60,
            IncludeLibertyHeader = IncludeLibertyHeader,
            MaxReceivedMessageSize = 256000,
            DebugMode = DebugMode,
            WspSoapVersion = WspSoapVersion
        });
}
