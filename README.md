glasshouse
==========

A way to control an Indigo / Insteon smart home

Indigo is a great piece of OS X software that can control and manage an Insteon smart home.


Architecture:
    Glass Tier:
    Whatever Google Glass ends up allowing us to do for an API.  I want to be
    able to take a command such as "OK Glass, are the garage doors shut?" and
    have it make a call to a REST api.

    House Tier:
    This would be the indigo plugin which is just a flask dev server running
    on an indigo plugin process. To start we could just hit this directly,
    I guess it would be easy to DDOS or something, but lets worry about that
    later.  I may run nginx in front of it on 443, and just map to the dev port.

    Since this is glass based, I am making the assumption that google oauth2
    is the way to go for auth on this.



Setup:

    pip install flask




Tools:
    To test endpoints in chrome:
        http://www.restconsole.com/
