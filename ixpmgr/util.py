import configparser
from collections import namedtuple
import os
import re

from ixpmgr import settings
from ixpmgr.models import Customer
from ixpmgr.models import PhysicalInterface
from ixpmgr.models import VirtualInterface
from ixpmgr.models import VlanInterface


def load_config():
    """
    load the IXP-Manager ini config into a dict and return it
    """
    home = settings.HOME
    cfg_file = os.path.join(home, 'application', 'configs', 'application.ini')
    if not os.path.exists(cfg_file):
        raise ValueError(f"Config file {cfg_file} not found")

    parser = configparser.ConfigParser()
    parser.read(cfg_file)

    rv = {}
    for section in parser.sections():
        if section not in rv:
            rv[section] = {}

        for k, v in parser.items(section):
            rv[section][k] = v
    return rv

Interface = namedtuple('Interface', ['phy', 'vir'])

def get_interface(vir_intf_id):
    vir_intf = VirtualInterface.objects.get(pk=vir_intf_id)
    phy_intf = PhysicalInterface.objects.get(pk=each.id)

def parse_macaddr(addr):
    addr = re.sub(r'[\.\s:-]+', '', addr)
    return "{:012x}".format(int(addr, 16))

def get_macaddr(virt_intf):
    qs = MacAddress.objects.filter(virtual_interface__id=virt_intf.id)
    cnt = len(qs)
    if cnt == 1:
        return qs[0]
    elif not cnt:
        raise ValueError('no mac addresses defined for interface')
    else:
        raise ValueError('multiple mac addresses already defined for interface')

def format_macaddr(addr):
	return ':'.join(map(''.join, list(zip(*[iter(addr)] * 2))))

def dns_intf_name(intf):
    regex = settings.RDNS_INTF_REGEX

    for (pattern, repl) in regex:
        intf = re.sub(pattern, repl, intf)
    return intf

