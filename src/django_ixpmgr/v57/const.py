class Router:
    PROTOCOL_IPV4 = 4;
    PROTOCOL_IPV6 = 6;

    TYPE_ROUTE_SERVER                 = 1;
    TYPE_ROUTE_COLLECTOR              = 2;
    TYPE_AS112                        = 3;
    TYPE_OTHER                        = 99;

    SOFTWARE_BIRD                     = 1;
    SOFTWARE_BIRD2                    = 6;
    SOFTWARE_CISCO                    = 5;
    SOFTWARE_FRROUTING                = 3;
    SOFTWARE_GOBGP                    = 8;
    SOFTWARE_JUNOS                    = 7;
    SOFTWARE_QUAGGA                   = 2;
    SOFTWARE_OPENBGPD                 = 4;
    SOFTWARE_OTHER                    = 99;

    API_TYPE_NONE                     = 0;
    API_TYPE_BIRDSEYE                 = 1;
    API_TYPE_OTHER                    = 99;
