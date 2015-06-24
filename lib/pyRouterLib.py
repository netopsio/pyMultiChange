class RouterLib(object):
    from os.path import expanduser
    import os.path
    import getpass

    """ User CREDENTIALS Module """
    creds_file = expanduser('~/.tacacslogin')
    if os.path.isfile(creds_file):
        f = open(creds_file, 'r')
        username = f.readline().strip()
        password = f.readline().strip()
        enable = f.readline().strip()
        f.close()
    else:
        print "Creating %s" % creds_file
        username = raw_input("Username: ")
        password = getpass.getpass("User Password: ")
        enable = getpass.getpass("Enable Password: ")

        f = open(creds_file, 'w')
        f.write(username + "\n" + password + "\n" + enable + "\n")
        f.close()

    """ SNMP Readonly CREDENTIALS Module """
    community_file = expanduser('~/.community')
    if os.path.isfile(community_file):
        f = open(community_file, 'r')
        snmp_read_only = f.readline().strip()
        f.close()
    else:
        print "Creating %s" % community_file
        snmp_read_only = raw_input("SNMP Read-only Community: ")

        f = open(community_file, 'w')
        f.write(snmp_read_only + "\n")
        f.close()

    def __init__(self):
        pass

    """ DEBUG Module """
    def enable_debug(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        verbose = True

        return verbose

    """ TELNET Module """
    """
    telnetlib documentation:
    https://docs.python.org/2/library/telnetlib.html
    """
    def use_telnet(self, host, username, password):
        import telnetlib
        import sys

        self.host = host
        self.username = username
        self.password = password
        self.access = telnetlib.Telnet(self.host)
        login_prompt = self.access.read_until("\(Username: \)|\(login: \)", 2)
        if 'login' in login_prompt:
            self.is_nexus = True
            self.access.write(username + "\n")
        elif 'Username' in login_prompt:
            self.is_nexus = False
            self.access.write(username + "\n")
        password_prompt = self.access.read_until('Password:', 1)
        self.access.write(password + "\n")
        if self.is_nexus is True:
            self.access.read_until("#")
            self.access.write("terminal length 0\n")
            self.access.read_until("#")
        else:
            self.access.read_until(">")
            self.access.write("enable\n")
            self.access.read_until("Password: ")
            self.access.write(RouterLib.enable + "\n")
            self.access.read_until("#")
            self.access.write("terminal length 0\n")
            self.access.read_until("#")

        return self.host, self.username, self.password, self.is_nexus, self.access

    """ SSH Module """
    """
    Paramiko Documentation:
    http://docs.paramiko.org/en/1.15/api/client.html
    """
    def use_ssh(self, host, username, password):
        import paramiko

        self.host = host
        self.username = username
        self.password = password
        self.access = paramiko.SSHClient()
        self.access.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.access.connect(host, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)

        return self.host, self.username, self.password, self.access

    """ SNMP Module """

    def use_snmp(self, host, community_string, mib_oid):
        from pysnmp.entity.rfc3413.oneliner import cmdgen

        """
        Snippet of code barrowed from Kirk Byers
        https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py
        """

        def snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=False):
            '''
            Retrieve the given OID
            Default OID is MIB2, sysDescr
            a_device is a tuple = (a_host, community_string, snmp_port)
            '''

            a_host, community_string, snmp_port = a_device
            snmp_target = (a_host, snmp_port)

            # Create a PYSNMP cmdgen object
            cmd_gen = cmdgen.CommandGenerator()

            (error_detected, error_status, error_index, snmp_data) = cmd_gen.getCmd(
                cmdgen.CommunityData(community_string),
                cmdgen.UdpTransportTarget(snmp_target),
                oid,
                lookupNames=True, lookupValues=True
            )

            if not error_detected:
                return snmp_data
            else:
                if display_errors:
                    print 'ERROR DETECTED: '
                    print '    %-16s %-60s' % ('error_message', error_detected)
                    print '    %-16s %-60s' % ('error_status', error_status)
                    print '    %-16s %-60s' % ('error_index', error_index)
                return None

        """
        Snippet of code barrowed from Kirk Byers
        https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py
        """

        def snmp_extract(snmp_data):
            '''
            Unwrap the SNMP response data and return in a readable format
            Assumes only a single list element is returned
            '''

            if len(snmp_data) > 1:
                raise ValueError("snmp_extract only allows a single element")

            if len(snmp_data) == 0:
                return None
            else:
                # Unwrap the data which is returned as a tuple wrapped in a list
                return snmp_data[0][1].prettyPrint()

        snmp_port = 161

        a_device = (host, community_string, snmp_port)
        snmp_data = snmp_get_oid(a_device, mib_oid, display_errors=False)

        # return snmp_get_oid(a_device, mib_oid, display_errors=False)
        return snmp_extract(snmp_data)
