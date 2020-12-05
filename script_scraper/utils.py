import re

import nltk
from nltk.tokenize import sent_tokenize
import pdftotext


def open_pdf(path):
    """
    Open a PDF file for analysis.

    Parameters
    ---------------
    path: Path or str
        Path to PDF file.

    Returns
    ---------------
    pdf: pdftotext.PDF

    """
    with open(str(path), 'rb') as f:
        return pdftotext.PDF(f)


def word_and_sentence_count(single_characters_dialogue):
    """
    Open a PDF file for analysis.

    Parameters
    ---------------
    single_characters_dialogue: List of dialogue

    Returns
    ---------------
    word_count: int
    sentence_count: int

    """
    nltk.download('punkt')

    # TODO: sentence count needs to be better
    pattern = re.compile('[\W]', re.IGNORECASE | re.UNICODE)

    single_characters_dialogue = ' '.join(single_characters_dialogue)
    words = single_characters_dialogue.split()

    word_list = list()
    for word in words:
        word = pattern.sub('', word).lower()

        if word and not word.isspace():
            word_list.append(word)

    sentence_list = sent_tokenize(single_characters_dialogue)

    return len(word_list), len(sentence_list)


def _prep_potential_name(line):
    return re.sub('\([^\)]+\)', '', line).replace('*', '')


def _check_if_potential_name(potential_name):
    return ('EXT.' not in potential_name
            and 'INT.' not in potential_name
            and 'TO:' not in potential_name
            and 'SFX:' not in potential_name)


def _initial_line_checks(line, currently_speaking):
    we_should_continue = False

    if len(line.strip()) == 0:
        currently_speaking = None
        we_should_continue = True

    return we_should_continue, currently_speaking


def _handle_parentheses(line, open_bracket):
    line = re.sub('\([^\)]+\)', '', line)
    if '(' in line:
        open_bracket = True
    if ')' in line:
        line = line.split(')', 1)[-1]
        open_bracket = False

    return line, open_bracket


def _get_spaces_before_line(line):
    return len(line) - len(line.lstrip(' '))