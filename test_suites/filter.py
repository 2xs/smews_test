# Returns a list of targets that need icmpv6 if built with ipv6
# For example, linux target does not need it as it uses a tun interface
# so it can be tested locally without the need to answer neighbor solicitation
# messages
def icmpv6_needed():
    return ['mbed_ethernet']

def discard_targets():
    """List of targets that must not be tested yet"""
    return ['WSN430wireless', 'GBA', 'WSN430', 'MicaZwireless', 'cygwin','WSN430','skeleton']


def is_v6(ip):
    return ':' in ip

def validate_build(build_options):
    # This function check if the build corresponds to a valid configuration
    # that has to be tested
    
    # skeleton is not a real target
    if build_options["target"] in discard_targets():
        return False

    # icmpv6 NEEDS GPIP, if disabled, the build should not be performed
    if "icmpv6" in build_options["apps"]:
        return not "gpip" in build_options["disable"]
    return True


def filter(build_options):
    # This is the global filter for smews tests.
    # It will perform some tests depending on the configuration, 
    # Modify the configuration if needed (for example, include the icmpv6 app when needed)
    # If a filter returns true, the test can be performed, otherwise, it is an incompatible test
    # so it will not be performed

    
    # First, check if we are in ipv6, and, if so, check if the target needs the icmpv6 app to work
    if is_v6(build_options["ipaddr"]):
        if build_options["target"] in icmpv6_needed():
            build_options["apps"] += ",icmpv6"
    
    return validate_build(build_options)
