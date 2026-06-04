# Text Renderer - OCR 训练数据生成工具

一个功能强大的 OCR（光学字符识别）训练数据生成框架，用于快速生成高质量的合成文本图像数据集。该项目基于 [oh-my-ocr/text_renderer](https://github.com/oh-my-ocr/text_renderer) 进行二次开发，针对实际应用场景进行了优化。

## 📋 目录

- [功能特点](#功能特点)
- [快速开始](#快速开始)
  - [环境要求](#环境要求)
  - [安装依赖](#安装依赖)
  - [基础示例](#基础示例)
- [项目结构](#项目结构)
- [核心模块](#核心模块)
- [配置指南](#配置指南)
- [数据处理流程](#数据处理流程)
- [常见用法](#常见用法)

## 🎯 功能特点

### 核心功能
- **多语言支持**：支持中文、英文、数字及混合文本生成
- **灵活的文本来源**：
  - 随机字符生成（Random Corpus）
  - 枚举文本生成（Enum Corpus）
  - 单词库生成（Word Corpus）
  - 字符级别生成（Character Corpus）
- **丰富的图像效果**：
  - 线条效果（Line Effect）
  - Dropout 效果（随机删除行/列）
  - Padding 效果（填充边距）
  - imgaug 增强效果集成
- **高级配置选项**：
  - 随机高度范围设置
  - 透视变换
  - 灰度/彩色生成
  - 文字颜色控制
  - 背景图片管理
- **高效的多进程生成**：支持多进程并行生成数据，提高效率
- **灵活的输出格式**：支持 LMDB 数据库和图像文件两种输出格式

### 应用场景
- 生成 OCR 模型训练数据
- 创建数据增强集合
- 快速验证 OCR 模型在不同场景下的表现

## 🚀 快速开始

### 环境要求

- Python >= 3.6
- 支持平台：Windows、Linux、macOS

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd text_renderer-master_zl

# 安装项目及其依赖
pip install -e .

# 安装额外依赖
pip install opencv-python pillow numpy loguru imgaug imutils tqdm
```

### 基础示例

**方式1：使用配置文件生成数据**

```bash
# 使用默认配置
python main.py --config example_data/zl_example.py --dataset img --num_processes 4

# 指定进程数
python main.py --config example_data/zl_example.py --dataset img --num_processes 2

# 使用单进程（调试模式）
python main.py --config example_data/zl_example.py --dataset img --num_processes 0
```

**参数说明：**
- `--config`：配置文件路径（Python 文件）
- `--dataset`：输出格式，`img`（图像文件）或 `lmdb`（LMDB 数据库）
- `--num_processes`：并行进程数，0 表示单进程
- `--log_period`：日志输出周期（百分比，默认 10）

**方式2：Python 代码中直接使用**

```python
from text_renderer.render import Render
from text_renderer.config import RenderCfg, GeneratorCfg, CharCorpusCfg, CharCorpus
from text_renderer.effect import Effects, Line

# 创建文本语料库
corpus_cfg = CharCorpusCfg(
    text_paths=['path/to/text.txt'],
    chars_file='path/to/chars.txt',
    font_dir='path/to/fonts',
    font_list_file='path/to/font_list.txt',
    font_size=(32, 48),
    length=(5, 10)
)
corpus = CharCorpus(corpus_cfg)

# 创建渲染配置
render_cfg = RenderCfg(
    bg_dir='path/to/backgrounds',
    corpus=corpus,
    corpus_effects=Effects([Line(p=0.5)]),
    gray=True
)

# 生成数据
renderer = Render(render_cfg)
image, label = renderer()
```

## 📁 项目结构

```
text_renderer-master_zl/
├── main.py                          # 主程序入口
├── setup.py                         # 项目配置
├── README.md                        # 项目文档
│
├── text_renderer/                   # 核心库
│   ├── __init__.py
│   ├── render.py                    # 渲染引擎（关键）
│   ├── dataset.py                   # 数据存储接口
│   ├── bg_manager.py                # 背景图片管理器
│   ├── font_manager.py              # 字体管理器
│   │
│   ├── config/                      # 配置模块
│   │   └── __init__.py              # 配置类定义
│   │
│   ├── corpus/                      # 文本语料库
│   │   ├── corpus.py                # 基类
│   │   ├── char_corpus.py           # 字符级语料库
│   │   ├── word_corpus.py           # 单词级语料库
│   │   ├── enum_corpus.py           # 枚举文本语料库
│   │   ├── rand_corpus.py           # 随机字符语料库
│   │   └── __init__.py
│   │
│   ├── effect/                      # 图像效果模块
│   │   ├── base_effect.py           # 效果基类
│   │   ├── line.py                  # 线条效果
│   │   ├── padding.py               # 填充效果
│   │   ├── dropout_*.py             # Dropout 效果
│   │   ├── imgaug_effect.py         # imgaug 集成
│   │   ├── selector.py              # 效果选择器
│   │   └── __init__.py
│   │
│   ├── layout/                      # 布局模块
│   │   ├── same_line.py             # 单行布局
│   │   └── extra_text_line.py       # 多行布局
│   │
│   ├── utils/                       # 工具函数
│   │   ├── bbox.py                  # 边界框计算
│   │   ├── draw_utils.py            # 绘制工具
│   │   ├── font_text.py             # 字体文本处理
│   │   └── ...
│   │
│   └── tests/                       # 测试模块
│       ├── test_*.py
│       └── data/
│
├── example_data/                    # 示例数据和配置
│   ├── example.py                   # 完整示例配置
│   ├── zl_example.py                # 优化版配置（推荐）
│   ├── effect_layout_example.py     # 效果和布局示例
│   │
│   ├── bg/                          # 背景图片
│   ├── font/                        # 字体文件
│   ├── char/                        # 字符集文件
│   ├── text/                        # 文本文件
│   └── font_list/                   # 字体列表
│
├── 1_DataSetGet/                    # 数据处理工具
│   ├── ch/                          # 中文数据处理
│   │   ├── 0_获得训练集和验证集.py  # 划分训练/验证集
│   │   ├── 1_符号验证.py            # 验证字符有效性
│   │   ├── 2_训练数据生成.py        # 生成训练数据
│   │   └── ppocr_keys_v1.txt        # 字符词典
│   │
│   └── en/                          # 英文数据处理
│       ├── 0_获得训练集和验证集.py
│       ├── 1_符号验证.py
│       ├── 2_训练数据生成.py
│       ├── en_dict.txt
│       └── ...
│
├── tools/                           # 辅助工具
│   ├── check_fonts.py               # 字体检查
│   ├── font_viewer.py               # 字体查看器
│   ├── lmdb2img.py                  # LMDB 转图像
│   └── prepare_effect_layout_example.py
│
└── docs/                            # 文档
    ├── corpus/                      # 语料库文档
    ├── effect/                      # 效果文档
    ├── config.rst
    └── ...
```

## 🔧 核心模块

### 1. Render（渲染引擎）
```python
from text_renderer.render import Render

# 创建渲染器
renderer = Render(render_cfg)

# 生成单张图像
image, label = renderer()
```

### 2. Corpus（文本语料库）

**CharCorpus - 字符级别**
```python
from text_renderer.corpus import CharCorpus, CharCorpusCfg

cfg = CharCorpusCfg(
    text_paths=['chn_text.txt'],        # 文本文件路径
    chars_file='chn.txt',               # 字符集文件
    font_dir='./fonts',                 # 字体目录
    font_list_file='font_list.txt',     # 字体列表
    font_size=(30, 50),                 # (最小, 最大) 字体大小
    length=(5, 15),                     # 文本长度范围
    char_spacing=(-0.3, 1.3)            # 字符间距范围
)
corpus = CharCorpus(cfg)
```

**RandCorpus - 随机字符**
```python
from text_renderer.corpus import RandCorpus, RandCorpusCfg

cfg = RandCorpusCfg(
    chars_file='chn.txt',               # 字符集文件
    font_dir='./fonts',
    font_list_file='font_list.txt',
    font_size=(30, 50),
    length=(5, 20)                      # 随机长度
)
corpus = RandCorpus(cfg)
```

**WordCorpus - 单词级别**
```python
from text_renderer.corpus import WordCorpus, WordCorpusCfg

cfg = WordCorpusCfg(
    text_paths=['words.txt'],           # 单词文件
    font_dir='./fonts',
    font_list_file='font_list.txt',
    font_size=(30, 50),
    num_word=(1, 3)                     # 每张图像的单词数
)
corpus = WordCorpus(cfg)
```

### 3. Effects（图像效果）

```python
from text_renderer.effect import Effects, Line, Padding, DropoutRand, OneOf

# 创建效果链
effects = Effects([
    Line(p=0.8, thickness=(2, 8)),              # 添加线条，概率80%
    Padding(p=0.5, w_ratio=[0.2, 0.3]),        # 添加填充，概率50%
    OneOf([DropoutRand(), DropoutVertical()])   # 随机选择一个效果
])
```

### 4. Config（配置）

```python
from text_renderer.config import RenderCfg, GeneratorCfg, NormPerspectiveTransformCfg

# 渲染配置
render_cfg = RenderCfg(
    bg_dir='./backgrounds',
    height=(32, 64),                    # 图像高度范围
    width=None,                         # 自动调整宽度
    gray=True,                          # 灰度图
    perspective_transform=NormPerspectiveTransformCfg(10, 10, 1.5),
    corpus=corpus,
    corpus_effects=effects
)

# 生成器配置
gen_cfg = GeneratorCfg(
    num_image=10000,                    # 要生成的图像数量
    save_dir='./output',                # 输出目录
    render_cfg=render_cfg
)
```

## ⚙️ 配置指南

### 推荐配置示例（zl_example.py）

```python
# 中文数据生成配置
def chn_data():
    return GeneratorCfg(
        num_image=2000,                 # 生成 2000 张图像
        save_dir=OUT_DIR / "chn_data",
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            height=(32, 64),            # 随机高度 32-64 像素
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            gray=False,                 # 彩色输出
            corpus=get_char_corpus(),
            corpus_effects=Effects([
                Line(0.5, color_cfg=FixedTextColorCfg())
            ])
        ),
    )
```

### 关键配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `num_image` | 要生成的图像数量 | 10000 |
| `save_dir` | 输出目录 | `./output/train` |
| `height` | 图像高度范围 | `(32, 64)` |
| `width` | 图像宽度范围，None 自动 | `None` |
| `gray` | 是否生成灰度图 | `True` 或 `False` |
| `font_size` | 字体大小范围 | `(30, 50)` |
| `length` | 文本长度范围 | `(5, 15)` |

## 📊 数据处理流程

### 完整工作流程

```
1. 准备资源
   ├── 背景图片 (backgrounds/)
   ├── 字体文件 (fonts/)
   ├── 文本文件 (text_data.txt)
   └── 字符集 (chars.txt)

2. 配置参数
   ├── 创建 .py 配置文件
   └── 指定语料库、效果、输出路径

3. 生成数据
   ├── 多进程并行渲染
   ├── 应用图像效果
   └── 保存到指定格式

4. 验证数据
   ├── 符号验证（1_DataSetGet/ch/1_符号验证.py）
   └── 数据集检查

5. 划分数据集
   ├── 训练集 (train/)
   ├── 验证集 (val/)
   └── 测试集 (test/)
```

### 中文数据处理示例

```bash
# 1. 生成原始数据
python main.py --config example_data/zl_example.py --num_processes 4

# 2. 验证字符有效性
cd 1_DataSetGet/ch
python 1_符号验证.py

# 3. 划分训练集和验证集
python 0_获得训练集和验证集.py

# 4. 生成最终训练数据
python 2_训练数据生成.py
```

## 💡 常见用法

### 1. 生成特定语言的数据

**中文**
```python
corpus = CharCorpus(
    CharCorpusCfg(
        text_paths=['chn_text.txt'],
        chars_file='chn.txt',
        **font_cfg_zh  # 使用中文字体列表
    )
)
```

**英文**
```python
corpus = WordCorpus(
    WordCorpusCfg(
        text_paths=['eng_words.txt'],
        chars_file='eng.txt',
        **font_cfg
    )
)
```

### 2. 自定义图像效果

```python
# 强效果：线条 + 填充 + Dropout
effects = Effects([
    Line(p=0.8, thickness=(2, 10)),
    Padding(p=0.5, w_ratio=[0.1, 0.3], h_ratio=[0.05, 0.2]),
    DropoutRand(p=0.3),
    ImgAugEffect(aug=iaa.Emboss(alpha=(0.9, 1.0)))
])

# 弱效果：仅线条
effects = Effects([Line(p=0.3)])

# 无效果
effects = Effects([])
```

### 3. 多语言混合生成

```python
configs = [
    chn_data(),         # 中文数据
    eng_word_data(),    # 英文单词
    rand_data(),        # 随机字符
]
```

### 4. 调整输出格式

```bash
# 输出为图像文件（推荐用于 OCR 训练）
python main.py --dataset img

# 输出为 LMDB 数据库（高效存储）
python main.py --dataset lmdb
```

### 5. 性能优化

```bash
# 增加进程数提高速度（根据 CPU 核心数调整）
python main.py --num_processes 8

# 单进程调试模式（检查配置是否正确）
python main.py --num_processes 0
```

## 🛠️ 辅助工具

### 字体查看器
```bash
python tools/font_viewer.py
```
查看系统可用字体。

### 检查字体
```bash
python tools/check_fonts.py --font_dir ./fonts
```
验证字体文件是否有效。

### LMDB 转图像
```bash
python tools/lmdb2img.py --lmdb_path ./data.lmdb --output_dir ./images
```
将 LMDB 数据库转换为单独的图像文件。

## 📝 配置文件示例模板

```python
# my_config.py
import inspect
from pathlib import Path
from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import RenderCfg, GeneratorCfg

CURRENT_DIR = Path(__file__).parent
OUT_DIR = CURRENT_DIR / "output"
BG_DIR = CURRENT_DIR / "backgrounds"
FONT_DIR = CURRENT_DIR / "fonts"
TEXT_DIR = CURRENT_DIR / "texts"

def my_dataset():
    return GeneratorCfg(
        num_image=5000,
        save_dir=OUT_DIR / "my_dataset",
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            height=(48, 64),
            gray=False,
            corpus=CharCorpus(
                CharCorpusCfg(
                    text_paths=[TEXT_DIR / "my_text.txt"],
                    chars_file=TEXT_DIR / "chars.txt",
                    font_dir=FONT_DIR,
                    font_list_file=FONT_DIR / "font_list.txt",
                    font_size=(40, 60),
                    length=(5, 20)
                )
            ),
            corpus_effects=Effects([
                Line(p=0.5, thickness=(2, 5)),
                Padding(p=0.3)
            ])
        ),
    )

configs = [my_dataset()]
```

## 🐛 常见问题

**Q: 生成速度很慢？**
A: 增加 `--num_processes` 参数，并确保 CPU 核心足够。

**Q: 字符显示不正确？**
A: 检查字体文件是否支持相应语言，验证 `chars_file` 和 `font_list_file` 配置。

**Q: 内存占用过高？**
A: 减少 `--num_processes` 数量，或减小批处理队列大小。

**Q: 输出图像尺寸不一致？**
A: 设置固定的 `height` 值，`width` 保持 `None` 自动调整。

## 📚 参考资源

- 原始项目：[oh-my-ocr/text_renderer](https://github.com/oh-my-ocr/text_renderer)
- OCR 模型：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- 数据增强：[imgaug](https://github.com/aleju/imgaug)

## 📄 许可证

本项目继承原始项目的许可证。详见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
