#
# connected to website specified. checked time and download speed
#
import argparse
import time
import pycurl
from io import BytesIO
# from io import StringIO


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
        self.__status_code = int()
        self.__connect_time = float()
        self.__pre_transfer_time = float()
        self.__start_transfer_time = float()
        self.__total_time = float()
        self.__transfer_speed = float()
        self.__effect_site = str()
        self.__content_length = int()
        self.__size_download = int()
        self.__header_size = int()

    def get_dns_time(self):
        return self.__dns_time

    def get_status_code(self):
        return self.__status_code

    def get_connect_time(self):
        return self.__connect_time

    def get_pre_transfer_time(self):
        return self.__pre_transfer_time

    def get_start_transfer_time(self):
        return self.__start_transfer_time

    def get_total_time(self):
        return self.__total_time

    def get_transfer_speed(self):
        return self.__transfer_speed

    def get_effect_site(self):
        return self.__effect_site

    def get_content_length(self):
        return self.__content_length

    def get_size_download(self):
        return self.__size_download

    def get_header_size(self):
        return self.__header_size

    dns_time = property(get_dns_time, None)
    status_code = property(get_status_code, None)
    connect_time = property(get_connect_time, None)
    pre_transfer_time = property(get_pre_transfer_time, None)
    start_transfer_time = property(get_start_transfer_time, None)
    total_time = property(get_total_time, None)
    transfer_speed = property(get_transfer_speed, None)
    effect_site = property(get_effect_site, None)
    content_length = property(get_content_length, None)
    size_download = property(get_size_download, None)
    header_size = property(get_header_size, None)

    def request_site(self):
        curl = pycurl.Curl()

        curl.setopt(pycurl.CONNECTTIMEOUT, 5)
        curl.setopt(pycurl.TIMEOUT, 5)
        curl.setopt(pycurl.NOPROGRESS, 1)
        curl.setopt(pycurl.FORBID_REUSE, 1)
        curl.setopt(pycurl.MAXREDIRS, 3)
        curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(curl.URL, self.__str_url)

        byte_io = BytesIO()  # 使用StringIO会出错，需要查一下

        try:
            curl.setopt(curl.WRITEFUNCTION, byte_io.write)
            curl.perform()
            self.__status_code = curl.getinfo(pycurl.HTTP_CODE)  # HTTP状态码
            self.__dns_time = curl.getinfo(pycurl.NAMELOOKUP_TIME) * 1000  # DNS消耗时间
            self.__connect_time = curl.getinfo(pycurl.CONNECT_TIME) * 1000  # 建连消耗时间
            self.__pre_transfer_time = curl.getinfo(pycurl.PRETRANSFER_TIME) * 1000  # 建连到准备传输消耗
            self.__start_transfer_time = curl.getinfo(pycurl.STARTTRANSFER_TIME) * 1000  # 建连到传输消耗
            self.__total_time = curl.getinfo(pycurl.TOTAL_TIME) * 1000  # 传输结束消耗时间
            self.__transfer_speed = curl.getinfo(pycurl.SPEED_DOWNLOAD)  # 平均下载速度
            self.__effect_site = curl.getinfo(pycurl.EFFECTIVE_URL)  # 实际连接的URL
            self.__content_length = curl.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)  # 网页内容的长度
            self.__size_download = curl.getinfo(pycurl.SIZE_DOWNLOAD)  # 实际下载的大小
            self.__header_size = curl.getinfo(pycurl.HEADER_SIZE)   # 头部大小

            byte_io.close()
            curl.close()
            
        except pycurl.error as err:
            print(err)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("host_file_name", action="store", help="spcify a hosts file name which need be resolved")
    parser.add_argument("-o", action="store", dest="output_file_name", help="output file name")
    try:
        parse_result = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(0)
    except argparse.ArgumentTypeError:
        parser.print_help()
        exit(0)
    except:
        parser.print_help()
        exit(0)

    host_file_name = parse_result.host_file_name
    output_file_name = parse_result.output_file_name

    str_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    try:
        with open(host_file_name) as host_file, open(str_time + ".txt", "w") as output_file:
            for host_name in host_file.readlines():
                sub = host_name.strip('\n')
                if not sub: #or sub in host_name:
                    continue
                site = URL(sub)
                site.request_site()
                print("%50s" % sub,
                      "%8.2fms" % site.dns_time,
                      "%6s" % site.status_code,
                      "%8.2fms" % site.connect_time,
                      "%8.2fms" % site.pre_transfer_time,
                      "%8.2fms" % site.start_transfer_time,
                      "%8.2fms" % site.total_time,
                      "%10s" % site.transfer_speed,
                      "%50s" % site.effect_site,
                      "%10s" % site.content_length,
                      "%10s" % site.size_download,
                      "%10s" % site.header_size)

                # print("dns_resolve_time:%8.2fms" % site.resolve_time, "ip_list:", site.ip_addr)
                # output_file.write("%50s\t%8.2f\t%s\n"%(sub,dns_check_name.resolve_time,dns_check_name.ip_addr))
    except IOError as err:
        print("File Error:" + str(err))