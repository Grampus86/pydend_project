"""
メゾットチェーンで使う
"""
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import mathtext

mathtext.FontConstantsBase = mathtext.ComputerModernFontConstants  # 上つき文字の補正
plt.rcParams['font.family'] = 'Times New Roman'


class Setplot(object):
    """
    プロットエリアを設定
    """

    def __init__(self, ax):
        self.ax = ax

    @classmethod
    def set_ax(cls, figsize=(6, 4), facecolor='white', right=0.7):
        """
        fig,axを設定
        プロットエリアの大きさ、線の幅、色を決める。
        facecolorを'white'にしておくことでmonokaiで見にくくなる問題を回避
        """
        fig = plt.figure(figsize=figsize, facecolor=facecolor, linewidth=10)
        fig.subplots_adjust(right=right)
        ax = fig.add_subplot(111)
        return cls(ax)

    def set_plot_layout(self, grid_axis='both', fontsize=18, is_bottom_tick=True):
        """
        プロットエリアのグリット線と軸の数字の大きさを設定
        ax.grid線は、
        水平+垂直：'both'
        水平のみ：'y'
        垂直のみ：'x'
        を引数にとる
        """
        self.ax.set_axisbelow(True)
        self.ax.grid(axis=grid_axis, color='black', linestyle='dashed', linewidth=0.8)
        self.ax.tick_params(labelsize=fontsize, direction='out',
                            length=5, colors='black', bottom=is_bottom_tick)
        self.ax.spines["top"].set_linewidth(1.0)
        self.ax.spines["left"].set_linewidth(1.0)
        self.ax.spines["bottom"].set_linewidth(1.0)
        self.ax.spines["right"].set_linewidth(1.0)
        self.ax.spines["top"].set_linewidth(1.0)
        self.ax.spines['top'].set_color('black')
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color('black')
        return self

    def set_axis_range(self, x_min='auto', x_max='auto', y_min='auto', y_max='auto'):
        """
        軸の範囲を設定。
        'auto'にしておくことで、autoにできる
        """
        if x_min == 'auto' or x_max == 'auto':
            self.ax.set_xlim(auto=True)
        else:
            self.ax.set_xlim([x_min, x_max])
        if y_min == 'auto' or y_max == 'auto':
            self.ax.set_ylim(auto=True)
        else:
            self.ax.set_ylim([y_min, y_max])
        return self

    def set_log(self, is_set_x=True, is_set_y=True):
        """
        軸をlogスケールにする
        """
        if is_set_x:
            self.ax.set_xscale('log')
        if is_set_y:
            self.ax.set_yscale('log')
        return self

    def set_axis_label(self, xlabel, ylabel, fontsize=18, font_name='MS Gothic'):
        """
        軸ラベルを設定。
        なしにしたい場合は''を入力
        """
        if xlabel != '':
            self.ax.set_xlabel(xlabel, fontsize=fontsize, fontname=font_name)
        if ylabel != '':
            self.ax.set_ylabel(ylabel, fontsize=fontsize, fontname=font_name)
        return self

    def set_legend(self, fontsize=14, loc='upper left'):
        """
        凡例を設定。
        """
        self.ax.legend(fontsize=fontsize, loc=loc, bbox_to_anchor=(1.05, 1),
                       fancybox=False, edgecolor="black", framealpha=1)
        return self

    def replace_xticks(self, xticks_array, xticks_label, rad=0):
        """
        x軸の目盛りを置換
        axes.set_xticks()で
        文字列に置き換えたい座標に限定してから置き換える。
        """
        self.ax.set_xticks(xticks_array)
        self.ax.set_xticklabels(xticks_label, rotation=rad)
        return self

    def plt_show(self, is_plot=True):
        """
        グラフを表示する。
        notebook使用する場合は、
        インラインでグラフが表示されるので、
        させたくない場合は、'is_plot'を'False'にする
        """
        if is_plot:
            plt.show()
        # メモリ解放
        plt.clf()
        plt.close()
        return self

    def savefig(self, figname, dpi=300, is_append_datetime=True, is_make_dir=False):
        """
        グラフを保存。
        日付を付けたければ、'is_append_datetime'を'True'にする
        """
        now = datetime.now()
        if is_append_datetime:
            save_file_name = '{0}_{1:%Y%m%d%H%M%S}'.format(figname, now)
        else:
            save_file_name = '{0}'.format(figname)
        save_dir_name = '.'
        if is_make_dir:
            save_dir_name = '{0:%Y%m%d%H%M%S}'.format(now)
            os.mkdir(save_dir_name)
        plt.savefig('{0}/{1}.jpeg'.format(save_dir_name, save_file_name),
                    dpi=dpi, bbox_inches="tight")
        time.sleep(3)
        # メモリ解放
        plt.clf()
        plt.close()
        return self

    def return_ax(self):
        """
        axを返す
        """
        return self.ax


class PlotScatter(Setplot):
    """
    散布図
    Setplotを継承
    """

    def plot_scatter(self, x_data, y_data, label='data',
                     edgecolors='black', facecolor='None', **kwargs):
        """
        散布図を作成
        'ax.scatter'関係の細かい引数は'**kwargs'で投げる
        """
        self.ax.scatter(x_data, y_data, label=label,
                        edgecolors=edgecolors, facecolor=facecolor, s=80, **kwargs)
        return self


class PlotLine(Setplot):
    """
    折れ線グラグ
    """

    def plot_line(self, x_data, y_data, label='data', **kwargs):
        """
        折れ線グラフを作成
        """
        self.ax.plot(x_data, y_data, label=label, **kwargs)
        return self


class PlotBar(Setplot):
    """
    棒グラフ
    """

    def plot_bar(self, x_data, y_data, label='data', width=0.3, **kwargs):
        """
        棒グラフを作成
        """
        self.ax.bar(x_data, y_data, label=label, width=width, edgecolor='black',
                    linewidth=0.8, align="center", **kwargs)
        return self

    def mlt_plot_bar(self, x_data, y_data_list, label_list,
                     bar_color_list=('b', 'r', 'g', 'y'), width=0.3, **kwargs):
        """
        横に複数並べた棒グラフを作成。
        幾つかのこうもくを比較するのに使用。
        棒グラフの位置は'if..else..'の部分で処理。
        :param x_data: 各棒グラフのx軸位置情報
        :param y_data_list: 棒グラフの高さ
        :param label_list: 凡例。グラフに表示させるときは、'set_legend'
        :param bar_color_list:　棒グラフの色。デフォルトで、青、赤、緑、黄色の順
        :param width: 棒一本幅
        :param kwargs: 'ax.plotbar'関係の詳細な引数を投げる
        :return: self
        """
        len_data = len(y_data_list)
        if len_data % 2 == 0:
            st_bar_loc = x_data + 0.5 * width * (1 - len_data)
        else:
            st_bar_loc = x_data - width * (len_data - 1) * 0.5

        for i, (y_data, label) in enumerate(zip(y_data_list, label_list)):
            self.plot_bar(st_bar_loc, y_data, label=label, color=bar_color_list[i], **kwargs)
            st_bar_loc += width
        return self


if __name__ == '__main__':
    pass