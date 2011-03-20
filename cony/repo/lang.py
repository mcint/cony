# -*- coding: utf-8 -*-
import datetime
import os.path
import urllib

from bottle import redirect

def cmd_translate(term):
    """Translates the text using Google Translate."""
    if len(term.decode('utf-8')) < len(term):
        direction = 'ru|en'
    else:
        direction = 'en|ru'
    redirect('http://translate.google.com/#%s|%s' % (direction, term))

cmd_tr = cmd_translate


def cmd_save_word(term):
    """Saves word and it's translation into the  ~/.words/YYYY-MM-DD.txt

    These files could be used to import words into the FlashCards ToGo.
    """
    if ';' not in term:
        return cmd_search_word(term)

    filename = datetime.datetime.now().strftime('~/.words/%Y-%m-%d.txt')

    template = """
    <p>Translation "{{ word }}" was saved to %s</p>
    %%rebase layout title='Translation saved'
    """ % filename

    filename = os.path.expanduser(filename)
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    with open(filename, 'a+') as f:
        f.write(term)
        f.write('\n')
    return dict(template=template, word=term)


def cmd_search_word(term):
    """Searches word translations at the http://slovari.yandex.ru.

    This command requires `simplejson` module to be installed.
    """
    import simplejson

    template = """
    <ul>
        %for v in variants:
            <li><a href="/?s=save_word+{{ v['en'].replace(' ', '+') }}%3B+{{ v['ru'].replace(' ', '+').replace(',', '%2C') }}">{{ v['en'] }}</a> — {{ v['ru'] }}</li>
        %end
    </ul>
    %rebase layout title='Word translation'
    """

    variants = {}

    for i in reversed(range((len(term) + 1) / 2, len(term) + 1)):
        url = 'http://suggest-slovari.yandex.ru/suggest-lingvo?v=2&lang=en&part=%s' % term[:i]
        data = urllib.urlopen(url).read()
        data = simplejson.loads(data)
        if data[0]:
            for trans, link in zip(*data[1:]):
                en, ru = trans.split(' - ', 1)
                variants[en] = dict(en=en, ru=ru, link=link)
            if len(variants) > 5:
                break

    return dict(template=template, variants=sorted(variants.values()))

cmd_wo = cmd_search_word
