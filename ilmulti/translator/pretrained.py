
"""
This file creates models already trained and available.
"""

import os

from .args import Args
from .translator import FairseqTranslator
from ..segment import SimpleSegmenter
from ..sentencepiece import SentencePieceTokenizer

ILMULTI_DIR = os.path.join(os.environ['HOME'], '.ilmulti')

def download_resources(url, save_path=ILMULTI_DIR):
    pass


class mm_all:
    def __init__(self, root=os.path.join(ILMULTI_DIR, 'mm-all')):
        model_path = os.path.join(root, 'model.pt')
        # If not model path, wire to download later.

        args = Args(
            path=model_path, max_tokens=1000, task='translation',
            source_lang='src', target_lang='tgt', buffer_size=2,
            data=[root]
        )

        parser = fairseq.options.get_generation_parser(interactive=True)
        default_args = fairseq.options.parse_args_and_arch(parser,
                input_args=['dummy-data'])

        kw = dict(default_args._get_kwargs())
        args.enhance(print_alignment=True)
        args.enhance(**kw)
        fseq_translator = FairseqTranslator(args)
        segmenter = ilmulti.segment.SimpleSegmenter()
        tokenizer = ilmulti.sentencepiece.SentencePieceTokenizer()
        self.engine = MTEngine(fseq_translator, segmenter, tokenizer)

    def __call__(self, *args, **kwargs):
        return self.engine(*args, **kwargs)