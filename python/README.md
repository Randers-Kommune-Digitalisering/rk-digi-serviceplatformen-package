[![PyPI version](https://img.shields.io/pypi/v/kombit-client.svg)](https://pypi.org/project/kombit-client/)
# kombit-client

A Python client for connecting to Danish government web services via [KOMBIT Serviceplatformen](https://digitaliseringskataloget.dk/). The package wraps a .NET library using [pythonnet](https://pythonnet.github.io/), exposing a clean Python API with Pythonic naming conventions.

## Requirements

- Python 3.10–3.14
- .NET 9 runtime or SDK ([download](https://dotnet.microsoft.com/download))
- Certificates issued by KOMBIT for STS and service authentication: [digitaliseringskataloget - certifikater](https://digitaliseringskataloget.dk/teknik/certifikater)*

***Note**: The “Den Danske Stat” root certificate must be installed in a trusted root certificate store (either the system or user trust store).

## Installation

```bash
pip install kombit-client
```

## Overview

All configuration can be handled via environment variables. You can set the following variables before using the service clients:

| Environment Variable        | Description                                                                   |
|-----------------------------|-------------------------------------------------------------------------------|
| `CVR_NUMBER`                | (Optional) Organisation's CVR number                                          |
| `CERT_BASE_PATH`            | (Optional) Directory containing all certificate files                         |
| `CLIENT_CERT`               | (Optional) Filename of client certificate (e.g., `client.p12`)                |
| `CLIENT_CERT_BASE64`        | (Optional) Client certificate as a base64 string                              |
| `CLIENT_CERT_PASS`          | (Optional) Password for client certificate                                    |
| `ROOT_CERT`                 | (Optional) Filename of the root certificate (needs to be added to trust store)|
| `ACCESS_CONTROL_CERT`       | (Optional) Filename of the STS/Access Control certificate                     |
| `SP_SIGNING_CERT`           | (Optional) Filename of the "serviceplatformen" signing certificate            |
| `YDELSESINDEKS_CERT`        | (Optional) Filename of the "ydelsesindeks" signing certificate                |
| `STS_ENDPOINT_ADDRESS`      | (Optional) URL of the STS endpoint                                            |
| `STS_ENDPOINT_ID`           | (Optional) Entity identifier for the STS                                      |

Defaults certificate names are defined in the code for public shared certificates and are based on current (2026-04-24) certificate names from serviceplatformen's production environment.
All certificate paths are constructed as `os.path.join(CERT_BASE_PATH, <filename>)`.

All configurations can also be set when initiating the service clients. Some service clients might require additional configuration passed at initialization. 

---

## Integrations

### SF1520 – CPR replika opslag
Lookup person base data from CPR via [SF1520](https://digitaliseringskataloget.dk/integration/sf1520).

#### Services

##### PersonBaseDataExtendedService
This service allows public authorities' user systems to retrieve personal information.



```python
from kombit_client.integrations.sf1520 import PersonBaseDataExtendedClient

client = PersonBaseDataExtendedClient()

result = client.person_lookup(pnr="<a civil registration number>")
# Returns a dict with person base data
```

---

### SF0770A – SKAT Indkomst - Opslag personoplysninger
Retrieve income data from SKAT via [SF0770_A](https://digitaliseringskataloget.dk/integration/sf0770a).

#### Services


##### SKATForwardEIndkomstService
Synchronous web service that allows you to retrieve income information.

The current implementation only allows retrieving income information for private individuals.

**Useful docs:**
* [eIndkomst Udstilling](https://info.skat.dk/data.aspx?oid=2248828&chk=220344) ("underbilag 1 (excel)" describes the different fields)

**Code example**
```python
from kombit_client.integrations.sf0770a import SKATForwardEIndkomstClient

client = SKATForwardEIndkomstClient(
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

### SF1491 – Hent ydelser fra egen sektor
Lookup granted benefits and payments for a person within your own sector via [SF1491](https://digitaliseringskataloget.dk/integration/sf1491).

#### Services

##### YdelseListeHent
This service allows public authorities' systems to retrieve information about granted and disbursed financial benefits (effektueringer) for a given person.

```python
from kombit_client.integrations.sf1491 import YdelseListeHentClient

client = YdelseListeHentClient(
    cvr="<organisation's CVR>"
)

result = client.effektuering_hent(
    cpr="<a civil registration number>",
    start_dato="2026-01-01",  # optional
    slut_dato="2026-12-31"    # optional
)
```

---

## License

MIT – see [LICENSE](../LICENSE) for details.

## Authors

- Rune Keena (runekeena@gmail.com)
- [Randers Kommune Digitalisering](https://github.com/Randers-Kommune-Digitalisering)
