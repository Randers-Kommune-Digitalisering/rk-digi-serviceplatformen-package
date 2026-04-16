# rk-digi-serviceplatformen

## Basic python file (placed in same dir as DLLs and runtime config)
```python
from clr_loader import get_coreclr
from pythonnet import set_runtime


set_runtime(get_coreclr(runtime_config="runtimeconfig.json"))

import clr
import sys
import os

dll_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(dll_dir)

clr.AddReference("KombitServiceClient")

from KombitServiceClient.Configuration import ServiceConfiguration

config = ServiceConfiguration(
    <params>
)

result = config.CreateStsConfig()

```
**Dependencies for running:** pythonnet v3.1.0-rc0, net9.0 runtime