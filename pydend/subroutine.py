import pydend.set_variable as sv
import pydend.solver as slv
import numpy as np


def calc_local_equilibrium(time):
    for ele in range(sv.element_num):
        if time != sv.end_time:
            # 液相界面の濃度を計算
            liq_interface_comp = sv.comp_array[ele][sv.liq_interface_cell]
            # 固相界面の濃度を計算
            solid_interface_comp = slv.LocalEquilibrium.calc_solid_comp(liq_interface_comp, sv.k_array[ele])
            # 濃度配列の界面セルに計算した固相界面の濃度を代入
            sv.comp_array[ele][sv.solid_interface_cell] = solid_interface_comp
            # 相分率を計算
            sol_fraction, liq_fraction = slv.LocalEquilibrium.calc_phase_fraction(sv.solid_interface_cell, sv.x_array)
            # 残存する液相の濃度を計算
            residual_liq_comp = slv.LocalEquilibrium. \
                calc_res_liq_comp_by_scheil_eq(sv.init_comp_array[ele], liq_fraction, sv.k_array[ele])
            # 液相濃度を更新.液相領域はすべて残存する濃度とする
            sv.comp_array[ele][sv.liq_interface_cell:] = residual_liq_comp
            sv.res_liq_comp_array[ele] = sv.comp_array[ele][sv.liq_interface_cell]
        else:
            continue


def solve_diffusion(temp):
    """
    固相の拡散方程式を計算
    1.99は気体定数
    """
    for ele in range(sv.element_num):
        diff_coeff = lambda temp: sv.d0_array[ele] * np.exp(-sv.q_array[ele] / (1.99 * temp)) * 2E8
        sde = slv.SolveDiffusionEquation(sv.comp_array[ele], sv.solid_interface_cell, diff_coeff(temp), sv.dt)
        sv.comp_array[ele] = sde.calc_diffusion()


def calc_liquid_temp_of_res_liq():
    """
    残存する液相の融点を計算
    """
    sv.temp_l = slv.LiquidusTempOfResLiq. \
        calc_liquidus_temp_of_res_liq(sv.temp_m, sv.m_array, sv.init_comp_array, sv.res_liq_comp_array)


def update_temp():
    """
    冷却速度から温度を更新
    """
    if sv.temp > sv.end_temp_m:
        sv.temp = sv.temp - sv.cooling_rate * sv.dt
    else:
        sv.temp=sv.end_temp_m
    return sv.temp


def update_interface_cell():
    """
    界面のセルの位置をアップデート
    """
    sv.solid_interface_cell += 1
    sv.liq_interface_cell += 1


def is_complete_solidification():
    """
    固相率が0.9以上になったら凝固完了とする
    """
    sol_fraction, _ = slv.LocalEquilibrium.calc_phase_fraction(sv.solid_interface_cell, sv.x_array)
    judge = sol_fraction >= 0.9
    return judge

