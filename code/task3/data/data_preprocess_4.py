# -*- coding:utf-8 -*-
#  XX
import pandas as pd
import json
import os
import random


def read_train_data(fn):
    """读取用于训练的json数据"""
    with open(fn, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
    return data


def read_test_data(fn):
    """读取用于测试的json数据"""
    with open(fn, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
    return data


def read_example_ids(fn):
    """读取划分数据集的文件"""
    example_ids = pd.read_csv(fn)
    return example_ids


def save_train_data(data, example_ids, mode):
    """
    训练集和验证集的数据转换 (trick：本次处理时将BIO转化为BIOES标注，以提高多任务训练的整体准确率)
    :param data: 用于训练的json数据
    :param example_ids: 样本id划分数据
    :param mode: train/dev
    :return:
    """
    eids = example_ids[example_ids['split'] == mode]['example_id'].to_list()

    sys_path = "../dataset/cmdd/symptom_norm.csv"
    sys_n = pd.read_csv(sys_path)
    sys_n = sys_n['norm'].tolist()
    sys_norm = set(sys_n)  # 病状词库

    seq_ins, seq_attrs, seq_types, seq_eids, seq_questions = [], [], [], [], []
    for eid in eids:
        # tmp_data = train里eid号数据
        tmp_data = data[str(eid)]
        # 提取数据中的对话
        tmp_dialogue = tmp_data['dialogue']
        # 取得分词结果
        tmp_types = tmp_data['implicit_info']['Symptom']  # 文本级label
        cur_len = 0
        seq_in, seq_attr, seq_type = [], [], []  # 句子组  症状组 XX组
        # 从当前对话中取出句子(for i)
        for i in range(len(tmp_dialogue)):
            # 取出对话内容中的句子和症状
            tmp_sent = tmp_dialogue[i]['speaker'] + '：' + tmp_dialogue[i]['sentence']  # 句子
            tmp_attr = tmp_dialogue[i]['symptom_norm']  # 症状

            if cur_len + len(tmp_sent) <= 254:
                if cur_len == 0:  # 首句
                    seq_in = tmp_sent
                    seq_attr = tmp_attr
                else:
                    seq_in = seq_in + ' ' + tmp_sent
                    seq_attr.extend(tmp_attr)
                cur_len = cur_len + len(tmp_sent)
            else:  # 超过max_len，重新开始

                s_attr = set(seq_attr)  # 症状组消重

                # 对先前存的句子中出现每一个症状都记下提问反馈 seq_eid seq_in seq_attr seq_question seq_type
                for attr in s_attr:
                    seq_eids.append(eid)  # 记下对话编号
                    seq_ins.append(seq_in)  # 句子
                    seq_attrs.append(attr)  # 症状
                    ### question generator ###
                    # seq_questions.append(attr)
                    seq_questions.append("是否患有" + attr + "?")
                    # seq_questions.append("是否患有" + attr +"症状?")
                    seq_types.append(tmp_types[attr])

                # 存完后，重新开始在新的一行记录
                seq_in = tmp_sent
                seq_attr = tmp_attr
                cur_len = len(tmp_sent)

        s_attr = set(seq_attr)
        none_attr = sys_norm - s_attr  # 不曾出现过的症状
        # 对最后一段句子中出现每一个症状都记下提问反馈 seq_eid seq_in seq_attr seq_question seq_type
        for attr in s_attr:
            seq_eids.append(eid)
            seq_ins.append(seq_in)
            seq_attrs.append(attr)
            # seq_questions.append(attr)
            seq_questions.append("是否患有" + attr + "?")
            # seq_questions.append("是否患有" + attr +"症状?")
            seq_types.append(tmp_types[attr])

        # 这一段代码👇额外加了一条在对话中没有出现过的症状并设为“3”（不知道为什么要这样做）
        # ###  加入none ####
        a_none = random.sample(none_attr, 1)
        seq_eids.append(eid)
        seq_ins.append(seq_in)
        seq_attrs.append(a_none[0])
        seq_questions.append("是否患有" + a_none[0] + "?")
        seq_types.append('3')

    assert len(seq_eids) == len(seq_ins) == len(seq_attrs) == len(seq_types) == len(seq_questions)
    print(mode, '句子数量为：', len(seq_ins))
    # 数据保存
    name = {
        "eids": seq_eids,
        "content": seq_ins,
        "question": seq_questions,
        "label": seq_types,
        "attr": seq_attrs
    }
    # 写入文件
    data = pd.DataFrame(name)
    # print(data.head(1))
    # data_dir = './data'
    # csv_path = os.path.join(data_dir, mode + '.csv')
    csv_path = os.path.join(mode + '.csv')
    data.to_csv(csv_path, index=False)


if __name__ == "__main__":
    train_data = read_train_data('../dataset/cmdd/train.json')
    example_ids = read_example_ids('../dataset/cmdd/split.csv')

    save_train_data(
        read_train_data('../dataset/cmdd/train.json'),
        example_ids,
        'train',
    )
    save_train_data(
        read_train_data('../dataset/cmdd/train.json'),
        example_ids,
        'dev',
    )
