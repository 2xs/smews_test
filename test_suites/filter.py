def icmpv6_needed():
    return ['mbed_ethernet']

def is_v6(ip):
    return ':' in ip

def validate_build(build_options):
    # This function check if the build corresponds to a valid configuration
    # that has to be tested
    
    # icmpv6 NEEDS GPIP, if disabled, the build should not be performed
    if "icmpv6" in build_options["apps"]:
        return not "general_purpose_ip_handler" in build_options["disable"]
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
    
    print(build_options)
    return validate_build(build_options)
