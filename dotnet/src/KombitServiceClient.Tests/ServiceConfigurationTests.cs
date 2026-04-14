using Xunit;
using KombitServiceClient.Configuration;

public class ServiceConfigurationTests
{
    [Fact]
    public void CreateStsConfig_WithValidParameters_DoesNotThrow()
    {
        // Arrange
        var config = new ServiceConfiguration(
            "../../../../certs/ADG_PROD_Adgangsstyring_2.cer",
            "stsEndpoint",
            "stsEntityId",
            "../../../../certs/new_SP_PROD_Signing_1.cer",
            "serviceEndpoint",
            "serviceEndpointId",
            "../../../../certs/client.p12",
            "12345678"  // cvr
        );

        // Act & Assert
        var exception = Record.Exception(() => config.CreateStsConfig());
        Assert.Null(exception);
    }
}
