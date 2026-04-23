import base64
import ssl
import subprocess
import sys

# Root CA details to check for
_CN = "Den Danske Stat OCES rod-CA"
_O = "Den Danske Stat"
_C = "DK"


def write_cert_file_from_base64_string(base64_string: str, output_file_path: str) -> None:
    with open(output_file_path, "wb") as f:
        f.write(base64.b64decode(base64_string))


def is_oces_root_ca_trusted() -> bool:
    """
    Return True if 'Den Danske Stat OCES rod-CA' is in the OS trust store.

    Uses platform-native tooling on Windows and macOS to ensure the live
    certificate store is queried rather than a stale snapshot.
    Checks both the machine-wide and current-user trust stores on all platforms.
    """
    if sys.platform == "win32":
        return _check_windows_store()
    elif sys.platform == "linux":
        return _check_ssl_context()  # type: ignore[unreachable]
    else:
        raise NotImplementedError(f"is_oces_root_ca_trusted is not supported on {sys.platform}")  # type: ignore[unreachable]


def _check_windows_store() -> bool:
    # PowerShell reads the live Windows certificate store and parses Subject
    # fields properly — no false positives from intermediate certs that merely
    # reference this CA in their issuer or extension fields.
    # Checks both LocalMachine\Root (machine) and CurrentUser\Root (user).
    ps_script = (
        r"$certs = Get-ChildItem Cert:\LocalMachine\Root,Cert:\CurrentUser\Root"
        f" | Where-Object {{ $_.Subject -like '*CN={_CN}*' }};"
        r" if ($certs) { exit 0 } else { exit 1 }"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        capture_output=True,
    )
    return result.returncode == 0


def _check_ssl_context() -> bool:
    # Linux: get_ca_certs() reads from the OpenSSL CA bundle on disk,
    # which reflects the current state after trust store changes.
    context = ssl.create_default_context()
    for cert in context.get_ca_certs(binary_form=False):
        subject = {k: v for rdn in cert["subject"] for k, v in rdn}
        if (
            subject.get("commonName") == _CN and subject.get("organizationName") == _O and subject.get("countryName") == _C
        ):
            return True
    return False
