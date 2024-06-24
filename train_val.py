i# 导入所需的模块和库
import datetime  # 用于处理日期和时间
import shutil  # 用于文件和目录操作
from pathlib import Path  # 用于处理文件路径
from collections import Counter  # 用于计数可哈希对象的出现次数

import yaml  # 用于读写YAML文件（一种用于配置文件的格式）
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据处理和分析
from ultralytics import YOLO  # 用于使用YOLO算法进行目标检测
from sklearn.model_selection import KFold  # 用于进行K折交叉验证
dataset_path = Path('E:\Transmmison and Distribution Infrastucture Imagery Dataset\Sample Data\images') # replace with 'path/to/dataset' for your custom data
labels = sorted(dataset_path.rglob("E:\Transmmison and Distribution Infrastucture Imagery Dataset\Sample Data\labels")) # all data in 'labels'
yaml_file = Path(r"Fruits-detection\data.yaml")
# 使用with语句打开YAML文件，确保在处理完后自动关闭文件，以避免资源泄漏
# yaml_file_path: 包含类别信息的YAML文件的路径
with open(yaml_file, 'r', encoding="utf8") as y:
    # 使用yaml.safe_load()函数加载YAML文件的内容
    # 这里假设YAML文件的内容是字典类型，其中包含一个键为'names'的列表，表示类别名称
    # safe_load()函数能够安全地将YAML数据转换为Python对象，避免了可能的安全风险
    classes = yaml.safe_load(y)['names']
# 对类别信息进行处理
# classes: 包含类别名称的列表
# classes字典的键是类别名称，值是对应的索引
# 为了按照类别名称的字母顺序排序索引，我们首先需要获取所有类别名称的列表，并对其进行排序
cls_idx = sorted(classes.keys())
# indx: 一个包含文件路径的列表
# l.stem: 使用Path.stem属性从文件路径中提取基本文件名（不包含扩展名）
# 使用列表推导式将所有文件的基本文件名提取出来，存储在indx列表中
indx = [l.stem for l in labels]

# 创建一个空的Pandas DataFrame，用于存储标签信息
# labels_df: 存储标签信息的DataFrame
# columns=cls_idx: DataFrame的列使用之前定义的cls_idx列表（按类别名称的字母顺序排序）
# index=indx: DataFrame的索引使用之前从文件路径中提取的基本文件名列表indx
labels_df = pd.DataFrame([], columns=cls_idx, index=indx)
# 遍历标签文件列表
# labels: 包含标签文件路径的列表
for label in labels:
    # 创建一个Counter对象，用于统计每个标签文件中各个类别的出现次数
    lbl_counter = Counter()

    # 使用with语句打开标签文件，确保在处理完后自动关闭文件，以避免资源泄漏
    # label: 当前标签文件的路径
    with open(label, 'r') as lf:
        # 逐行读取标签文件的内容，并存储在lines列表中
        lines = lf.readlines()

    # 遍历标签文件中的每一行
    for l in lines:
        # YOLO标签格式使用整数作为每行的第一个位置来表示类别
        # 使用split()函数根据空格分隔每一行，并提取出第一个整数，将其作为类别索引
        # 将类别索引及其出现次数添加到lbl_counter中进行统计
        lbl_counter[int(l.split(' ')[0])] += 1

    # 将当前标签文件对应的类别出现次数更新到labels_df的相应行
    # label.stem: 使用Path.stem属性从文件路径中提取基本文件名（不包含扩展名）
    labels_df.loc[label.stem] = lbl_counter

# 使用0.0替换DataFrame中的NaN值（如果有的话）
# 这样可以确保所有的缺失值（NaN）都被替换为0.0
labels_df = labels_df.fillna(0.0)

# ksplit: 指定K折交叉验证的折数（将数据集划分为多少个子集）
ksplit = 5

# 创建一个KFold对象，用于执行K折交叉验证
# n_splits: 指定K折交叉验证的折数
# shuffle: 指定是否在进行划分之前对数据进行洗牌（打乱顺序）
# random_state: 随机种子，用于确保结果可重复
kf = KFold(n_splits=ksplit, shuffle=True, random_state=20)

# 使用KFold对象对数据进行K折交叉验证，并将结果存储在kfolds列表中
# labels_df: 包含标签信息的Pandas DataFrame
kfolds = list(kf.split(labels_df))
# 创建一个列表，用于存储每个子集的名称
# 例如，对于K=5的情况，folds将包含['split_1', 'split_2', 'split_3', 'split_4', 'split_5']
folds = [f'split_{n}' for n in range(1, ksplit + 1)]

# 创建一个空的Pandas DataFrame，用于标识每个样本所属的训练集或验证集
# indx: 包含文件基本名称的列表（之前从文件路径中提取的基本文件名列表）
# folds: 列名，表示每个子集的名称
folds_df = pd.DataFrame(index=indx, columns=folds)

