import eel
import os
import time
from datetime import datetime
from twilio.rest import Client
from functions import scanner, function_send_sms_all_ip, check_dns, flush_dns, display_dns
import threading


class NetworkAdministrator(object):
    def __init__(self, ip_address, send_to, time_to_start, time_to_stop, send_from, account_sid, auth_token):
        """NetworkAdministrator class boot method. class NetworkAdministrator is q class that contains functions whose function is to build
       software that will assist the network administrator in his work and send him an
       SMS when a computer on the network does not respond to ping requests.
        :param ip_address: The ip address that the user will want to scan / ip address within the range of the network that the user will want to scan
        :param send_to: Your phone number to which the sms will be sent
        :param time_to_start: Scan start time. The scan will start as soon as you click Start. This parameter will only be relevant when the time entered as a value for the variable arrives next time
        :param time_to_stop: Scan start time. The scan will be restart when the time wile is the time entered as a value for the time_to_start variable
        :param send_from: The phone number you received from twilio. From this number you will be sent an sms with an alert
        :param account_sid: your account_sid. This number can be found in your twilio account
        :param auth_token: your auth_token. This number can be found in your twilio account
        """
        self.ip_address = ip_address
        self.send_to = send_to
        self.time_to_start = time_to_start
        self.time_to_stop = time_to_stop
        self.send_from = send_from
        self.account_sid = account_sid
        self.auth_token = auth_token

    def function_time_now(self):
        """A function that returns the time now
        :return: time now
        :rtype:str
        """
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def ping_my_ip_address(self):
        """A function that sends a ping request to the IP address entered by the user
        :return: True if the ip address responds to the ping request, false if not
        """
        ping_one_ip = os.popen("ping -n 1 {0}".format(self.ip_address)).read()
        if "TTL" in ping_one_ip:
            return True
        else:
            return False

    def send_sms_one_address(self):
        """Sending an sms to the phone number entered by the user if the IP address he chose does not respond to
         the ping request.The ping request is sent every 10 minutes
        """
        while True:
            if self.function_time_now != self.time_to_stop:
                self.ping_my_ip_address()
                if not self.ping_my_ip_address():
                    account_sid = self.account_sid
                    auth_token = self.auth_token
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        body='Warning: The ip address {0} does not respond to ping requests'.format(self.ip_address),
                        from_=self.send_from,
                        to=self.send_to
                    )
                    time.sleep(600)
                if self.function_time_now == self.time_to_start:
                    continue


class FollowTheEntireNetwork(NetworkAdministrator):
    def __init__(self, ip_address, send_to, time_to_start, time_to_stop, send_from, account_sid, auth_token):
        """FollowTheEntireNetwork class boot method inherited from the NetworkAdministrator class
        FollowTheEntrieNetwork is a class that inherits from the NetworkAdministrator class the boot method values.
        This department scans the entire network and sends an sms to the user if one of the
        devices that responded to the first ping request does not respond to the ping requests afterwards
    """
        super().__init__(ip_address, send_to, time_to_start, time_to_stop, send_from, account_sid, auth_token)
        self.clients = []
        NetworkAdministrator.function_time_now(self)

    def ping_to_all_network(self):
        """This function passes the relevant values ​​to a separate function that scans all possible addresses
         on the network (assuming the Subnet mask is class c).
         This scan will determine which web addresses will be scanned afterwards.
         The scan function is performed in a thread
        """
        ip_format = self.ip_address[:self.ip_address.rfind(".") + 1]

        for number in range(1, 255):
            ip = ip_format + str(number)
            thread_scanner = threading.Thread(target=scanner, args=(ip, self.clients,))
            thread_scanner.start()

    def send_sms_all_address(self):
        """A function that passes the relevant values ​​to the function that scans and sends sms if one of
         the network addresses entered in the clients list in the scanner function does not respond to the ping request.
         The function first checks whether the time condition is True.
         The scan and send sms function is performed in a thread
        """
        while True:
            if self.function_time_now != self.time_to_stop:
                # The time conditions are written so and not "if time_to_start < function_time_now() < time_to_stop"
                # Because in case time to start == 7:00 and time to stop == 1:00 at night, the condition will
                # not be relevant, since 8:00 in the morning is greater than 1:00 at night mathematically
                thread_all_address = threading.Thread(target=function_send_sms_all_ip, args=(
                    self.clients, self.send_to, self.send_from, self.account_sid, self.auth_token,))
                thread_all_address.start()
                time.sleep(600)
            if self.function_time_now == self.time_to_start:
                continue


@eel.expose
def my_function_one(ip_address, to_number, time_to_start, time_to_stop, from_number, account_sid, auth_token):
    """
    A function which passes eel to the Network Administrator class
    """
    my_class = NetworkAdministrator(ip_address, to_number, time_to_start, time_to_stop, from_number, account_sid,
                                    auth_token)
    my_class.function_time_now()
    my_class.ping_my_ip_address()
    my_class.send_sms_one_address()


@eel.expose
def my_function_to(ip_address, to_number, time_to_start, time_to_stop, from_number, account_sid, auth_token):
    """A function which passes eel to the FollowTheEntireNetwork class
    """
    my_class_to = FollowTheEntireNetwork(ip_address, to_number, time_to_start, time_to_stop, from_number, account_sid, auth_token)
    my_class_to.function_time_now()
    my_class_to.ping_to_all_network()
    my_class_to.send_sms_all_address()


# Calling eel is done through another function, For reading the code will be more convenient

@eel.expose
def return_check_dns():
    """A function that passes eel the value that returns in the check_dns function
    :return:check_dns function
    """
    return check_dns()


@eel.expose
def flush_dns_t_f():
    """A function that passes eel the value that returns in the flush_dns_t_f function
    :return:flush_dns function
    """
    return flush_dns()


@eel.expose
def display_dns_cache():
    """A function that passes eel the value that returns in the display_dns_cache function
    :return:display_dns function
    """
    return display_dns()


eel.init('web')
eel.start('main.html', size=(1050, 450))
