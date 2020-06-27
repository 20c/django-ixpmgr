from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db import transaction
import dns.query
import dns.tsigkeyring
import dns.update
import ipaddress
import logging
import math
from optparse import make_option
import re

from ixpmgr.models import Customer
from ixpmgr.models import PhysicalInterface
from ixpmgr.models import Switch
from ixpmgr.models import VirtualInterface
from ixpmgr.models import VlanInterface
from ixpmgr.models import ViewVlanInterfaceDetailsByCustid as ViewInterface
from ixpmgr import const
from ixpmgr import util

from pysnmp.entity.rfc3413.oneliner import cmdgen
from snimpy.manager import Manager as M
from snimpy.manager import load


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--force",
            action="store_true",
            default=False,
            help="Force update for all entries",
        ),
    )
    help = "SNMP scan all switches and update mac addr table (does not work)"

    def handle(self, *args, **options):
        log = logging.getLogger("ixpmgr.script")

        conf = util.load_config()

        if options["force"]:
            qs = ViewInterface.objects.all()
        else:
            # query for any interface that's enabled for ip and missing hostname
            qs = ViewInterface.objects.filter(
                ~Q(ipv4address=0), ipv4enabled=1, ipv4hostname=""
            )
            qs |= ViewInterface.objects.filter(
                ~Q(ipv6address=0), ipv6enabled=1, ipv6hostname=""
            )

        qs = Switch.objects.filter(active=True, switchtype=const.SWITCHTYPE_SWITCH)
        for switch in qs:
            print(switch.name, switch.hostname, switch.snmppasswd)

        print(switch.name, switch.hostname, switch.snmppasswd)
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(switch.snmppasswd),
            cmdgen.UdpTransportTarget((switch.hostname, 161)),
            cmdgen.MibVariable("SNMPv2-MIB", "sysName", 0),
        )

        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print(
                    (
                        "%s at %s"
                        % (
                            errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1] or "?",
                        )
                    )
                )
            else:
                for name, val in varBinds:
                    print(("%s = %s" % (name.prettyPrint(), val.prettyPrint())))

        load("IF-MIB")
        load("SNMPv2-MIB")
        load("BRIDGE-MIB")
        load("Q-BRIDGE-MIB")
        # for id in s.dot1qPortIngressFiltering:

        m = M(switch.hostname, switch.snmppasswd)
        # m = M(switch.hostname, 'dev_aLFMBMoZ30dNy8NqnHDJJgtRfP3', 2)
        # print m.ifDescr[0]
        # print m.sysContact
        print(m.ifDescr)
        #        for idx in m.ifDescr:
        #            print m.ifDescr[idx]
        # dot1qTpFdbPort
        for i in m.dot1dBasePortIfIndex:
            ifidx = m.dot1dBasePortIfIndex[i]
            print("dot1d: ", i, m.dot1dBasePortIfIndex[i])
            # print "dot1d: ", i, m.dot1dBasePortIfIndex[i], " ifDescr: ", m.ifDescr[ifidx]
