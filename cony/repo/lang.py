# -*- coding: utf-8 -*-
import datetime
import os.path
import urllib
from requests.sessions import Session

from bottle import redirect
from cony.utils import force_str
from xml.etree import ElementTree as ET

xhtml = '{http://www.w3.org/1999/xhtml}'


def cmd_translate(term):
    """Translates the text using Google Translate."""
    if len(term) < len(term.encode('utf-8')):
        direction = 'ru|en'
    else:
        direction = 'en|ru'
    redirect('http://translate.google.com/#%s|%s' % (direction, term.encode('utf-8')))

cmd_tr = cmd_translate


def cmd_save_word(term):
    """Saves word and it's translation into the  ~/.words.csv

    These files could be used to import words into the FlashCards ToGo.
    """
    if ';' not in term:
        return cmd_search_word(term)

    filename = '~/.words.csv'

    template = """
    <p>Translation "{{ word }}" was saved to %s</p>
    %%rebase layout title='Translation saved'
    """ % filename

    filename = os.path.expanduser(filename)
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    with open(filename, 'a+') as f:
        f.write(term.encode('utf-8'))
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
            <li><a href="/?s=save_word+{{ v['en'].replace(' ', '+') }}%3B+{{ v['ru'].replace(' ', '+').replace(',', '%2C') }}">{{ v['en'] }}</a>
            %if v['transcript']:
                ({{ v['transcript'] }})
            %end
            %if v['has_audio']:
                <object
                    type="application/x-shockwave-flash"
                    data="http://audio.lingvo.yandex.net/swf/lingvo/lingvo-player.swf"
                    width="27"
                    height="27"
                    style="visibility: visible;">
                        <param name="allowscriptaccess" value="always">
                        <param name="wmode" value="transparent">
                        <param name="flashvars" value="color=0xFFFFFF&amp;size=27&amp;counter-path=slovari&amp;count=yes&amp;service-url=http://audio.lingvo.yandex.net&amp;download-url-prefix=sounds&amp;timestamp-url-prefix=timestamp.xml&amp;language=SoundEn&amp;sound-file={{ v['en'] }}.mp3">
                    </object>
            %end
            — {{ v['ru'] }}</li>
        %end
    </ul>
    %rebase layout title='Word translation'
    """

    variants = {}

    internet = Session()

    for i in reversed(range((len(term) + 1) / 2, len(term) + 1)):
        url = 'http://suggest-slovari.yandex.ru/suggest-lingvo?v=2&lang=en&' + \
                urllib.urlencode(dict(part=term[:i].encode('utf-8')))
        response = internet.get(url)
        data = simplejson.loads(response.content)

        if data[0]:
            for trans, link in zip(*data[1:]):
                en, ru = trans.split(' - ', 1)
                variants[en] = dict(en=en, ru=ru, link=link)
            if len(variants) > 5:
                break


    def get_spelling(value):
        url = 'http://lingvo.yandex.ru/' + force_str(value['en']).replace(' ', '%20') + '/%D1%81%20%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B3%D0%BE/'
        data = internet.get(url).content

        xml = ET.fromstring(force_str(data))
        transcript = xml.find('*//{x}span[@class="b-translate__tr"]'.format(x=xhtml))

        if transcript is None:
            value['transcript'] = ''
        else:
            value['transcript'] = transcript.text

        has_audio = xml.find('*//{x}h1[@class="b-translate__word"]//{x}span[@class="b-audio g-js"]'.format(x=xhtml))
        value['has_audio'] = has_audio is not None
        return value

    variants = dict((key, get_spelling(value)) for key, value in variants.iteritems())

    return dict(template=template, variants=sorted(variants.values()))

cmd_wo = cmd_search_word
