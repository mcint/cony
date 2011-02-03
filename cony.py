#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import bottle

from bottle import SimpleTemplate, template
from bottle import route, run, request, redirect
from itertools import groupby

################
#  CONFIGURATION
#
#  These values can be overridden in a "local_settings.py" file so that
#  your local changes don't require merging into new versions of cony.
################

DEBUG = True
#  Stand-alone server running as a daemon on port 8080
SERVER_MODE = 'STANDALONE' # or 'WSGI', or 'CGI'
SERVER_PORT = 8080
SERVER_HOST = 'localhost'  # or '' to allow on all interfaces


##################
# Default commands
##################

def cmd_g(term):
    """Google search."""
    redirect('http://www.google.com/search?q=%s' % term)

cmd_fallback = cmd_g


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


def cmd_p(term):
    """Python documentation search."""
    redirect('http://docs.python.org/search.html?q=%s&check_keywords=yes&area=default' % term)


def cmd_help(term):
    """Shows all available commands."""
    items = []

    # functions should be sorted by value
    # because we will group them lately
    functions = sorted(globals().items(), key=lambda x: x[1])

    commands = (
        (cmd, name)
        for name, cmd in functions
        if name != 'cmd_fallback' and name.startswith('cmd_') and callable(cmd)
    )

    commands = groupby(commands, lambda x: x[0])

    # "list" of (func, (cmd_example, cmd_exmpl, cmd_ex, ...)) tuples
    # names are sorted by length
    commands = (
        (cmd, sorted(map(lambda x: x[1][4:], values), key=lambda x: len(x), reverse=True))
        for cmd, values in commands
    )

    # and finally, sort by name
    commands = sorted(commands, key=lambda x: x[1])

    for cmd, names in commands:
        title = ', '.join(names)
        if cmd is cmd_fallback:
            title += ' (default)'
        items.append({ 'name' : names[0], 'title' : title, 'doc' : cmd.__doc__ })

    return dict(items = items, title = u'Help — Cony')

########################
# Templates related part
########################

_TEMPLATES = dict( # {{{
    layout = """
<!DOCTYPE html>
<html>
    <head>
        <title>{{ title or u'Cony — Smart bookmarks' }}</title>
        <style>
        .container {
            margin: 2em 200px 2em 200px; background: #EEE;
            padding: 1em 1em 0.5em 1em;
        }
        .container header {
            border-bottom: 1px solid #BBB;
            margin-bottom: 2em;
        }
        .container dl.help dd {
            margin-bottom: 1em;
        }
        .container dl.help dt {
            font-weight: bold;
        }
        .container footer {
            border-top: 1px solid #BBB;
            text-align: center;
        }
        .container footer p {
            font-size: 0.75em;
            margin-top: 0.5em;
            margin-bottom: 0.2em;
        }
        </style>
    </head>
    <body>
        <div class="container">
            <header><h1>{{ title }}</h1></header>
            %include
            <footer>
                <p class="copyright">Opensource. By <a href="mailto:svetlyak.40wt@gmail.com">Alexander Artemenko</a>. <a href="http://github.com/svetlyak40wt/cony/">Fork it</a> at the GitHub.</p>
                <p class="thanks">Idea was stolen from Facebook's <a href="https://github.com/facebook/bunny1/">bunny1</a>, many thanks to them.</p>
            </footer>
        </div>
    </body>
</html>
""",
    help = """
    <dl class="help">
    %for item in items:
        <dt><a href="?s={{ item['name'] }}">{{ item['title'] }}</a></dt>
        <dd>{{ item['doc'] }}</dt>
    %end
    </dl>
%rebase layout title='Help — Cony'
"""
) # }}}


class VerySimpleTemplate(SimpleTemplate):
    """ A wrapper around Bottle templates, allows to
        define templates right in the same file keeping
        ability to use inheritance.
    """
    def __init__(self, source=None, name=None, **kwargs):
        if source is None and name is not None:
            source = _TEMPLATES[name]
        super(VerySimpleTemplate, self).__init__(
            source=source, name=name, **kwargs
        )


try:
    from local_settings import *
    if 'TEMPLATES' in locals():
        _TEMPLATES.update(TEMPLATES)
except ImportError:
    pass


@route('/')
def do_command():
    """Runs a command"""
    search_string = request.GET.get('s', 'help')

    tokens = search_string.split(' ', 1)
    command_name = tokens[0]
    term = len(tokens) == 2 and tokens[1] or ''

    command = globals().get('cmd_' + command_name, cmd_fallback)

    if command is cmd_fallback:
        term = search_string

    result = command(term)
    if isinstance(result, dict):
        # Command could return a dict
        # in that case, we have to render it first

        # here we have to take original function's name
        # to work with aliases
        original_cmd_name = command.__name__[4:]
        name = result.pop('template', original_cmd_name)
        kwargs = dict(
            title = None,
        )
        kwargs.update(result)
        return template(name, template_adapter=VerySimpleTemplate, **kwargs)
    else:
        return result


bottle.debug(DEBUG)

if SERVER_MODE == 'WSGI':
    application = bottle.app()

elif __name__ == '__main__':
    if SERVER_MODE == 'STANDALONE':
        run(
            reloader=DEBUG,
            host=SERVER_HOST,
            port=SERVER_PORT,
        )
    elif SERVER_MODE == 'CGI':
        run(server=bottle.CGIServer)
    else:
        print 'Wrong SERVER_MODE=%r defined for running from command-line' % (SERVER_MODE,)
        sys.exit(1)
    sys.exit(0)
