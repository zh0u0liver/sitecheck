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

    def __get_dns_time(self):
        return self.__dns_time

    def __get_status_code(self):
        return self.__status_code

    def __get_connect_time(self):
        return self.__connect_time

    def __get_pre_transfer_time(self):
        return self.__pre_transfer_time

    def __get_start_transfer_time(self):
        return self.__start_transfer_time

    def __get_total_time(self):
        return self.__total_time

    def __get_transfer_speed(self):
        return self.__transfer_speed

    def __get_effect_site(self):
        return self.__effect_site

    def __get_content_length(self):
        return self.__content_length

    def __get_size_download(self):
        return self.__size_download

    def __get_header_size(self):
        return self.__header_size

    # 利用property 创建只读属性
    dns_time = property(__get_dns_time, None)
    status_code = property(__get_status_code, None)
    connect_time = property(__get_connect_time, None)
    pre_transfer_time = property(__get_pre_transfer_time, None)
    start_transfer_time = property(__get_start_transfer_time, None)
    total_time = property(__get_total_time, None)
    transfer_speed = property(__get_transfer_speed, None)
    effect_site = property(__get_effect_site, None)
    content_length = property(__get_content_length, None)
    size_download = property(__get_size_download, None)
    header_size = property(__get_header_size, None)

    def request_site(self):
        curl = pycurl.Curl()

        curl.setopt(pycurl.CONNECTTIMEOUT, 10)
        curl.setopt(pycurl.TIMEOUT, 10)
        curl.setopt(pycurl.NOPROGRESS, 1)
        curl.setopt(pycurl.FORBID_REUSE, 1)
        curl.setopt(pycurl.MAXREDIRS, 3)
        curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.URL, self.__str_url)
        # 否则可能会出现部分网站40x错误（403）
        curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0')

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
    parse_result = None
    try:
        parse_result = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(0)
    except argparse.ArgumentTypeError:
        parser.print_help()
        exit(0)
    except Exception as err:
        print(err)
        parser.print_help()
        exit(0)

    host_file_name = parse_result.host_file_name
    output_file_name = parse_result.output_file_name

    str_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    try:
        str_title = "%150s%16s%16s%16s%16s%16s%16s%16s%151s%16s%16s%16s"
        str_result = "%150s%16.2f%16s%16.2f%16.2f%16.2f%16.2f%16s%151s%16s%16s%16s"
        with open(host_file_name) as host_file, open(str_time + ".txt", "w") as output_file:
            tup_title = ("URL","DNS Time","Return Code","Connected Time",
                         "Prepare Time","Transfer Time","Total Time",
                         "Transfer Speed","Effect URL",
                         "Content Length","Download Size","Head Size")
            print(str_title % tup_title)
            output_file.write((str_title + "\n") % tup_title)
            for host_name in host_file.readlines():
                sub = host_name.strip('\n')
                if not sub: #or sub in host_name:
                    continue
                site = URL(sub)
                site.request_site()
                tup_result = (sub,
                              site.dns_time,
                              site.status_code,
                              site.connect_time,
                              site.pre_transfer_time,
                              site.start_transfer_time,
                              site.total_time,
                              site.transfer_speed,
                              site.effect_site,
                              site.content_length,
                              site.size_download,
                              site.header_size)
                print(str_result % tup_result)
                output_file.write((str_result + "\n") % tup_result)
    except IOError as err:
        print("File Error:" + str(err))