# 自己写的测试
# import pandas as pd
# import json
# import os
# import random
#
# sys_path = "../dataset/cmdd/symptom_norm.csv"
# sys_n = pd.read_csv(sys_path)
# sys_n = sys_n['norm'].tolist()
# sys_norm = set(sys_n)
# print(sys_norm)
#
#
# def read_example_ids(fn):
#     """读取划分数据集的文件"""
#     example_ids = pd.read_csv(fn)
#     return example_ids
#
#
# example_ids = read_example_ids('../dataset/cmdd/split.csv')
#
# eids = example_ids[example_ids['split'] == 'train']['example_id'].to_list()
# print(eids)
