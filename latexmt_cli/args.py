import argparse


parser = argparse.ArgumentParser(
    prog='latexmt', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
    'root_documents',
    nargs='*',
    help='filename(s) of LaTeX root document(s) to be translated\npass \'-\' or omit for stdin')
parser.add_argument(
    '-o', '--output',
    help='directory name for output documents\npass \'-\' to direct all output to stdout',
    default='./latexmt_out',
    required=False)
parser.add_argument(
    '-s', '--src-lang',
    default='de'
)
parser.add_argument(
    '-t', '--tgt-lang',
    default='en'
)
parser.add_argument(
    '-l', '--log-level',
    choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'],
    default='INFO'
)
parser.add_argument(
    '-T', '--translator',
    choices=['null', 'opus', 'api_opus', 'api_deepl', 'api_openai'],
    default='opus'
)
parser.add_argument(
    '-A', '--aligner',
    help=("'auto' selects translator's built-in aligner for if supported\n"
          "translators with alignment support: null, opus"),
    choices=['auto', 'awesome'],
    default='auto'
)
parser.add_argument(
    '-M', '--opus-model-base',
    help=('use specified model (local or on HF) instead of Helsinki-NLP/opus-mt-{src}-{tgt}\n'
          '{src} and {tgt} may be used as placeholders for source and target language'),
    required=False
)
parser.add_argument(
    '-P', '--opus-input-prefix',
    help=('A prefix to add to the translation input (for multilingual models)\n'
          'e.g. `>>ita<<`'),
    required=False
)
parser.add_argument(
    '-g', '--glossary-file',
    help='path to file containing glossary in SOURCE,TARGET format',
    required=False
)
parser.add_argument(
    '--glossary-method',
    help='glossary enforcement method',
    choices=['auto', 'align', 'srcrepl'],
    default='auto',
    required=False
)
parser.add_argument(
    '--glossary-fallback',
    help='glossary enforcement method used when translator builtin is not available',
    choices=['align', 'srcrepl'],
    default='align',
    required=False
)
