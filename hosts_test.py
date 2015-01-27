import unittest
import os
import tempfile
import re
import socket

from hosts import Hosts, compare_ip


SPLIT_RE = re.compile("[\t ]+")


def has_host_line(hosts_file, host_line):
    needle = SPLIT_RE.split(host_line)
    with open(hosts_file) as f:
        for line in f.readlines():
            if needle == SPLIT_RE.split(line.strip()):
                return True
    return False


class HostManipulationTestCase(unittest.TestCase):
    def setUp(self):
        fh, self.hosts_file = tempfile.mkstemp()
        self.hosts = Hosts(self.hosts_file)

    def tearDown(self):
        os.unlink(self.hosts_file)

    def assertHasHostLine(self, host_line):
        if not has_host_line(self.hosts_file, host_line):
            raise AssertionError("Line not present: {0}".format(host_line))

    def assertDoesNotHaveHostLine(self, host_line):
        if has_host_line(self.hosts_file, host_line):
            raise AssertionError("Line is present: {0}".format(host_line))

    def test_set_one(self):
        self.hosts.set_one("test", "1.2.3.4")
        self.hosts.write(self.hosts_file)

        self.assertHasHostLine("1.2.3.4 test")

    def test_set_all(self):
        self.hosts.set_all(["test", "alias"], "1.2.3.4")
        self.hosts.write(self.hosts_file)

        self.assertHasHostLine("1.2.3.4 test")
        self.assertHasHostLine("1.2.3.4 alias")

    def test_remove_one(self):
        self.hosts.set_one("test",  "1.2.3.4")
        self.hosts.write(self.hosts_file)

        self.hosts = Hosts(self.hosts_file)

        self.hosts.remove_one("test")
        self.hosts.write(self.hosts_file)

        self.assertDoesNotHaveHostLine("1.2.3.4 test")

    def test_remove_no_raise(self):
        self.assertRaises(KeyError, self.hosts.remove_one, "test")
        self.hosts.remove_one("test", False)

    def test_purge_empty_records(self):
        with open(self.hosts_file, 'a') as f:
            f.write('1.2.3.4')

        self.assertHasHostLine('1.2.3.4')

        hosts = Hosts(self.hosts_file)
        hosts.set_one("test",  "1.2.3.4")
        hosts.set_one("",  "1.2.3.4")
        hosts.write(self.hosts_file)

        self.assertDoesNotHaveHostLine('1.2.3.4')


class IPComparisonTestCase(unittest.TestCase):
    def test_compare_ipv4(self):
        self.assertEqual(0, compare_ip("1.1.1.1", "01.001.1.1"))
        self.assertNotEqual(0, compare_ip("1.1.1.1", "1.2.3.4"))

    def test_compare_ipv6(self):
        self.assertEqual(0, compare_ip("::1", "0::1"))
        self.assertNotEqual(0, compare_ip("::1", "::f"))


class FallbackIPComparisonTestCase(unittest.TestCase):
    def setUp(self):
        self.inet_pton = socket.inet_pton
        del socket.inet_pton

    def tearDown(self):
        socket.inet_pton = self.inet_pton

    def test_parse_ipv4(self):
        self.assertEqual(0, compare_ip("1.1.1.1", "01.001.1.1"))

    def test_parse_ipv6(self):
        # Not supported as of now. We're just verifying that
        # we use the fallback
        self.assertRaises(ValueError, compare_ip, "::1", "::1")


if __name__ == "__main__":
    unittest.main()
