import sys
from pathlib import Path
sys.path.insert(1, str(Path(__file__).parent))

# autopep8: off - the stuff at the top needs to STAY at the top
import gc
import logging
import os
import signal

from .args import parser
from latexmt_core.context_logger import ContextLogger
from latexmt_core.get_translator import get_translator_aligner
from latexmt_core.glossary import Glossary, load_glossary
# autopep8: on


def main():
    args = parser.parse_args()

    if 'help' in args:
        parser.print_usage()
        sys.exit(0)

    logging.setLoggerClass(ContextLogger)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(levelname)s:%(name)s:%(message)s\tcontext=%(context)s', defaults={'context': {}}))
    logging.basicConfig(level=args.log_level, handlers=[handler])

    translator, aligner = get_translator_aligner(
        src_lang=args.src_lang, tgt_lang=args.tgt_lang,
        trans_type=args.translator, align_type=args.aligner,
        opus_model_base=args.opus_model_base,
        logger=logging.getLogger(__name__)
    )

    glossary: Glossary = dict()
    if args.glossary is not None:
        glossary = load_glossary(csv_path=Path(args.glossary))

    from latexmt_core.document_processor import DocumentTranslator
    processor = DocumentTranslator(translator=translator,
                                   aligner=aligner,
                                   recurse_input=True,
                                   glossary=glossary,
                                   glossary_method=args.glossary_method,
                                   glossary_fallback=args.glossary_fallback)

    if len(args.root_documents) == 0:
        args.root_documents = [Path('-')]

    for root_document in args.root_documents:
        root_document = Path(root_document)
        root_output_dir = Path(args.output)
        processor.process_document(root_document, root_output_dir)
    # for root_document

    # manual exit; workaround for hang in /lib/python3.12/threading.py
    sys.stdout.flush()
    sys.stderr.flush()
    del processor
    del translator
    del aligner
    gc.collect()
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == '__main__':
    main()
