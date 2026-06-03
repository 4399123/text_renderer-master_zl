import inspect
import os
from pathlib import Path
import imgaug.augmenters as iaa

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    FixedTextColorCfg,
)
from text_renderer.layout.same_line import SameLineLayout
from text_renderer.layout.extra_text_line import ExtraTextLineLayout


CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "zl_output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg"
CHAR_DIR = DATA_DIR / "char"
FONT_DIR = DATA_DIR / "font"
FONT_LIST_DIR = DATA_DIR / "font_list"
TEXT_DIR = DATA_DIR / "text"

font_cfg = dict(
    font_dir=FONT_DIR,
    font_list_file=FONT_LIST_DIR / "font_list.txt",
    font_size=(640, 800),   #（最小，最大）
)

perspective_transform = NormPerspectiveTransformCfg(20, 20, 1.5)


def get_char_corpus():
    return CharCorpus(
        CharCorpusCfg(
            text_paths=[TEXT_DIR / "chn_text.txt", TEXT_DIR / "eng_text.txt"],
            filter_by_chars=True,
            chars_file=CHAR_DIR / "chn.txt",
            length=(5, 10),
            char_spacing=(-0.3, 1.3),
            **font_cfg
        ),
    )


def base_cfg(
    name: str, corpus, corpus_effects=None, layout_effects=None, layout=None, gray=True
):
    return GeneratorCfg(
        num_image=2000,
        save_dir=OUT_DIR / name,
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            height=(32, 64),  # 随机高度范围（最小, 最大）
            perspective_transform=perspective_transform,
            gray=False,
            layout_effects=layout_effects,
            layout=layout,
            corpus=corpus,
            corpus_effects=Effects(
            [
                Line(0.8, thickness=(2, 10),),
                OneOf([DropoutRand(), DropoutVertical()]),
            ])

        ),
    )


def chn_data():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=get_char_corpus(),
        corpus_effects=Effects(
            [
                Line(0.5, color_cfg=FixedTextColorCfg()),
                OneOf([DropoutRand(), DropoutVertical()]),
            ]
        ),
    )


def enum_data():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=EnumCorpus(
            EnumCorpusCfg(
                text_paths=[TEXT_DIR / "enum_text.txt"],
                filter_by_chars=True,
                chars_file=CHAR_DIR / "chn.txt",
                **font_cfg
            ),
        ),
    )


def rand_data():
    """
    生成随机字符数据配置

    使用随机字符语料库生成指定长度范围的字符数据。

    """
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=RandCorpus(
            RandCorpusCfg(chars_file=CHAR_DIR / "eng_with_dig.txt",
                          length=(3,30),
                          # text_color_cfg=FixedTextColorCfg(), ##固定为黑色字体
                          **font_cfg),
        ),
    )


def eng_word_data():
    """
    生成英文单词数据配置

    """
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[TEXT_DIR / "pack_text.txt"],   #需要用脚本提前写好大量单词
                # filter_by_chars=True,                      #从text_paths过滤chars_file不存在的字符
                # chars_file=CHAR_DIR / "eng_with_dig.txt",
                # text_color_cfg=FixedTextColorCfg(), ##固定为黑色字体
                num_word=(1,1),
                **font_cfg
            ),
        ),
    )



# fmt: off
# The configuration file must have a configs variable
configs = [
    # chn_data(),
    # enum_data(),
    rand_data(),        #生成随机长度字符数据
    # eng_word_data(),  #生成英文单词and数字数据
]
# fmt: on
