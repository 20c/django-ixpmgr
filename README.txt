
# django-ixpmgr
A (very much work in progress) django overlay for INEX's IXP-Manager

### License

Copyright 2015 20C, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this softare except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### Configuration

Django settings (defined in config as IXPMGR_<NAME>, included as ixpmgr.settings.<NAME>):

HOME = getattr(settings, 'IXPMGR_HOME', '/usr/local/ixp')

RDNS_DOMAIN= getattr(settings, 'IXPMGR_RDNS_DOMAIN', '')
RDNS_FORMAT = getattr(settings, 'IXPMGR_RDNS_FORMAT', 'as{cust.autsys}.{intf}.{phy_intf.switchport.switch.name}')
RDNS_INTF_REGEX = getattr(settings, 'IXPMGR_RDNS_INTF_REGEX', [('[ /]', '-')])
RDNS_IPV6_PREFIX_LEN= getattr(settings, 'IXPMGR_RDNS_IPV6_PREFIX_LEN', 64)
RDNS_KEYRING = getattr(settings, 'IXPMGR_RDNS_KEYRING', {})
RDNS_SERVER = getattr(settings, 'IXPMGR_RDNS_SERVER', None)
RDNS_TTL= getattr(settings, 'IXPMGR_RDNS_TTL', 86400)

### Commands

`upd_rdns`
    updates RDNS based on configured template for ports without RDNS
    --force to do all of them

`set_l2db` <virtual interface id> <mac address>
    updates mac address for specified virtual port

### Model
Model is currently largely just done from a `manage.py inspectdb`, with some
normalization. This is by no means complete, specifically, anything marked with
'# Field name made lowercase.' should be converted to use underscores.

### Session integration

Must add to django settings:
    SESSION_COOKIE_NAME = 'sid'

Must add to application.ini:

    resources.session.name = sid
    resources.session.hash_bits_per_character = 6

### Versioning
First 3 octets of version match the official IXP-Manager release, anything with
a 4th octect should be considered development.


