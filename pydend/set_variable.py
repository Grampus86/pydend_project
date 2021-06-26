import numpy as np
from pydend.input import df_modeling_param, df_conditon, df_export

cond_dict = df_conditon.set_index('Condition')['Value'].to_dict()

ele_dict = dict(map(reversed, df_modeling_param['Element'].to_dict().items()))

init_comp_array = \
    df_modeling_param.set_index('Element')['C0'].to_numpy()
d0_array = \
    df_modeling_param.set_index('Element')['D0'].to_numpy()
q_array = \
    df_modeling_param.set_index('Element')['Q'].to_numpy()
k_array = \
    df_modeling_param.set_index('Element')['K'].to_numpy()
m_array = \
    df_modeling_param.set_index('Element')['m'].to_numpy()

# 元素名
element_name_list = list(ele_dict.keys())

# 元素数
element_num = len(ele_dict)  # cell_array = np.arange(cond_dict['CELL_NUM'])

# デンドライトの樹幹距離
comp_array_length = int(cond_dict['CELL_NUM'])
x_length = cond_dict['X_LENGTH']
x_array = np.linspace(0, x_length, comp_array_length)

# 各元素の濃度の配列を初期化
comp_array = np.zeros((element_num, int(cond_dict['CELL_NUM'])))

# 残存する液相中の濃度配列を初期化
res_liq_comp_array = np.zeros(element_num)

# 温度の配列を初期化
temp_array = np.zeros(int(cond_dict['CELL_NUM']))

# 初期濃度を代入
for i in range(element_num):
    comp_array[i][:] = init_comp_array[i]

# 時間配列
dt = cond_dict['DELTA_TIME']
time_array = np.arange(dt, cond_dict['CALC_TIME'] + dt, dt)
end_time = cond_dict['CALC_TIME']
# 温度を初期化
temp_m = cond_dict['TEMP_M']
temp = temp_m
temp_l = temp_m

# 冷却速度
cooling_rate = cond_dict['COOLING_RATE']

# 界面のセルを初期化
solid_interface_cell = 0
liq_interface_cell = 1

# アウトプット用の変数
export_cond_dict = df_export.set_index('Condition')['Value'].to_dict()
delta_export_time = export_cond_dict['DELTA_EXPORT_TIME']
x_dist_min = export_cond_dict['X_DISTANCE_RANGE_MIN']
x_dist_max = export_cond_dict['X_DISTANCE_RANGE_MAX']
x_fs_min = export_cond_dict['X_FS_RANGE_MIN']
x_fs_max = export_cond_dict['X_FS_RANGE_MAX']
y_min = export_cond_dict['Y_RANGE_MIN']
y_max = export_cond_dict['Y_RANGE_MAX']
export_time = 0.00
