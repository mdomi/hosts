'''
Copyright (c) 2012 Michael Dominice

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

import re


class Hosts(object):

    def __init__(self, path):
        self.hosts = {}
        self.read(path)

    def get_one(self, host_name):
        return self.hosts[host_name]

    def print_one(self, host_name):
        print host_name, self.get_one(host_name)

    def print_all(self, host_names=None):
        if host_names is None:
            for host_name in self.hosts.keys():
                self.print_one(host_name)
        else:
            for host_name in host_names:
                self.print_one(host_name)

    def read(self, path):
        with open(path, 'r') as hosts_file:
            for line in hosts_file.read().split('\n'):
                if len(re.sub('\s*', '', line)) and not line.startswith('#'):
                    parts = re.split('\s+', line)
                    ip_address = parts[0]
                    for host_name in parts[1:]:
                        self.hosts[host_name] = ip_address

    def write(self, path):
        reversed_hosts = {}
        for host_name in self.hosts.keys():
            ip_address = self.hosts[host_name]
            if ip_address not in reversed_hosts:
                reversed_hosts[ip_address] = [host_name]
            else:
                reversed_hosts[ip_address].append(host_name)
        with open(path, 'w') as hosts_file:
            for ip_address in reversed_hosts.keys():
                hosts_file.write('%s\t%s\n' % (ip_address, '\t'.join(reversed_hosts[ip_address]),))

    def set_one(self, host_name, ip_address):
        self.hosts[host_name] = ip_address

    def set_all(self, host_names, ip_address):
        for host_name in host_names:
            self.set_one(host_name, ip_address)

    def alias_all(self, host_names, target):
        self.set_all(host_names, self.get_one(target))

if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Manipulate your hosts file')

    parser.add_argument('name', nargs='+')
    parser.add_argument('--set', dest='ip_address')
    parser.add_argument('--alias')
    parser.add_argument('--get', action='store_true', default=False)

    args = parser.parse_args()

    if os.name == 'nt':
        hosts_path = os.path.join(os.environ['SYSTEMROOT'], 'system32/drivers/etc/hosts')
    if os.name == 'posix':
        hosts_path = '/etc/hosts'
    else:
        raise Exception('Unsupported OS: %s' % os.name)

    hosts = Hosts(hosts_path)

    if args.get:
        hosts.print_all(args.name)
    elif args.alias is not None:
        hosts.alias_all(args.name, args.alias)
        hosts.write(hosts_path)
    elif hasattr(args, 'ip_address'):
        hosts.set_all(args.name, args.ip_address)
        hosts.write(hosts_path)
