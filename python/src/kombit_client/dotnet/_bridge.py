import importlib
import os

from clr_loader import get_coreclr
from pythonnet import set_runtime

_DOTNET_DIR = os.path.abspath(os.path.dirname(__file__))
_INTEGRATIONS_NS = "KombitServiceClient.Integrations"


def _load_dotnet() -> None:
    runtime_config = os.path.join(_DOTNET_DIR, "KombitServiceClient.runtimeconfig.json")
    set_runtime(get_coreclr(runtime_config=runtime_config))
    import clr
    clr.AddReference(os.path.join(_DOTNET_DIR, "KombitServiceClient"))


_load_dotnet()

import System.Reflection as _Reflection  # noqa: E402

_assembly = _Reflection.Assembly.Load("KombitServiceClient")
for _t in _assembly.GetTypes():
    if _t.Namespace and _t.Namespace.startswith(_INTEGRATIONS_NS) and _t.IsPublic and not _t.IsAbstract:
        globals()[_t.Name] = getattr(importlib.import_module(_t.Namespace), _t.Name)
