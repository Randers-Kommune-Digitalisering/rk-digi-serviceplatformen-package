import os
from clr_loader import get_coreclr
from pythonnet import set_runtime

_DOTNET_DIR = os.path.abspath(os.path.dirname(__file__))


def _load_dotnet() -> None:
    runtime_config = os.path.join(_DOTNET_DIR, "KombitServiceClient.runtimeconfig.json")
    set_runtime(get_coreclr(runtime_config=runtime_config))
    import clr
    clr.AddReference(os.path.join(_DOTNET_DIR, "KombitServiceClient"))


_load_dotnet()
from KombitServiceClient.Integrations.SF1520 import PersonBaseDataExtendedClient as _PersonBaseDataExtendedClient  # noqa: E402

__all__ = ["_PersonBaseDataExtendedClient"]
