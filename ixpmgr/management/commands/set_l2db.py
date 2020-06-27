

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db import transaction
import dns.query
import dns.tsigkeyring
import dns.update
import logging

from ixpmgr.models import MacAddress
from ixpmgr.models import VirtualInterface
from ixpmgr import util


class Command(BaseCommand):
    args = '<virtual interface id> <mac address>'
    help = 'set mac address for port'

    def handle(self, *args, **options):
        log = logging.getLogger('ixpmgr.script')

        conf = util.load_config()

        if len(args) != 2:
            self.stdout.write(self.usage(""))
            raise CommandError("virtual interface id and mac address are required")

        vir_intf_id = int(args[0])
        macaddr = util.parse_macaddr(args[1])
        try:
            vir_intf = VirtualInterface.objects.get(pk=vir_intf_id)
        except VirtualInterface.DoesNotExist:
            raise CommandError('virtual interface "%s" does not exist' % vir_intf_id)

        qs = MacAddress.objects.filter(virtual_interface__id=vir_intf_id)
        cnt = len(qs)
        if not cnt:
            mac = MacAddress(virtual_interface=vir_intf, mac=macaddr)
        elif cnt == 1:
            mac = qs[0]
        else:
            raise CommandError('multiple mac addresses already defined for interface')

        mac.mac = macaddr
        mac.save()

