import pydend.subroutine as sbr
import pydend.set_variable as sv
from pydend.export import init_export, export_result


def before_solidification_process(time):
    """
    凝固未完了
    """
    if sv.temp <= sv.temp_l:
        sbr.calc_local_equilibrium(time)
        sbr.calc_liquid_temp_of_res_liq()
        sbr.solve_diffusion(sv.temp)
        sbr.update_interface_cell()
    else:
        pass
    sbr.update_temp()


def after_solidification_process():
    """
    凝固完了
    """
    sv.solid_interface_cell = int(sv.comp_array_length)
    sbr.solve_diffusion(sv.temp)
    sbr.update_temp()


def main():
    export_dirname = init_export()
    export_result(0.0, export_dirname)
    for time_array_index, time in enumerate(sv.time_array):
        if not sbr.is_complete_solidification():
            before_solidification_process(time)
        else:
            after_solidification_process()
        export_result(time, export_dirname)


main()
