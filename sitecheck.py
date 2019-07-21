#
# connected to website specified. checked time and download speed
#
import pycurl


#################################
# Class Name: URL
# Author: 0liver
# Date: 2019-07-22
# Description:
#################################
class URL:
    def __init__(self, str_url):
        self.__str_url = str_url
        self.__dns_time = float()
        self.__site_handshake_time = float()
        self.__site_transfer_time = float()
        self.__site_page_size = int()

    def get_dns_time(self):
        return self.__dns_time

    def get_site_handshake_time(self):
        return self.__site_handshake_time

    def get_site_transfer_time(self):
        return self.__site_transfer_time * 1000

    def get_site_page_size(self):
        return self.__site_page_size

    def get_transfer_speed(self):
        return self.__site_page_size / self.__site_transfer_time

    dns_time = property(get_dns_time, None)
    site_handshake_time = property(get_site_handshake_time, None)
    site_transfer_time = property(get_site_transfer_time, None)
    site_page_size = property(get_site_page_size, None)
    transer_speed = property(get_transfer_speed, None)

    def request_site(self):
        cURL = pycurl.Curl()
        try:
            cURL.setopt(pycurl.WRITEFUNCTION, self.bo)
        except pycurl.error as err:
            print(err)

        response = http.request('GET', self.__str_url)
        print(response)

if __name__ == '__main__':

    site = URL("http://www.sina.com.cn")

    site.request_site()
