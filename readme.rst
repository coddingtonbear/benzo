Benzo
=====

Hand-craft your artisanal REST requests more easily.

Do you find yourself hand-crafting REST requests by opening up a python,
ruby, or javascript repl, or hand-building a curl request?  Do you find
the process of remembering each service's required headers, request format
and authentication rules terribly tedious?  This library is for you.

Benzo makes the process of building and iterating on common request types
easy by providing a few features:

* Templatized requests: Both generic (json, yaml, or form-encoded) and
  service-specific templatized requests make it really easy for you to
  define the content you'd like to send.
* Simple and intuitive creating of requests.  Your request's contents
  and properties (like URL, request method, and headers) are displayed
  in your default editor, and you can add, alter, or remove parameters
  as you wish.
* Separation of the API payload from the editor format. Although the API
  you're interacting with might demand form-encoded, JSON, or yaml values,
  you can edit your request using a variety of formats, and Benzo will
  convert it to the proper format when dispatching your request.
* Saveable sessions.  Do you ever build a request perfectly the first
  time?  Me neither.  Iterate quickly and easily on your request by
  using Benzo's sessions.  If first you do not succeed, just re-run
  Benzo in the same session, and the editor will be opened just as you
  last left it.

Installation
------------

Install using ``pip``:

::

   pip install benzo

Usage
-----

You can just run ``benzo``, but the real power comes when using either
sessions or one of the built-in templates.

Sessions
~~~~~~~~

You can save a session for your request by using the
``--session=<path to file>`` command-line argument.  When using a session,
future requests using the same session file will continue with not only
the same actual session (including any cookies the server you connected
to previously sent down), but the editor when opened will show you exactly
the request you made previously.  This makes it very easy to iterate on
a particularly tricky request.

Templates
~~~~~~~~~

You can use a request template by using the ``--template=<template name>``
command-line argument.  Available templates include:

* ``yaml``, ``json``, and ``form``: These are just generic REST request
  templates that will build an API payload in the Yaml, JSON, or
  form-encoded formats, respectively.
* ``urbanairship.push``: This will provide you with a blank template you
  can use for dispatching a Push using Urban Airship's API.

  * This template also allows for a few configuration settings in your
    ``~/.benzo`` file's ``[urbanairship]`` section:

    * ``app_key``: The Urban Airship App Key to use by default for requests.
    * ``master_secret``: The Urban Airship Master Secret to use by default
      for requests.

* ``twilio.sms``: This will provide you with a blank template you can use
  for dispatching an SMS notification via Twilio's API.

  * This template allows for a few configuration settings in your
    ``~/.benzo`` file's ``[twilio]`` seciton:

    * ``account_sid``: The Twilio Account SID to use by default for requests.
    * ``auth_token``: The Twilio Auth Token to use by default for requests.

Editing your Request
~~~~~~~~~~~~~~~~~~~~

Parameters
++++++++++

Request templates will generally contain a variety of parameters displayed
at the top of your editor as comments.  Parameters usually will include
things like ``Method`` and ``URL``, but individual templates may provide
additional parameters.  These parameters can be edited to alter your
request's behavior before being dispatched.

Headers
+++++++

Request templates will usually contain a list of extra headers displayed
near the top of your editor as comments starting with the proword
``[Header]``.  You can alter or add additional headers at-will; just make
sure to keep the proword ``[Header]`` at the beginning of the line so
Benzo knows which lines to interpret as headers.

Cancelling
++++++++++

If you would like to abort making a request once your editor is opened,
just delete all content from the file, save, and quit.

Configuration
-------------

You do not need to provide any special configuration details, but you can
fine-tune the behavior of Benzo by adding configuration settings to your
``~/.benzo`` file's ``[benzo]`` section.

* ``default_editor_format``: Which format would you like to use for building
  your API requests?  I personally recommend setting this to ``yaml`` for
  more humane editing of API requests.  Default: ``json``.  
* ``default_template``: If you do not specify a template to use, which template
  should be used for generating your request?  Default: ``json``.

Note that individual templates may define extra configuration settings;
see `Templates` for more information.
