from clr_loader import get_coreclr
from pythonnet import set_runtime


def _load_dotnet() -> None:
    set_runtime(get_coreclr(runtime_config="KombitServiceClient.runtimeconfig.json"))
    import clr  # noqa: WPS43
    clr.AddReference("KombitServiceClient")


# dll_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(dll_dir)
_load_dotnet()
from KombitServiceClient.Services import CPRPersonLookup  # noqa: E402

__all__ = ["CPRPersonLookup"]
