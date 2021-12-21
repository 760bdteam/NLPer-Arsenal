"""
dataset explore for each task
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List
from collections import Counter
from nlper.utils import read_data, seed_everything
from matplotlib.font_manager import FontProperties


seed_everything()
font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')
font.set_style('normal')
font.set_size(12)


def CharTokenizer(s: str):
    return list(s)


def WhitespaceTokenizer(s: str):
    return s.split(' ')


def len_distribution(data: Union[List[str], List[List[str]]], title:str, tokenizer=None):
    if tokenizer:
        instance_lens = [len(tokenizer(ins)) for ins in data]
    else:
        instance_lens = [len(ins) for ins in data]
    print(f'min: {np.min(instance_lens)}, max: {np.max(instance_lens)},'
          f'median: {np.median(instance_lens)}, mean: {np.mean(instance_lens):.2f}')

    # 默认只覆盖98%的数据分布
    p = 98
    boundary = np.percentile(instance_lens, p)
    print(f'set max_length to {int(boundary)} can cover {p}% data instances')
    plot_instance_lens = [len(ins[:int(boundary)]) for ins in data]

    plt.figure(figsize=(8, 5), dpi=300)
    plt.style.use(['science', 'no-latex'])
    sns.distplot(plot_instance_lens)
    # todo: add text
    # plt.text(0.8, 0.8, f'cover {p}%: {int(boundary)}')
    
    plt.xticks(font_properties=font)
    plt.yticks(font_properties=font)

    plt.gca().set_xlabel('instance length', font_properties=font, fontsize=16)
    plt.gca().set_ylabel('frequency', font_properties=font, fontsize=16)

    plt.title(f"length distribution of {title}", font_properties=font, fontsize=20)
    plt.show()


def label_distribution(data: List[Union[str, int]], title:str):
    label_counter = Counter(data)
    # 固定画图顺序，保持颜色一致
    sorted_item = sorted(label_counter.items(), key=lambda x:(x[0]), reverse=True)
    keys, values = zip(*sorted_item)

    plt.figure(figsize=(8, 8), dpi=300)
    plt.style.use(['science', 'no-latex'])
    plt.pie(values, labels=keys, autopct='%1.1f%%')
    
    plt.title(f"label distribution of {title}", font_properties=font, fontsize=20)
    plt.show()


if __name__ == '__main__':
    raw_data = read_data('smp2020-ewect/usual/test.tsv')
    text, label = [], []
    label_map = {
        0: 'neutral',
        1: 'angry',
        2: 'happy',
        3: 'sad',
        4: 'fear',
        5: 'surprise'
    }
    for idx, row in raw_data.iterrows():
        text.append(row['text_a'])
        label.append(label_map[row['label']])
    len_distribution(text, title='smp2020 usual test')
    label_distribution(label, title='smp2020 usual test')
