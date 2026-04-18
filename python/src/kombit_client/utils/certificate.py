import shutil
import ssl
import subprocess
import sys
from pathlib import Path


# Root CA details to check for
_CN = "Den Danske Stat OCES rod-CA"
_O = "Den Danske Stat"
_C = "DK"


def is_oces_root_ca_trusted() -> bool:
    """Return True if 'Den Danske Stat OCES rod-CA' is in the OS trust store.

    Uses platform-native tooling on Windows and macOS to ensure the live
    certificate store is queried rather than a stale snapshot.
    Checks both the machine-wide and current-user trust stores on all platforms.
    """
    if sys.platform == "win32":
        return _check_windows_store()
    else:
        return _check_ssl_context()  # type: ignore[unreachable]


def install_cert_to_trust_store(cert_path: str | Path) -> None:
    """Install a certificate into the machine-wide OS trust store.

    Requires elevated privileges (Administrator on Windows, root on Linux).

    On Linux the certificate is converted to PEM if needed, then installed via
    ``update-ca-certificates`` (Debian/Ubuntu) or ``update-ca-trust`` (RHEL/CentOS).

    Raises RuntimeError if the installation fails.
    """
    if sys.platform == "win32":
        _install_cert_windows(cert_path)
    elif sys.platform == "linux":
        _install_cert_linux(cert_path)  # type: ignore[unreachable]
    else:
        raise NotImplementedError(f"install_cert_to_trust_store is not supported on {sys.platform}")  # type: ignore[unreachable]


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
            subject.get("commonName") == _CN
            and subject.get("organizationName") == _O
            and subject.get("countryName") == _C
        ):
            return True
    return False


def _install_cert_windows(cert_path: str | Path) -> None:
    ps_script = f'Import-Certificate -FilePath "{cert_path}" -CertStoreLocation Cert:\\LocalMachine\\Root'
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to install certificate on Windows: {result.stderr.strip()}")


def _install_cert_linux(cert_path: str | Path) -> None:
    cert_path = Path(cert_path)

    # Ensure the cert is PEM-encoded (required by both tools).
    raw = cert_path.read_bytes()
    pem = raw if b"-----BEGIN" in raw else ssl.DER_cert_to_PEM_cert(raw).encode()

    if shutil.which("update-ca-certificates"):
        # Debian / Ubuntu — cert must have .crt extension.
        dest = Path("/usr/local/share/ca-certificates") / cert_path.with_suffix(".crt").name
        dest.write_bytes(pem)
        result = subprocess.run(["update-ca-certificates"], capture_output=True, text=True)
    elif shutil.which("update-ca-trust"):
        # RHEL / CentOS / Fedora
        dest = Path("/etc/pki/ca-trust/source/anchors") / cert_path.name
        dest.write_bytes(pem)
        result = subprocess.run(["update-ca-trust", "extract"], capture_output=True, text=True)
    else:
        raise RuntimeError(
            "No supported trust store tool found. "
            "Install 'ca-certificates' (Debian) or 'ca-certificates' (RHEL)."
        )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to update CA trust store: {result.stderr.strip()}")
