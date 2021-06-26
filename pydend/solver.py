import numpy as np


class LocalEquilibrium(object):

    def __init__(self):
        pass

    @staticmethod
    def calc_solid_comp(liq_comp, k):
        """
        分配係数を用いて
        液相の濃度から固相の濃度を計算
        """
        solid_comp = liq_comp * k
        return solid_comp

    @staticmethod
    def calc_res_liq_comp_by_scheil_eq(init_comp, liq_fraction, k):
        """
        シャイルの式によって残存する液相の溶質濃度を計算
        Cl = C0*fl^(k−1)
        """
        res_liq_comp = init_comp * liq_fraction ** (k - 1)
        return res_liq_comp

    @staticmethod
    def calc_phase_fraction(solid_interface_cell, x_array):
        """
        固相と液相の相分率を計算
        """
        tot_dend_area = len(x_array) * len(x_array)
        solid_dend_area = (solid_interface_cell + 1) * (solid_interface_cell + 1)
        solid_fraction = solid_dend_area / tot_dend_area
        liq_fraction = 1 - solid_fraction
        return solid_fraction, liq_fraction

    # @staticmethod
    # def calc_res_liq_comp_by_lever_rule(init_comp, solid_fraction, solid_interface_comp, liq_fraction):
    #     """
    #     レバールールを用いて液相濃度を計算
    #     """
    #     res_liq_comp = (init_comp - solid_fraction * solid_interface_comp) / liq_fraction
    #     return res_liq_comp


class LiquidusTempOfResLiq(object):
    def __init__(self):
        pass

    @classmethod
    def calc_liquidus_temp_of_res_liq(cls, temp_m, m_array, init_comp, comp):
        """
        残存する液相の融点を計算
        """
        delt_comp_array = cls._calc_delt_comp(init_comp, comp)
        temp_l = temp_m + np.sum(m_array * delt_comp_array)
        return temp_l

    @staticmethod
    def _calc_delt_comp(init_comp, comp):
        """
        初期濃度からの差を計算
        """
        delt_comp = comp - init_comp
        return delt_comp


class SolveDiffusionEquation(object):
    """
    拡散方程式を計算
    """

    def __init__(self, comp_array, solid_interface_cell, diffusion_coeff, dt):
        self.comp_array = comp_array
        self.solid_interface_cell = solid_interface_cell
        self.diffusion_coeff = diffusion_coeff
        self.dt = dt

    def calc_diffusion(self):
        """
        メイン
        """
        solid_comp_array = self._get_soild_comp_array()
        if self._is_solid_comp_array_leg_more_3(solid_comp_array):
            solid_comp_sec_ord_diff_array = self._calc_sec_ord_diff_in_one_dim(solid_comp_array)
            new_sol_comp_array = solid_comp_array + solid_comp_sec_ord_diff_array * self.diffusion_coeff * self.dt
            self.comp_array[:self.solid_interface_cell + 1] = new_sol_comp_array
        else:
            pass
        return self.comp_array

    def _get_soild_comp_array(self):
        """
        固相中の濃度配列を取得
        """
        solid_comp_array = self.comp_array[:self.solid_interface_cell + 1]
        return solid_comp_array

    @staticmethod
    def _calc_sec_ord_diff_in_one_dim(array):
        """
        １次元の2階微分を計算
        """
        array_dot = np.gradient(array)
        array_2dot = np.gradient(array_dot)
        return array_2dot

    @staticmethod
    def _is_solid_comp_array_leg_more_3(solid_comp_array):
        """
        拡散方程式では，中心差分を用いて二階微分を行うので，
        少なくともセルが3つ以上必要．
        そのため，2以下であれば拡散の計算を行わない
        """
        judge = len(solid_comp_array) >= 3
        return judge
