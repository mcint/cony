Shared Smart Bookmarks Server
=============================

"Cony" is a tool to write [smart bookmarks][smart-bm] in the python and
to share them across all your browsers and with other developers
on GitHub. This project is inspired by Facebook's [bunny1][].

What the difference between Cony and Bunny1?
--------------------------------------------

* Cony has no dependencies other than Bottle, which itself is a
  micro web framework without dependencies.
* Cony could be easily extended. You have no need to inherit any classes like
  you do with Bunny1. With Cony, you place your commands in a separate
  file and fire `./cony.py`.

Introduction
------------

Smart bookmarks are a fast way to retrive information from the web.
For example, you could type `w smart bookmarks` in the browser's
location bar and it will open the Wikipedia article about
[smart bookmarks][smart-bm].

If you use more than one browser or device, then you are in trouble,
because you have to sync the smart bookmarks of the various browsers.

Cony not only solves this problem, creating one place were you store your
smart bookmarks, but also, it makes your bookmarks **much** **much**
**smarter**.

For example, you could create this bookmark which will choose the
text translation mode depending on language:

    def cmd_tr(term):
        """Translates the text using Google Translate."""
        if len(term.decode('utf-8')) < len(term):
            direction = 'ru|en'
        else:
            direction = 'en|ru'
        redirect('http://translate.google.com/#%s|%s' % (direction, term))

This bookmark converts from English to Russian if it contains only ASCII
characters.  Otherwise it translates in other direction.

There are many other applications of this small webserver.


Installation
------------

Ways to install Cony:

* Just clone the repository and to run `./cony.py`.
* `easy_install cony; cony.py`
* `pip install cony; cony.py`

Now you have server up and running. It binds to the localhost:8080 by
default. Open the <http://localhost:8080> in your browser to see the help.

You can configure Cony by editing the top of "cony.py" and looking for the
"SERVER_*" entries.  These can be adjusted to change the port, change what
interface is bound to (use '' to bind to all interfaces).

You can also configure CGI or WSGI modes if you want to integrate this into
an existing web server such as Apache.

### Apache CGI

Create "local_settings.py" which contains:

    SERVER_MODE = 'CGI'

In your Apache configuration, add:

    ScriptAlias /cony/ /path/to/cony.py

Re-start Apache and you should now be able to use
"http://servername/cony/?s=%s" as the Cony URL in your browser
configuration.

### Apache WSGI

Create "local_settings.py" which contains:

    SERVER_MODE = 'WSGI'

Install mod_wsgi ("apt-get install libapache2-mod-wsgi" or "yum install
mod_wsgi").

In your Apache configuration, add:

    WSGIPythonPath /path/to/cony/directory
    WSGIScriptAlias /cony/ /path/to/cony/directory/cony.py

Re-start Apache and you should now be able to use
"http://servername/cony/?s=%s" as the Cony URL in your browser
configuration.

Browser Configuration
---------------------

### Firefox

* Type `about:config` into your location bar in Firefox.
* Set the value of `keyword.URL` to be `http://localhost/?s=`
* Now, type `pypi cony` into your location bar and press ENTER.

### Google Chromium

* Click the "Wrench" to the right of the URL bar.
* Click "Preferences".
* Click "Search:", click on "Manage Search Engines".
* Click "Add".
   * Name: Cony
   * Keyword: c
   * URL: http://localhost:8080/?s=%s
   * OK.
* Select the "Cony" line.
* Click "Make Default" in the upper right.
* Close the window.
* Type "pypi cony" in the URL bar and press ENTER.


### Google Chrome

* Choose `Options` from the wrench menu to the right of the
location bar in Chrome.
* Under the section `Default Search`.
* Click the `Manage` button.
* Click the `Add` button and then fill in the fields:
   * Name: Cony
   * Keyword: c
   * URL: http://localhost:8080/?s=%s
   * OK.
* Select the "Cony" line.
* Click "Make Default" in the upper right.
* Close the window.
* Type "pypi cony" in the URL bar and press ENTER.

### Safari

For Safari you could try to install [Keywurl][] plugin. And add a `Cony`
as default search.

Creating Custom Commands
------------------------

Cony defines some default commands ("g", "p", and "pypi", as well as a
general "help" command).  However, you can also create your own commands
by placing them in a `local_settings.py`.

If you define a `cmd_fallback` function (which is probably just set to
another function, like `cmd_fallback = cmd_g`), then this will be used if
no other command is matched. If you do not define a "cmd_fallback", then
the default "cmd_g" is used, doing a Google search. Similarly, if no
`cmd_help` is defined, a default one will be used which shows the
[docstrings][] of the commands.

Cony's default commands can be overridden or turned off. To turn a command
off, just assign it none in your `local_settings.py`: `cmd_g = None`.

Also, commands can be aliased: `cmd_tl = cmd_too_long`.

For example, here is a simple `local_settings.py` config that uses the
default "g", and "p", but not "pypi" commands, uses the default fallback
and help commands (as described above), and creates a "weather" command
with an alias "w":

    from bottle import redirect

    #  local templates
    TEMPLATES = dict(
       weather = """
          <p />Display the weather in the specified location.  For example,
          you could enter the following locations:
          <dl class="help">
          %for example in examples:
          <dt><a href="/?s=weather {{ example }}">{{ example }}</a></dt>
          %end
          </dl>
          %rebase layout title = 'Weather Help'
          """,
       )

    def cmd_weather(term):
       '''Look up weather forecast in the specified location.'''
       examples = [ 'Moscow, Russia', 'Fort Collins, Colorado' ]
       if term and term != 'help':
          redirect('http://weather.yahoo.com/search/weather?location=%s' % term)
       else:
          #  render the "weather" template defined above, pass "examples"
          return dict(examples = examples)

    cmd_w = cmd_weather
    cmd_pypi = None


Contributors
------------

* Alexander Artemenko (author)
* Sean Reifschneider

[smart-bm]: http://en.wikipedia.org/wiki/Smart_bookmark
[bunny1]: https://github.com/facebook/bunny1
[Keywurl]: http://alexstaubo.github.com/keywurl/
[docstrings]: http://en.wikipedia.org/wiki/Docstring#Python
