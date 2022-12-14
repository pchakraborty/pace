try:
    import xarray as xr
    from xarray import DataArray, Dataset, open_dataset
except ModuleNotFoundError as err:
    from ._optional_imports import RaiseWhenAccessed

    xr = RaiseWhenAccessed(err)
    DataArray = RaiseWhenAccessed(err)
    Dataset = RaiseWhenAccessed(err)
    open_dataset = RaiseWhenAccessed(err)


def to_dataset(state):
    data_vars = {
        name: value.data_array for name, value in state.items() if name != "time"
    }
    if "time" in state:
        data_vars["time"] = state["time"]
    return xr.Dataset(data_vars=data_vars)
