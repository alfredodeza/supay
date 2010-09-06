import unittest
import os
import sys
from subprocess import Popen, PIPE
from time import sleep

import supay
import test_script
from mock import MockSys

class TestDaemon(unittest.TestCase):
    

    def tearDown(self):
        try:
            os.remove('/tmp/supay_test_pid.pid')
        except Exception:
            pass


    def test_init_defaults(self):
        daemon = supay.Daemon()

        self.assertEqual(daemon.pid_dir, '/var/run')
        self.assertEqual(daemon.name, 'PythonDaemon')
        self.assertTrue(daemon.log)
        self.assertEqual(daemon.stdin, '/var/log/PythonDaemon.log')
        self.assertEqual(daemon.stdout, '/var/log/PythonDaemon.log')
        self.assertEqual(daemon.stderr, '/var/log/PythonDaemon.log')


    def test_init_catch_all_log_dir(self):
        daemon = supay.Daemon(catch_all_log='/tmp')
        
        self.assertEqual(daemon.stdin, '/tmp/PythonDaemon.log')
        self.assertEqual(daemon.stdout, '/tmp/PythonDaemon.log')
        self.assertEqual(daemon.stderr, '/tmp/PythonDaemon.log')


    def test_init_catch_all_log_file(self):
        daemon = supay.Daemon(catch_all_log='/tmp/my_daemon.log')
        
        self.assertEqual(daemon.stdin, '/tmp/my_daemon.log')
        self.assertEqual(daemon.stdout, '/tmp/my_daemon.log')
        self.assertEqual(daemon.stderr, '/tmp/my_daemon.log')


    def test_status_ioerror(self):
        sys.stderr = MockSys()
        daemon = supay.Daemon(name='foo', pid_dir=os.getcwd())
        daemon.status()
        actual = sys.stderr.captured()
        expected = "\nPID file not found. Process may not be running.\n"
        self.assertEqual(actual, expected) 


    def test_status_oserror(self):
        my_pid = open('/tmp/supay_test_pid.pid', 'w')
        my_pid.write('999999')
        my_pid.close()
        sys.stdout = MockSys()
        daemon = supay.Daemon(name='supay_test_pid', pid_dir='/tmp')
        daemon.status()
        actual = sys.stdout.captured()
        expected = "\nsupay_test_pid process is not running.\n"
        self.assertEqual(actual, expected) 

    def test_status_running(self):
        my_pid = open('/tmp/supay_test_pid.pid', 'w')
        my_pid.write('0')
        my_pid.close()
        sys.stdout = MockSys()
        daemon = supay.Daemon(name='supay_test_pid', pid_dir='/tmp')
        daemon.status()
        actual = sys.stdout.captured()
        expected = "\nsupay_test_pid process is running with PID: 0\n"
        self.assertEqual(actual, expected) 


    def test_start(self):
        """See if after starting the daemon, it writes a PID"""
        command = "python %s/test_script.py start" % os.getcwd()
        Popen(command, shell=True, stdout=PIPE)
        pid_file = "%s/testScript.pid" % os.getcwd()
        sleep(2) # need to put a sleep to give time for the process to start
        self.assertTrue(pid_file)
        
    def test_stop(self):
        """Tries to stop the Daemon previously created"""
        command = "python %s/test_script.py stop" % os.getcwd()
        Popen(command, shell=True, stdout=PIPE)
        sleep(2) # Again the sleep here to give some time to stop the process
        pid_file = "%s/testScript.pid" % os.getcwd()
        self.assertFalse(os.path.isfile(pid_file))
        


if __name__ == '__main__':
    unittest.main()
