#!/usr/bin/env python

from bottle import redirect
from cony import rich_help
import urllib2


@rich_help('--help')
def cmd_areacode(term):
	'''Look up an areacode in Wikipedia.'''

	template = """
		<p />Look up an areacode in Wikipedia.
		If the term is:

		<ul>
			<li /><b>No arguments</b> -- Take you to a page on Wikipedia
					listing US areacodes.
			<li /><b>Areacode</b> -- Go directly to that
					areacode's page on Wikipedia.
		</ul>

		%rebase layout title = 'Areacode Help'
		"""

	if term == '--help' or term == '?' or term == '-?':
		return dict(template = template)
	elif not term:
		redirect('http://en.wikipedia.org/wiki/List_of_NANP_area_codes')
	else:
		url = 'http://en.wikipedia.org/wiki/Area_code_720%s' % term
		redirect(url)
