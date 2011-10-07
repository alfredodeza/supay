from unittest import TestCase
import os
import sys
from subprocess import Popen, PIPE
from time import sleep
from mock import Mock, patch
from cStringIO import StringIO

import supay

class TestDaemonLogging(TestCase):


    def test_catch_all_log_takes_precedence(self):
        daemon = supay.Daemon(catch_all_log='/tmp/my_deamon.log')
        result = daemon.log_path('/tmp')

        assert result == '/tmp/my_deamon.log'


    def test_catch_all_log_should_never_be_a_dir(self):
        daemon = supay.Daemon(catch_all_log='/tmp')
        result = daemon.log_path('/tmp')

        assert result == '/tmp/PythonDaemon.log'


    def test_log_path_convert_dir(self):
        daemon = supay.Daemon()
        result = daemon.log_path('/tmp/foo.log')

        assert result == '/tmp/foo.log'


    def test_log_path_never_is_a_dir(self):
        daemon = supay.Daemon()
        result = daemon.log_path('/tmp')

        assert result == '/tmp/PythonDaemon.log'


    def test_from_dir_file(self):
        daemon = supay.Daemon()
        result = daemon.dir_to_file('/tmp')

        assert result == '/tmp/PythonDaemon.log'

    def test_from_dir_file_if_it_is_file(self):
        daemon = supay.Daemon()
        result = daemon.dir_to_file('/tmp/foo.log')

        assert result == '/tmp/foo.log'


class TestFork(TestCase):

    def setUp(self):
        self.daemon = supay.Daemon()

    def test_pid_is_greater_than_zero(self):
        m_fork = Mock()
        self.assertRaises(SystemExit, self.daemon.fork, m_fork)


    def test_fork_raises_OSError(self):
        daemon = supay.Daemon(err_writer=StringIO())
        m_fork = Mock(side_effect=OSError)
        with patch('supay.sys.exit'):
            daemon.fork(m_fork)

        assert 'fork failed' in daemon.err_writer.getvalue()

        


class TestErrMessage(TestCase):

    def test_should_output_message_to_stderr(self):
        daemon = supay.Daemon(err_writer=StringIO())
        with patch('supay.sys.exit'):
            daemon.err_msg('foo')

        assert daemon.err_writer.getvalue() == 'foo'

    def test_should_raise_systemExit(self):
        daemon = supay.Daemon(err_writer=StringIO())
        self.assertRaises(SystemExit, daemon.err_msg, 'foo')
        

class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = []

    def write(self, string):
        self.message.append(string)
        pass
                                                                                                                                                                                                         
    def captured(self):
        return ''.join(self.message)


class TestDaemon(TestCase):
    

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
