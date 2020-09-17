import os
from twilio.rest import Client


def scanner(ip_address, clients):
    """A function that sends a ping request to all the computers on the network and adds the addresses that respond to the request to the clients list.
    At the addresses in this list we will perform the scan in the following function
    :param ip_address:IP address of one of the devices on the network (Subnet mask is class c)
    :param clients:An empty list to which all the addresses responding to the ping request will be added
    """
    result = os.popen("ping {0} -n 3".format(ip_address)).read()
    if "TTL" in result:
        clients.append(ip_address)


def function_send_sms_all_ip(clients, to_phone_number, from_phone_number, account_sid_sms, auth_token_sms):
    """A function that sends a ping request to all IP addresses every 10 minutes and if it does not
     receive a response from one of the addresses, it sends an SMS alert
    :param clients: List of IP addresses on the network that responded to the ping request in the previous scan
    :param from_phone_number: The phone number you received from twilio. From this number you will be sent an sms with an alert
    :param to_phone_number: Your phone number to which the sms will be sent
    :param account_sid_sms: your account_sid. This number can be found in your twilio account
    :param auth_token_sms: your auth_token. This number can be found in your twilio account
    """
    for cli in clients:
        ping_output = os.popen("ping -n 3 {0}".format(cli)).read()
        if "TTL" not in ping_output:
            account_sid = account_sid_sms
            auth_token = auth_token_sms
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body='Warning: The ip address {0} does not respond to ping requests'.format(cli),
                from_=from_phone_number,
                to=to_phone_number
            )


def check_dns():
    """A function that checks if the dns server Working Properly
    by executing the nslookup command
    :return:Does the nslookup command return normal input or not
    :rtype:str
    """
    output_check_dns = os.popen("nslookup facebook.com").read()
    if "UnKnown" in output_check_dns:
        return "There is a problem. Maybe your dns server is a hidden or inactive server"
    else:
        return "Your dns settings are excellent. Well done!"


def flush_dns():
    """A function which executes an os command which deletes the cache memory of the dns server
    :return: if successful or not
    :rtype:str
    """
    flush_command = os.popen("ipconfig /flushdns").read()
    if "Successfully" in flush_command:
        return "the transaction completed successfully"
    else:
        return "We apologize, there is an error"


def display_dns():
    """A function that displays the information in the cache memory of the dns server
    :return:if successful or not
    """
    output_display_dns = os.popen("ipconfig /displaydns").read()
    if "not display" in output_display_dns:
        return "We apologize, there is an error"
    else:
        return output_display_dns
