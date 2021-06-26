import pandas as pd
import pydend.set_path as path

"""
input.xlsxからパラメータを取得
"""
# df_modeling_param = pd.read_excel('/Users/kota/Desktop/pydend_project/input.xlsx', sheet_name='param')
df_modeling_param = pd.read_excel('{}/input.xlsx'.format(path.input_file_path), sheet_name='param')
df_conditon = pd.read_excel('{}/input.xlsx'.format(path.input_file_path), sheet_name='condition')
df_export = pd.read_excel('{}/input.xlsx'.format(path.input_file_path), sheet_name='export')
