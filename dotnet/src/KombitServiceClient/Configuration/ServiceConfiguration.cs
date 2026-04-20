
using Digst.OioIdws.OioWsTrustCore;
using Digst.OioIdws.WscCore.OioWsTrust;
using static Digst.OioIdws.WscCore.OioWsTrust.TokenServiceConfigurationFactory;


/// <summary>
/// Provides configuration and initialization for STS token service communication.
/// </summary>
namespace KombitServiceClient.Configuration;


/// <summary>
/// Base class for service configuration, responsible for creating and storing the STS token service configuration.
/// </summary>
public class ServiceConfiguration
{
    /// <summary>
    /// The STS token service configuration instance created from the provided parameters.
    /// </summary>
    private readonly StsTokenServiceConfiguration _stsConfig;

    /// <summary>
    /// Gets the STS token service configuration for use by subclasses.
    /// </summary>
    protected StsTokenServiceConfiguration StsConfig => _stsConfig;


    /// <summary>
    /// Initializes a new instance of the <see cref="ServiceConfiguration"/> class and creates the STS token service configuration.
    /// </summary>
    /// <param name="stsCertificateFilePath">Path to the STS certificate (.cer).</param>
    /// <param name="stsEndpointAddress">STS endpoint address.</param>
    /// <param name="stsEntityIdentifier">STS entity identifier.</param>
    /// <param name="serviceCertificateFilePath">Path to the service certificate (.cer).</param>
    /// <param name="serviceEndpoint">Service endpoint address.</param>
    /// <param name="serviceEndpointId">Service endpoint ID.</param>
    /// <param name="cvr">CVR number.</param>
    /// <param name="clientCertificateFilePath">Path to the client certificate (.p12).</param>
    /// <param name="clientCertificatePassword">Optional password for the client certificate (.p12).</param>
    /// <param name="includeLibertyHeader">Whether to include the Liberty header (default: true).</param>
    /// <param name="wspSoapVersion">SOAP version for WSP (default: "1.1").</param>
    /// <param name="debugMode">Enable debug mode (default: false).</param>
    public ServiceConfiguration(
        string stsCertificateFilePath,
        string stsEndpointAddress,
        string stsEntityIdentifier,
        string serviceCertificateFilePath,
        string serviceEndpoint,
        string serviceEndpointId,
        string cvr,
        string clientCertificateFilePath,
        string? clientCertificatePassword = null,
        bool includeLibertyHeader = true,
        string wspSoapVersion = "1.1",
        bool debugMode = false)
    {
        _stsConfig = CreateStsConfigInternal(
            stsCertificateFilePath,
            stsEndpointAddress,
            stsEntityIdentifier,
            serviceCertificateFilePath,
            serviceEndpoint,
            serviceEndpointId,
            cvr,
            clientCertificateFilePath,
            clientCertificatePassword,
            includeLibertyHeader,
            wspSoapVersion,
            debugMode
        );
    }


    /// <summary>
    /// Creates the STS token service configuration from the provided parameters.
    /// </summary>
    /// <param name="stsCertificateFilePath">Path to the STS certificate (.cer).</param>
    /// <param name="stsEndpointAddress">STS endpoint address.</param>
    /// <param name="stsEntityIdentifier">STS entity identifier.</param>
    /// <param name="serviceCertificateFilePath">Path to the service certificate (.cer).</param>
    /// <param name="serviceEndpoint">Service endpoint address.</param>
    /// <param name="serviceEndpointId">Service endpoint ID.</param>
    /// <param name="cvr">CVR number.</param>
    /// <param name="clientCertificateFilePath">Path to the client certificate (.p12).</param>
    /// <param name="clientCertificatePassword">Optional password for the client certificate (.p12).</param>
    /// <param name="includeLibertyHeader">Whether to include the Liberty header.</param>
    /// <param name="wspSoapVersion">SOAP version for WSP.</param>
    /// <param name="debugMode">Enable debug mode.</param>
    /// <returns>The created <see cref="StsTokenServiceConfiguration"/> instance.</returns>
    private StsTokenServiceConfiguration CreateStsConfigInternal(
        string stsCertificateFilePath,
        string stsEndpointAddress,
        string stsEntityIdentifier,
        string serviceCertificateFilePath,
        string serviceEndpoint,
        string serviceEndpointId,
        string cvr,
        string clientCertificateFilePath,
        string? clientCertificatePassword = null,
        bool includeLibertyHeader = true,
        string wspSoapVersion = "1.1",
        bool debugMode = false)
    {
        Certificate clientCert;

        if (clientCertificatePassword is null)
        {
            clientCert = new Certificate { FilePath = clientCertificateFilePath, FromFileSystem = true };
        }
        else
        {
            clientCert = new Certificate { FilePath = clientCertificateFilePath, Password = clientCertificatePassword, FromFileSystem = true };
        }

        return CreateConfiguration(new OioIdwsWcfConfigurationSection()
        {
            StsCertificate = new Certificate { FilePath = stsCertificateFilePath, FromFileSystem = true },
            StsEndpointAddress = stsEndpointAddress,
            StsEntityIdentifier = stsEntityIdentifier,
            ServiceCertificate = new Certificate { FilePath = serviceCertificateFilePath, FromFileSystem = true },
            WspEndpoint = serviceEndpoint,
            WspEndpointID = serviceEndpointId,
            ClientCertificate = clientCert,
            Cvr = cvr,
            TokenLifeTimeInMinutes = 60,
            IncludeLibertyHeader = includeLibertyHeader,
            MaxReceivedMessageSize = 256000,
            DebugMode = debugMode,
            WspSoapVersion = wspSoapVersion
        });
    }
}
