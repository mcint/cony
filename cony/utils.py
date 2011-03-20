from cony import HELP_TERMS

def rich_help(help_argument = ''):
    """Decorator for command functions to mark them as providing help.

    It causes the default cmd_help to link to them. The optional
    `help_argument`, if set, is the argument passed to the linked command
    for help.

    Usage:

        @rich_help('help')
        def cmd_some_command(term):
            \"\"\"Short help\"\"\"
            ...

    or

        @rich_help
        def cmd_some_command(term):
            \"\"\"Short help\"\"\"
            ...
    """
    if callable(help_argument): # it means decorator was applied without args
        func = help_argument
        func.rich_help = HELP_TERMS[0]
        return func
    else:
        def decorator(handler):
            handler.rich_help = help_argument
            return handler
        return decorator


