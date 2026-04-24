# RK Serviceplatformen python wrapper project

## kombit-client
[kombit-client python package](python/README.md)


## WSDL
All connected services are generated from wsdl files downloaded from [digitaliseringskataloget](https://digitaliseringskataloget.dk/). When downloading documentation for an integration from digitaliseringskataloget the wdsl files are located in the "teknisk spec" zip file.


* [SF0770A](https://digitaliseringskataloget.dk/integration/sf0770a) - downloaded at 2026-04-23
* [SF1491](https://digitaliseringskataloget.dk/integration/sf1491) - downloaded at 2026-04-23
* [SF1520](https://digitaliseringskataloget.dk/integration/sf1520) - downloaded at 2026-04-23

**dotnet-svcutil config used**
```
{
  "providerId": "Microsoft.Tools.ServiceModel.Svcutil",
  "version": "8.0.0",
  "options": {
    "inputs": [
      "<path to wsdl file>"
    ],
    "namespaceMappings": [
      "*, ConnectedServices.<service name>"
    ],
    "outputFile": "<service name>.cs",
    "references": [
      "<path to project file (KombitServiceClient.csproj)>"
    ],
    "targetFramework": "net9.0",
    "typeReuseMode": "Specified"
  }
}
```
