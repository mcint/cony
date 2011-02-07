from bottle import redirect
from cony import rich_help


@rich_help('--help')
def cmd_reader(term):
	'''Go to the Google Reader page.'''

	template = """
		<p />Go to the Google Reader inbox page.

		%rebase layout title = 'Reader Help'
		"""

	if term == '--help' or term == '?' or term == '-?':
		return dict(template = template)
	else:
		redirect('http://www.google.com/reader/view/')
