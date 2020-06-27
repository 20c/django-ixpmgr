

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

from ixpmgr import settings
from ixpmgr.models import Customer
from ixpmgr.models import PhysicalInterface
from ixpmgr.models import VirtualInterface
from ixpmgr.models import VlanInterface
from ixpmgr.models import ViewVlanInterfaceDetailsByCustid as ViewInterface
from ixpmgr import util


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            default=False,
            help='Force update for all entries'),
        )
    help = 'Scans for entries without rdns set, sets it, and then sends nsupdate to nameserver'

    @transaction.atomic
    def handle(self, *args, **options):
        log = logging.getLogger('ixpmgr.script')

        if options['force']:
            qs = ViewInterface.objects.all()
        else:
            # query for any interface that's enabled for ip and missing hostname
            qs = ViewInterface.objects.filter(~Q(ipv4address=0),
                ipv4enabled=1, ipv4hostname='')
            qs |= ViewInterface.objects.filter(~Q(ipv6address=0),
                ipv6enabled=1, ipv6hostname='')

        if not len(qs):
            return

        # len for next nibble
        zone_nibble_len = int(math.ceil(settings.RDNS_IPV6_PREFIX_LEN / 4))
        keyring = dns.tsigkeyring.from_text(settings.RDNS_KEYRING)
        updates={}

        for each in qs:
            cust = Customer.objects.get(pk=each.cust_id)
            phy_intf = PhysicalInterface.objects.get(pk=each.id)
            vir_intf = phy_intf.virtual_interface
            for vlan_intf in VlanInterface.objects.filter(virtual_interface__id=each.virtual_interface_id):
                intf = util.dns_intf_name(phy_intf.switchport.ifname)
                hostname = settings.RDNS_FORMAT.format(view=each, cust=cust, phy_intf=phy_intf, vir_intf=vir_intf, intf=intf)
                if not hostname.endswith('.') and not settings.RDNS_DOMAIN.startswith('.'):
                    hostname += '.'
                hostname += settings.RDNS_DOMAIN
                log.debug("set hostname='%s'" % (hostname,))

                if each.ipv4enabled and each.ipv4address:
                    ip = ipaddress.IPv4Address(each.ipv4address)
                    roctets = str(ip).split('.')[::-1]
                    upargs = (roctets.pop(0), settings.RDNS_TTL, 'ptr', hostname)
                    zone = '.'.join(roctets) + '.in-addr.arpa.'

                    updates.setdefault(zone, []).append(upargs)
                    vlan_intf.ipv4hostname = hostname

                if each.ipv6enabled and each.ipv6address:
                    ip = ipaddress.IPv6Address(each.ipv6address)
                    rnibble = ip.exploded[::-1].replace(':', '')
                    upargs = ('.'.join(rnibble) + '.ip6.arpa', settings.RDNS_TTL, 'ptr', hostname)
                    zone = '.'.join(rnibble[zone_nibble_len:]) + '.ip6.arpa.'

                    updates.setdefault(zone, []).append(upargs)
                    vlan_intf.ipv6hostname = hostname

                vlan_intf.save()

        # loop through all updates and send each zone at once
        for zone, upargs in list(updates.items()):

            nsup = dns.update.Update(zone, keyring=keyring)
            for each in upargs:
                nsup.replace(*each)
            res = dns.query.tcp(nsup, settings.RDNS_SERVER)

