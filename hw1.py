from ipaddress import ip_address
from socket import gethostbyname
from subprocess import PIPE, Popen
from tabulate import tabulate


def host_ping(hosts):
    reachable = []
    unreachable = []
    ping_dict = {'Reachable hosts': reachable, 'Unreachable hosts': unreachable}
    for addr in hosts:
        address = None
        try:
            address = ip_address(addr)
        except:
            if address is None:
                try:
                    address = ip_address(gethostbyname(addr))
                except:
                    print(f'{addr} is not hostname or ip address')
                    continue

        ping_process = Popen(f"ping {address}", stdout=PIPE)
        ping_process.wait()
        if ping_process.returncode == 0:
            result = f'{address} is reachable'
            reachable.append(address)
        else:
            result = f'{address} is unreachable'
            unreachable.append(address)
        print(result)
    return ping_dict


def host_range_ping(start_addr, end_addr):
    print(f'Cheking range {start_addr} ... {end_addr}')
    hosts = []
    try:
        start_address = ip_address(start_addr)
        end_address = ip_address(end_addr)
    except:
        print(f'Inappropriate range of ip addresses')
    current_address = start_address
    while current_address < end_address:
        hosts.append(current_address)
        current_address += 1
    return host_ping(hosts)


def host_range_ping_tab(start_adr, end_adr):
    result_table = host_range_ping(start_adr, end_adr)
    print(tabulate(result_table, headers='keys', tablefmt="grid", stralign="center"))


if __name__ == '__main__':
    host_list = ['localhost', '8.8.8.8', 'google.com', '192.168.121.1', 'unknown.404', 'gb.ru']
    host_ping(host_list)
    host_range_ping_tab('8.8.8.6', '8.8.8.11')
