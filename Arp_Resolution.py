import re
import csv
import os
from datetime import datetime
# encoding: utf-8
# function: 该脚本用于解析ip和mac地址对应关系,并将对应ip添加到端口统计表中
# input: sh_ip_arp.log，端口统计表.csv
# output: 待处理端口统计表.csv
# Time: 2017/6/19

# 根据sh ip arp结果查找ip和mac对应表格
def ip_arp_resolution(file_path):
    #打开文文本
    file = open(file_path, 'r', encoding='utf8')
    #读取文本内容
    text = file.read()
    file.close()
    arp_table = re.compile(r'[1-2]{2}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\S+\s+\S+\s+\S+', re.S)
    arps = arp_table.findall(text, re.S)
    # print(arps)

    ip_mac_dict = {}
    for arp in arps:
        ip_mac_regx = re.split(r'\s+', arp)
        if ip_mac_regx:
            ip = ip_mac_regx[0]
            mac = ip_mac_regx[2]
            ip_mac_dict['%s' % mac] = ip
    # print(ip_mac_dict)

    return ip_mac_dict

# 根据arp表，在原来的端口状态表格中添加一列‘port_ip’
def process_ip_arp():
    # 改变当前目录到 D:\python\csv
    os.chdir('D:\python\csv')
    int_file = open('ports_status.csv',mode='w', encoding='utf8', newline='')
    int_csv_file = csv.writer(int_file)
    int_csv_file.writerow(['ip', 'interface', 'status', 'syslog_status', 'mode', 'type', 'mac', 'mac_history', 'vlan-id', 'show_run', 'update', 'auth_mode', 'port_ip'])

    with open('端口状态.csv', 'r') as f:
        f.readline()
        port_file = csv.reader(f)

        ip_mac_dict = ip_arp_resolution('sh_ip_arp.log')
        # print(ip_mac_dict)


        for line in port_file:
            macs = line[6]
            mac_table = macs.splitlines()
            ip_table = ''
            for mac in mac_table:
                ip = ip_mac_dict.get(mac)
                if ip:
                    ip_table = ip_table + ip + '\n'
                    # print(ip_table)
            if ip_table:
                line.append(ip_table)
            int_csv_file.writerow(line)



if __name__ == '__main__':
    # ip_arp_resolution('sh_ip_arp.log')
    process_ip_arp()

