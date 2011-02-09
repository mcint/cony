#!/usr/bin/env python

from bottle import redirect
from cony import rich_help


@rich_help('--help')
def cmd_wikipedia(term):
	'''Wikipedia page search.'''

	template = """
		<p />Search Wikipedia for the given term.  If no term is specified,
		the home page is opened.  Otherwise, the term is searched for on
		Wikipedia, which may result in a redirect to an exact page match,
		or to a list of search results.
		</p>

		<p>If the term "slash" (/) followed by one of the language-specific
		Wikipedia sub-sites, such as "/en" or "/ru", go directly to that
		page.</p>

		%rebase layout title = 'Wikipedia Help'
		"""

	if term == '--help' or term == '?' or term == '-?':
		return dict(template = template)
	elif not term:
		redirect('http://www.wikipedia.org/')
	elif term[0] == '/' and len(term) == 3:
		redirect('http://%s.wikipedia.org/' % term[1:])
	else:
		redirect('http://www.wikipedia.org/w/index.php?search=%s'
				% term.replace(' ', '+'))
