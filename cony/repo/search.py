# -*- coding: utf-8 -*-
import urllib2
from bottle import redirect
from cony.utils import rich_help, HELP_TERMS


def cmd_google(term):
    """Google search."""
    redirect('http://www.google.com/search?q=%s' % term)


def cmd_yandex(term):
    """Yandex search."""
    redirect('http://yandex.ru/yandsearch?text=%s' % term)


def cmd_fl(term):
    """Search among Flickr photos under Creative Commons license."""
    redirect('http://www.flickr.com/search/?q=%s&l=cc&ss=0&ct=0&mt=all&w=all&adv=1' % term)


def cmd_pep(term):
    """Search a Python Enhancement Proposal by it's number. For example: 'pep 8'."""
    redirect('http://www.python.org/dev/peps/pep-%0.4d/' % int(term))


def cmd_dj(term):
    """Django documentation search."""
    redirect(
        'http://docs.djangoproject.com/en/dev/search/?cx=009763561546736975936:e88ek0eurf4&'
        'cof=FORID:11&q=%s&siteurl=docs.djangoproject.com/en/dev/topics/db/models/' % term
    )


def cmd_android(term):
    """Search app in Adroid Market"""
    redirect('https://market.android.com/search?q=%s&c=apps' % term)


def cmd_pypi(term):
    """Python package index search.

    If there is exact match, then redirects right to the package's page.
    """
    import urllib
    try:
        direct_url = 'http://pypi.python.org/pypi/%s/' % term
        result = urllib.urlopen(direct_url)
    except Exception, e:
        pass
    else:
        if result.code == 200:
            redirect(direct_url)

    redirect('http://pypi.python.org/pypi?:action=search&term=%s&submit=search' % term)


@rich_help
def cmd_python(term):
    '''Python documentation search.'''

    if term in HELP_TERMS:
        _template = """
            <p>Search the Python documentation pages for the specified string.
            If the term is:</p>

            <ul>
                <li><b>No arguments</b> — Take you to the main Python
                        documentation library page.</li>
                <li><b>Matches module name</b> — Go directly to that
                        module's documentation page.</li>
                <li><b>Otherwise</b> — Passes the term on to the PyDoc search page.</li>
            </ul>
        %rebase layout title = 'PyDoc Help — Cony'
        """
        return dict(template=_template)
    elif not term:
        redirect('http://docs.python.org/library/index.html')
    else:
        try:
            url = 'http://docs.python.org/dev/library/%s.html' % term
            urllib2.urlopen(url)
            redirect(url)
        except urllib2.HTTPError:
            redirect('http://docs.python.org/search.html?q=%s'
                    '&check_keywords=yes&area=default' % term)


@rich_help
def cmd_wikipedia(term):
    '''Wikipedia page search.'''

    template = """
        <p>Search Wikipedia for the given term.  If no term is specified,
        the home page is opened.  Otherwise, the term is searched for on
        Wikipedia, which may result in a redirect to an exact page match,
        or to a list of search results.
        </p>

        <p>If the term "slash" (/) followed by one of the language-specific
        Wikipedia sub-sites, such as "/en" or "/ru", go directly to that
        page.</p>

        %rebase layout title = 'Wikipedia Help'
        """

    if term in HELP_TERMS:
        return dict(template = template)
    elif not term:
        redirect('http://www.wikipedia.org/')
    elif term[0] == '/' and len(term) == 3:
        redirect('http://%s.wikipedia.org/' % term[1:])
    else:
        redirect('http://www.wikipedia.org/w/index.php?search=%s'
                % term.replace(' ', '+'))

