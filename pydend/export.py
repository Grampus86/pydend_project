from pydend.plt_toolkit import PlotLine
import pydend.set_variable as sv
import pandas as pd
import pydend.set_path as path
import os
import datetime
from time import sleep


class SetExportDir(object):
    def __init__(self):
        pass

    @staticmethod
    def create_export_dir():
        """
        時間付きexportディレクトリを作成
        """
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        export_dirname = 'export_{}'.format(now)
        os.mkdir('{0}/{1}'.format(path.output_data_path, export_dirname))
        sleep(3)
        return export_dirname

    @staticmethod
    def create_export_data_dir(export_dirname):
        """
        データを格納するディレクトリを作成
        """
        os.mkdir('{0}/{1}/data'.format(path.output_data_path, export_dirname))

    @staticmethod
    def create_export_plot_dir(export_dirname):
        """
        プロット図を格納するディレクトリを作成
        """
        os.mkdir('{0}/{1}/plot_against_distance'.format(path.output_data_path, export_dirname))
        os.mkdir('{0}/{1}/plot_against_fs'.format(path.output_data_path, export_dirname))


class ExportResult(object):
    def __init__(self, time, export_dirname):
        self.time = float('{0:.2f}'.format(time))
        self.export_dirname = export_dirname

    @classmethod
    def _to_dataflame(cls):
        """
        データフレームにする
        """
        df_export_data = pd.DataFrame(sv.comp_array.T)
        df_export_data.columns = sv.element_name_list
        fs_array = cls._convert_to_fs_array()
        df_export_data.insert(0, 'distance', sv.x_array)
        df_export_data.insert(1, 'fs', fs_array)
        return df_export_data

    def export_comp_data(self):
        """
        組成データを出力
        """
        df_export_data = self._to_dataflame()
        df_export_data.to_excel('{0}/data/comp_data_{1}.xlsx'.format(self.export_dirname, self.time))

    def is_export_time(self):
        if (self.time >= sv.export_time) or (self.time >= sv.end_time):
            judge = True
        else:
            judge = False
        return judge

    def export_plot_against_distance(self):
        pll = PlotLine.set_ax(figsize=(8, 6))
        pll.set_plot_layout()
        pll.set_axis_label(xlabel='Distance (μm)', ylabel='Content (mass%)',
                           font_name='Times New Roman')
        df = self._to_dataflame()
        for ele in sv.element_name_list:
            pll.plot_line(df['distance'], df[ele], label=ele)
        pll.set_legend()
        pll.set_axis_range(x_min=sv.x_dist_min, x_max=sv.x_dist_max, y_min=sv.y_min, y_max=sv.y_max)
        pll.savefig('{0}/plot_against_distance/fig_{1}'.format(self.export_dirname, self.time),
                    is_append_datetime=False)

    def export_plot_against_fs(self):
        pll = PlotLine.set_ax(figsize=(8, 6))
        pll.set_plot_layout()
        pll.set_axis_label(xlabel='fs (-)', ylabel='Content (mass%)',
                           font_name='Times New Roman')
        df = self._to_dataflame()
        for ele in sv.element_name_list:
            pll.plot_line(df['fs'], df[ele], label=ele)
        pll.set_legend()
        pll.set_axis_range(x_min=sv.x_fs_min, x_max=sv.x_fs_max, y_min=sv.y_min, y_max=sv.y_max)
        pll.savefig('{0}/plot_against_fs/fig_{1}'.format(self.export_dirname, self.time),
                    is_append_datetime=False)

    @staticmethod
    def _convert_to_fs_array():
        tot_dend_area = sv.x_length * sv.x_length
        solid_dend_area = sv.x_array * sv.x_array
        fs_array = solid_dend_area / tot_dend_area
        return fs_array


def init_export():
    sed = SetExportDir()
    export_dirname = sed.create_export_dir()
    sed.create_export_data_dir(export_dirname)
    sed.create_export_plot_dir(export_dirname)
    return export_dirname


def export_result(time, export_dirname):
    er = ExportResult(time, export_dirname)
    if er.is_export_time():
        er.export_comp_data()
        er.export_plot_against_fs()
        er.export_plot_against_distance()
        sv.export_time += sv.delta_export_time
