# Copyright 2009-2010 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from signal import SIGTERM

class Daemon(object):
    """Daemonize Module. Accepts start stop and spawn"""

    def __init__(self, name='PythonDaemon',
                 pid_dir='/var/run',
                 log=True,
                 stdin='/var/log',
                 stdout='/var/log',
                 stderr='/var/log',
                 ):
        self.name = name
        self.log = log
        self.pid_dir = pid_dir
        self.pid = "%s/%s.pid" % (self.pid_dir, self.name)
        self.stdin = "%s/%s" % (stdin, self.name)
        self.stdout = "%s/%s" % (stdout, self.name)
        self.stderr = "%s/%s" % (stderr, self.name)

    def start(self, check_pid=True, verbose=True):
        """
        Double forks the process in the background
        to avoid zombies, writes a PID and opens a log file if needed.
        """
        self.check_pid = check_pid
        self.verbose = verbose
        
        if self.check_pid:
            if os.path.isfile(self.pid):
                print "\n%s already running\n " % self.name 
                sys.exit(1)
            
        sys.stdout.flush()
        sys.stderr.flush()
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, exc:
            sys.exit("%s: fork #1 failed: (%d) %s\n" % (sys.argv[0],
            exc.errno, exc.strerror))

        os.chdir("/")
        os.umask(0)
        os.setsid()

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, exc:
            sys.exit("%s: fork #2 failed: (%d) %s\n" % (sys.argv[0],
            exc.errno, exc.strerror))
        
        if self.check_pid:
            try:
                pid_file =  open(self.pid, "w")
                pid = str(os.getpid())
                pid_file.write(pid+"\n")
                pid_file.close
            except IOError, e:
                if e.errno == 13:
                    error = "You do not have permission to create the PID file:\
\n%s\n" % self.pid
                    sys.stderr.write(error)
                    sys.exit(1)
                else:
                    error_message = """The Daemon module had an IO error:
%s \n""" % e
                    sys.stderr.write(error_message)
                    sys.exit(1)
        
        if self.verbose:
            print "\nStarting the %s daemon." % self.name
            print "With PID:\t %s\n" % pid
        
        if self.log:
            if not os.path.isfile(self.stdin):
                log = open(self.stdin, 'w')
                log.close()
            si = open(self.stdin, 'r')
            so = open(self.stdout, 'a+')
            se = open(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())
            

    def stop(self, verbose=True):
        """
        Stops the running process with the
        corresponding pid.
        """
        self.verbose = verbose
        try:
            pidfile = open(self.pid, "r")
            pid = pidfile.readline()
            if self.verbose:
                print "\nStopping the %s daemon." % self.name
                print "With pid number %s" % pid
            os.kill(int(pid), SIGTERM)
            os.remove(self.pid)

        except OSError, e:
            if self.verbose:
                print "Could not kill %s process.\n" % self.name
                print e
            if e.errno == 13: # catch a 'no such process'
                os.remove(self.pid)
                if self.verbose:
                    print "Removed defunct PID file. Try starting the daemon now."
            
        except IOError:
            if self.verbose:
                print "\nPID file not found. Process may not be running.\n"
            
    def spawn_child(self):
        """Overlooks the PID information lock to spawn child processes.
        Warning! Since we are no longer checking the PID, we can't stop
        the process once it has started. Make sure spawned processes timeout!
        """
        self.start(check_pid=False, verbose=False)
        
    def status(self):
        """Check the status of the process (running | not running)"""
        try:
            pidfile = open(self.pid)
            pid = pidfile.readline()
            os.kill(int(pid), 0)
        
        except OSError:
            message = "\n%s process is not running.\n" % self.name
            sys.stdout.write(message)
            
        except IOError:
            message = "\nPID file not found. Process may not be running.\n"
            sys.stderr.write(message)
        else:
            message = "\n%s process is running with PID: %s\n" % (self.name, pid)
            sys.stdout.write(message)
        
            
