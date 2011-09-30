from bottle import redirect
from cony import rich_help


@rich_help('--help')
def cmd_voice(term):
	'''Go to the Google Voice page.'''

	template = """
		<p>Go to the Google Voice inbox page.</p>

		%rebase layout title = 'Voice Help'
		"""

	if term == '--help' or term == '?' or term == '-?':
		return dict(template = template)
	else:
		redirect('https://www.google.com/voice#inbox')
