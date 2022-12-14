class RaiseWhenAccessed:
    def __init__(self, err):
        self._err = err

    def __getattr__(self, _):
        raise self._err

    def __call__(self, *args, **kwargs):
        raise self._err


try:
    import zarr
except ModuleNotFoundError as err:
    zarr = RaiseWhenAccessed(err)

try:
    import xarray
except ModuleNotFoundError as err:
    xarray = None

try:
    import cupy
except ImportError:
    cupy = None

try:
    import gt4py
except ImportError:
    gt4py = None

try:
    import dace
except ImportError:
    dace = None