# 遍历K折交叉验证的每个子集，并将训练集和验证集的样本标记为'train'和'val'
# idx: 当前子集的索引（从1开始，表示第几个子集）
# (train, val): 当前子集的训练集和验证集索引
for idx, (train, val) in enumerate(kfolds, start=1):
    # 将训练集的样本标记为'train'
    # labels_df.iloc[train].index: 使用训练集的索引获取对应的样本基本文件名列表
    # folds_df[f'split_{idx}'].loc[labels_df.iloc[train].index]: 将这些样本在folds_df的对应列中标记为'train'
    folds_df[f'split_{idx}'].loc[labels_df.iloc[train].index] = 'train'

    # 将验证集的样本标记为'val'
    # labels_df.iloc[val].index: 使用验证集的索引获取对应的样本基本文件名列表
    # folds_df[f'split_{idx}'].loc[labels_df.iloc[val].index]: 将这些样本在folds_df的对应列中标记为'val'
    folds_df[f'split_{idx}'].loc[labels_df.iloc[val].index] = 'val'
# 创建一个空的Pandas DataFrame，用于存储每个交叉验证子集中各个类别的样本分布比例
# index=folds: 行索引使用之前创建的子集名称列表
# columns=cls_idx: 列索引使用之前定义的cls_idx列表（按类别名称的字母顺序排序）
fold_lbl_distrb = pd.DataFrame(index=folds, columns=cls_idx)

# 遍历K折交叉验证的每个子集，并计算训练集和验证集中各个类别的样本分布比例
# n: 当前子集的索引（从1开始，表示第几个子集）
# (train_indices, val_indices): 当前子集的训练集和验证集的索引
for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
    # 使用训练集的索引计算训练集中各个类别的样本总数
    train_totals = labels_df.iloc[train_indices].sum()

    # 使用验证集的索引计算验证集中各个类别的样本总数
    val_totals = labels_df.iloc[val_indices].sum()

    # 计算验证集中各个类别样本数与训练集中各个类别样本数的分布比例
    # ratio: 一个包含分布比例的Series，其中索引为类别名称，值为对应的比例
    # 为避免除以零的情况，我们在分母上添加了一个小值（1E-7）
    ratio = val_totals / (train_totals + 1E-7)

    # 将当前子集的分布比例信息更新到fold_lbl_distrb的相应行
    # fold_lbl_distrb.loc[f'split_{n}']: 获取当前子集的行
    # ratio: 将当前子集的分布比例信息存储到对应的行中
    fold_lbl_distrb.loc[f'split_{n}'] = ratio
# 创建保存数据集的目录路径
# dataset_path: 包含数据集的路径
# datetime.date.today().isoformat(): 获取当前日期的ISO格式字符串（YYYY-MM-DD）
# ksplit: K折交叉验证的折数
save_path = Path(dataset_path / f'{datetime.date.today().isoformat()}_{ksplit}-Fold_Cross-val')
save_path.mkdir(parents=True, exist_ok=True)

# 获取所有图片文件的路径，并按文件名进行排序
# images: 包含所有图片文件的路径列表
images = sorted(dataset_path.rglob("*images/*.jpg"))  # 可根据需要更改文件扩展名
# print(images)

# 存储所有数据集的YAML文件路径列表
ds_yamls = []

# 遍历每个交叉验证子集，并为每个子集创建目录结构和数据集YAML文件
# split: 每个交叉验证子集的名称（之前的split名称，如'split_1'）
for split in folds_df.columns:
    # 创建当前子集的目录
    split_dir = save_path / split
    split_dir.mkdir(parents=True, exist_ok=True)

    # 创建子集中的训练集和验证集的目录
    (split_dir / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'labels').mkdir(parents=True, exist_ok=True)

    # 创建当前子集的数据集配置文件（YAML文件）
    dataset_yaml = split_dir / f'{split}_dataset.yaml'
    ds_yamls.append(dataset_yaml)

    # 将数据集信息写入数据集配置文件
    with open(dataset_yaml, 'w') as ds_y:
        # 使用yaml.safe_dump()函数将数据写入YAML文件
        yaml.safe_dump({
            'path': save_path.as_posix(),  # 数据集根目录路径
            'train': 'train',  # 训练集所在的子目录名称
            'val': 'val',  # 验证集所在的子目录名称
            'names': classes  # 数据集类别信息
        }, ds_y)

# 遍历图像文件和标签文件，使用zip()函数将它们一一对应起来
# images: 包含所有图像文件路径的列表
# labels: 包含所有标签文件路径的列表
for image, label in zip(images, labels):
    # 根据图像文件的基本名称（不包含扩展名）找到它所属的交叉验证子集和数据拆分（train/val）
    # 对应的split和k_split将是字符串，表示图像所属的子集和数据拆分（train或val）
    for split, k_split in folds_df.loc[image.stem].items():
        # 获取目标目录的路径
        img_to_path = save_path / split / k_split / 'images'  # 图像文件的目标目录
        lbl_to_path = save_path / split / k_split / 'labels'  # 标签文件的目标目录

        # 将图像文件和标签文件复制到新目录
        # 使用shutil.copy()函数复制文件到目标目录
        # img_to_path / image.name: 目标目录中图像文件的完整路径
        # lbl_to_path / label.name: 目标目录中标签文件的完整路径
        # 如果文件已存在，则可能引发SamefileError，这意味着某个文件在目标目录中已经存在
        shutil.copy(image, img_to_path / image.name)  # 复制图像文件
        shutil.copy(label, lbl_to_path / label.name)  # 复制标签文件
