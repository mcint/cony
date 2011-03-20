from bottle import redirect
from cony.utils import rich_help, HELP_TERMS

@rich_help
def cmd_reader(term):
    '''Go to the Google Reader page.'''

    template = """
        <p>Go to the Google Reader inbox page.</p>

        %rebase layout title = 'Reader Help'
        """
    if term in HELP_TERMS:
        return dict(template = template)
    else:
        redirect('http://www.google.com/reader/view/')


@rich_help
def cmd_voice(term):
    '''Go to the Google Voice page.'''

    template = """
        <p>Go to the Google Voice inbox page.</p>

        %rebase layout title = 'Voice Help'
        """

    if term in HELP_TERMS:
        return dict(template = template)
    else:
        redirect('https://www.google.com/voice#inbox')
