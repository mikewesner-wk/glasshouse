Glass House
==========

A way to control an Indigo / Insteon smart home from Google Glass

Indigo is a great piece of OS X software that can control and manage an Insteon smart home.

Requirements:

    Anyone wanting to use this will require the following:

    1. An Insteon setup, controlling it with Indigo.
    2. A static IP/DNS or dyndns on your home network and port forwarding
        to port 5000 and the machine running indigo.

    3. Install the GlassHouse Indigo plugin. (and enable it)

    4. A google account to login and authorize glasshouse to talk to your glass.

Architecture:

    Glass Tier:
    The Google Glass Mirror API.  Glasshouse will create and subscribe to
    a few cards that show house status information such as:  Motion, Doors open
    or closed, recent activity log, home variables like weather, water sensors,
    etc.

    Glassware Tier:
    I will create an appengine app that you can go to and authorize it to access
    your google glass via the Mirror API.  It will ask you for information like:
    house name, house ip/dns.   It will then retrieve a list of devices, actions
    and variables. Then a screen to allow you to choose your notification
    preferences for those things.  You may be able to configure cards and choose
    how you want information to apear on glass.

    House Tier:
    This would be the indigo plugin.  The Glassware app will make calls to
    this to retrieve information and set device, variable, and action preferences
    so that you can specify on the web app (glassware) what you want to see in
    glass.




Install Instructions for Indigo User:

    1. install indigo plugin in indigo 5+
    2. go to xglasshouse.appspot.com and signup
        a. it will ask for the dns to your indigo install
        b. it will ask you to authorize it to use mirror api and user info

Install Instructions for setting up your own appspot.

    1. create an appid
    2. create a project under the google api console at https://code.google.com/apis/console
        a. under "API Access", create a Client ID for web applications
    3.

Install Instructions for local dev environtment:
    To configure virtualenvwrapper to run at start up update your profile (.bashrc,
    bash_profile, .profile, .zshrc, etc)
    ```
    open ~/.profile

    # virtualenvwrapper

    # Sets the working directory for all virtualenvs
    export WORKON_HOME=$HOME/dev/

    # Sources the virtualenvwrapper so all the commands are availabe in the shell
    source /usr/local/bin/virtualenvwrapper.sh
    ```

    * Create a virtual environment for this

    ```
    $ [sudo] pip install virtualenv
    $ [sudo] pip install virtualenvwrapper
    $ source /usr/local/bin/virtualenvwrapper.sh
    $ cd /where/you/have/glasshouse
    $ mkvirtualenv glasshouse -a $PWD
    $ workon glasshouse
    $ cdvirtualenv
    $ echo $(python -c "from distutils.sysconfig import get_python_lib; print('export PYTHONPATH=' + get_python_lib())") >> bin/activate
    $ pip install -Ur requirements_dev.txt
    $ pip install -Ur requirements.txt
    ```

    To deploy to appengine:
        appcfg.py update appengine

    To iterate on the plugin:
        ./build_plugin.sh
        reload plugin in indigo






Dependencies Notes:
uritemplate
    used by: apiclient oauth2client
    https://pypi.python.org/pypi/uritemplate

_pytest and py are related


