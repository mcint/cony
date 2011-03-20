# -*- coding: utf-8 -*-
import urllib2
from bottle import redirect
from cony.utils import rich_help


def cmd_google(term):
    """Google search."""
    redirect('http://www.google.com/search?q=%s' % term)


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


@rich_help('--help')
def cmd_python(term):
    '''Python documentation search.'''

    if term == '--help' or term == '?' or term == '-?':
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

