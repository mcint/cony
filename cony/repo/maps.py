# -*- coding: utf-8 -*-
from bottle import redirect


def cmd_yandex_maps(term):
    """Yandex Maps Search."""
    redirect('http://maps.yandex.ru/?text=%s' % term)

