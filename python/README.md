# kombit-client

A Python client for connecting to Danish government web services via [KOMBIT Serviceplatformen](https://digitaliseringskataloget.dk/). The package wraps a .NET library using [pythonnet](https://pythonnet.github.io/), exposing a clean Python API with Pythonic naming conventions.

## Requirements

- Python 3.10–3.14
- .NET 9 runtime or SDK ([download](https://dotnet.microsoft.com/download))
- Certificates issued by KOMBIT for STS and service authentication: [digitaliseringskataloget - certifikater](https://digitaliseringskataloget.dk/teknik/certifikater)

## Installation

```bash
pip install kombit-client
```

## Overview

All configuration is handled via environment variables. You must set the following variables before using the client:

| Environment Variable        | Description                                                                   |
|-----------------------------|-------------------------------------------------------------------------------|
| `CERT_BASE_PATH`            | Directory containing all certificate files                                    |
| `CLIENT_CERT`               | Filename of client certificate (e.g., `client.p12`)                           |
| `CLIENT_PASS`               | (Optional) Password for client certificate                                    |
| `ROOT_CERT`                 | (Optional) Filename of the root certificate (needs to be added to trust store)|
| `ACCESS_CONTROL_CERT`       | (Optional) Filename of the STS/Access Control certificate                     |
| `SIGNING_CERT`              | (Optional) Filename of the Service Provider signing certificate               |
| `STS_ENDPOINT_ADDRESS`      | (Optional) URL of the STS endpoint                                            |
| `STS_ENDPOINT_ID`           | (Optional) Entity identifier for the STS                                      |

If optional variables are not set, defaults will be used as defined in the code. All certificate paths are constructed as `os.path.join(CERT_BASE_PATH, <filename>)`.

---

## Integrations

### SF1520 – CPR replika opslag
Lookup person base data from CPR via [SF1520](https://digitaliseringskataloget.dk/integration/sf1520).

#### Services

##### PersonBaseDataExtendedService
This service allows public authorities' user systems to retrieve personal information.



```python
from kombit_client.integrations.sf1520 import PersonBaseDataExtendedClient

client = PersonBaseDataExtendedClient(
    cvr="<organisation's CVR>"
)

result = client.person_lookup(pnr="<a civil registration number>")
# Returns a dict with person base data
```

---

### SF0770A – SKAT Indkomst - Opslag personoplysninger
Retrieve income data from SKAT via [SF0770_A](https://digitaliseringskataloget.dk/integration/sf0770a).

#### Services


##### SKATForwardEIndkomstService
Synchronous web service that allows you to retrieve income information.

The current implementaion only allows retrieving income information for private individuals.

**Useful docs:**
* [eIndkomst Udstilling](https://info.skat.dk/data.aspx?oid=2248828&chk=220344) ("underbilag 1 (excel)" describes the different fields)

**Code example**
```python
from kombit_client.integrations.sf0770a import SKATForwardEIndkomstClient

client = SKATForwardEIndkomstClient(
    cvr="<organisation's CVR number>",
    virksomhed_se_nummer_identifikator="<organisation's SE number>",
    abonnement_type_kode="<subscription type code>",
    abonnent_type_kode="<subscriber type code>",
    adgang_formaal_type_kode="<purpose of access code>"
)

result = client.indkomstoplysninger_laes(
    person_civil_registration_identifier="<a civil registration number>",
    soege_aar_maaned_fra_kode="202401",
    soege_aar_maaned_til_kode="202403",
)
# Returns a dict with income data for the given period
```

The `soege_aar_maaned_fra_kode` and `soege_aar_maaned_til_kode` parameters are year-month strings in `YYYYMM` format defining the search period.

---

## License

MIT – see [LICENSE](../LICENSE) for details.

## Authors

- Rune Keena (runekeena@gmail.com)
- [Randers Kommune Digitalisering](https://github.com/Randers-Kommune-Digitalisering)
