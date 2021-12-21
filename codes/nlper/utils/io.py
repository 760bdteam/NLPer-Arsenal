r"""
对数据样例的读取与保存
"""

import os
import json
import pandas as pd
import yaml


def create_parentDir(path, exist_ok=True):
    head, tail = os.path.split(path)
    if head and not os.path.exists(head):
        print(f'create {head} directory')
        os.makedirs(head, exist_ok=exist_ok)


def load_nlp_data(file, task_name='text_clf'):
    """读取不同任务的标准数据

    :param file: data file
    :param task_name: one of ['text_clf']
    :return: target data
    """
    if task_name == 'text_clf':
        raw_data = read_data(file, f_type='txt')
        target_data = []
        for raw_instance in raw_data:
            split_instance = raw_instance.split('\t')
            if len(split_instance) == 2:  # with label
                split_instance[1] = int(split_instance[1])  # int(label)
            target_data.append(split_instance)
    else:
        raise ValueError(f'load {task_name} failed, we only support load text_clf data now')
    return target_data


def read_data(file, f_type=None):
    """read data from file

    :param file: file path
    :param f_type: one of ['txt', 'json', 'csv', 'tsv', 'yaml'], default: file postfix
    :return: target data
    """
    # 根据文件后缀自动选择读取方式
    f_type = os.path.splitext(file)[-1].replace('.', '') if not f_type else f_type
    if f_type == 'txt':
        with open(file, encoding='utf-8') as f:
            data = [line.strip() for line in f]
    elif f_type == 'json':
        with open(file, encoding='utf-8') as f:
            data = json.load(f)
    elif f_type == 'csv':
        data = pd.read_csv(file)
    elif f_type == 'tsv':
        data = pd.read_csv(file, sep='\t')
    elif f_type == 'yaml':
        with open(file, encoding='utf-8') as f:
            data = yaml.safe_load(f)
    else:
        raise ValueError('f_type should be one of [txt, json, csv, tsv, yaml]')
    if f_type != 'yaml':
        print(f'{file} -> {f_type} data over, nums: {len(data)}')
    return data


def save_data(data, saved_path, f_type='txt'):
    create_parentDir(saved_path)
    with open(saved_path, 'w', encoding='utf-8') as f:
        if f_type == 'txt':
            for example in data:
                f.write(str(example) + '\n')
        elif f_type == 'json':
            json.dump(data, f, ensure_ascii=False, indent=1)
        else:
            raise ValueError('f_type should be one of [txt, json]')
    print(f'{f_type} data -> {saved_path} over')
