import pace.dsl
import pace.fv3core
import pace.util
from pace.fv3core.stencils import temperature_adjust
from pace.fv3core.stencils.dyn_core import get_nk_heat_dissipation
from pace.fv3core.testing import TranslateDycoreFortranData2Py


class TranslatePressureAdjustedTemperature_NonHydrostatic(
    TranslateDycoreFortranData2Py
):
    def __init__(
        self,
        grid,
        namelist: pace.util.Namelist,
        stencil_factory: pace.dsl.StencilFactory,
    ):
        super().__init__(grid, namelist, stencil_factory)
        dycore_config = pace.fv3core.DynamicalCoreConfig.from_namelist(namelist)
        self.namelist = dycore_config
        n_adj = get_nk_heat_dissipation(
            config=dycore_config.d_grid_shallow_water,
            npz=grid.grid_indexing.domain[2],
        )
        self.compute_func = stencil_factory.from_origin_domain(  # type: ignore
            temperature_adjust.apply_diffusive_heating,
            origin=stencil_factory.grid_indexing.origin_compute(),
            domain=stencil_factory.grid_indexing.restrict_vertical(
                nk=n_adj
            ).domain_compute(),
        )
        self.in_vars["data_vars"] = {
            "cappa": {},
            "delp": {},
            "delz": {},
            "pt": {},
            "heat_source": {"serialname": "heat_source_dyn"},
        }
        self.in_vars["parameters"] = ["bdt"]
        self.out_vars = {"pt": {}}
        self.stencil_factory = stencil_factory

    def compute_from_storage(self, inputs):
        inputs["delt_time_factor"] = abs(inputs["bdt"] * self.namelist.delt_max)
        del inputs["bdt"]
        self.compute_func(**inputs)
        return inputs
