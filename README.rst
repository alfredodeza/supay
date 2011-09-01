Will effectively daemonize a running Python script. Tested and used with Python 2.6

Start, Stop, Restart, check the status and/or spawn child processes of any Python script/module.

Methods
-------
There are a few methods available with the module, here a short description of each one:

* start   Detaches a Python script from the terminal and assigns a PID to the process
* stop    Finds the process with the matching PID and stops it.
* spawn   Will create a new instance of the Python script (Warning: this should time out or you will not be able to stop the process.)
* restart Although there is no 'restart' method, you can easily integrate the stop and restart together so they can perform a full restart of your daemon.
* status  Tells you if your process is still running or not.


Installation
------------
If you have Setup Tools installed (along with Python) in your machine you can do::

    sudo pip nstall supay

If you download the tar.gz file or the source code, use the setup.py file to install it::

    python setup.py install

Usage
=====


Start
-----
To use the "start" method::

    from supay import Daemon

    def run():
        daemon = Daemon(name='thisScript')
        daemon.start()
        while True:
            do_something()

Stop
----
Even easier to use the "stop" method::

    def stop()
        daemon = Daemon(name='thisScript')
        daemon.stop()

A verification method is performed when a daemon has died for some reason but
the PID has been left behind. As you know, the start method will check if the
PID exists so this check will remove the PID if the process does not exist.

We are also including the ability to spawn a process (also known as creating a
child process). Beware! spawning processes should be able to TIME OUT. They are
cut off the ability of stopping with no PID file to write. This is a good way
of dealing with calls to your script that you want to handle separately.

Spawn
-----
To spawn::

    def spawn():
        daemon.spawn_child()
        do_something()  # and then expire!

Status
------
Check the process status::

    def status():
        daemon.status()

Tests
-----
If you download the source code, a tests directory will include all the tests.
I have used Nose to run my tests and I suggest you run them with that tool
within the uncompressed directory::

    py.test -v

Deafults
--------
Supay does some things by default.

Tries to write a PID file to "/var/run/scriptName" Gives an error if you do not
have permissions. You can also change this when initializing the Daemon class.
Stderr, Stdout and Stdin all try to write to "/var/log/scriptName" If a name
for the running script is not given "PythonDaemon" is used.  Verbose is set to
True, this will show output when starting or stopping the daemon at the
terminal.

Note on Permissions
-------------------
If you use this module with sudo or root permissions and the default values,
you should see no errors. But a lot of times, using super user powers to run a
simple script might be a security problem. To avoid running this module as root
change the PID and LOG options when initializing the module::

    from supay import Daemon

    daemon = Daemon(name='myScript', pid_dir='/home/me', stdin='/home/me/logs', stdout='/home/me/logs', stderr='/home/me/logs')

    daemon.start()

Another way to set stdin, stdout and stderr at the same time is to use a helper
parameter called catch_all_log. When used, all the parameters regarding std...?
will be redirected to the path::

    daemon = Daemon(name="myScript", catch_all_log="/var/log"

And to turn off logging::

    daemon = Daemon(log=False)

Daemon or Service?
------------------
A bit of inspiration came from reading PEP-3143. After talking to the author of
that PEP, I was told that what I wanted to develop was not a Daemon library,
but more a Service library. My reasoning behind building something more than a
simple daemon library was this:

A pure Daemon library
---------------------
Would make sure to daemonize correctly a process and nothing else.
What Supay is intended for:

* Daemonize a Python process (a script or a call)
* Accept calls to STOP, START, SPAWN child processes.
* Manage processes PID numbers.
* Check the STATUS of a process.
* Redirect output (stderr, stdin, stdout) to a log file.

As you can see, I am not interested in a simple standard daemonizing module,
and although PEP-3143 was used as a start point, the functionality behind SUPAY
goes way beyond that.

Some history about SUPAY
------------------------
In the ancient language of Quechua (still used today in some regions of South
America, like Peru, Bolivia and Ecuador) Supay was the word to refer to Demons.
Although different in significance, I decided to revive a rather unknown word
to refer to this small module.

Questions? Requests?
--------------------
You can always send me an email: alfredodeza at gmail dot com
