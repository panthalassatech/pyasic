from typing import Union
import ipaddress


class MinerNetworkRange:
    """A MinerNetwork that takes a range of IP addresses.

    Parameters:
        ip_range: ## A range of IP addresses to put in the network, or a list of IPs
            * Takes a string formatted as:
                * {ip_range_1_start}-{ip_range_1_end}, {ip_address_1}, {ip_range_2_start}-{ip_range_2_end}, {ip_address_2}...
            * Also takes a list of strings formatted as:
                * [{ip_address_1}, {ip_address_2}, {ip_address_3}, ...]
    """

    def __init__(self, ip_range: Union[str, list]):
        self.host_ips = []
        if isinstance(ip_range, str):
            ip_ranges = ip_range.replace(" ", "").split(",")
            for item in ip_ranges:
                if "-" in item:
                    start, end = item.split("-")
                    start_ip = ipaddress.ip_address(start)
                    end_ip = ipaddress.ip_address(end)
                    networks = ipaddress.summarize_address_range(start_ip, end_ip)
                    for network in networks:
                        self.host_ips.append(network.network_address)
                        for host in network.hosts():
                            if host not in self.host_ips:
                                self.host_ips.append(host)
                        if network.broadcast_address not in self.host_ips:
                            self.host_ips.append(network.broadcast_address)
                else:
                    self.host_ips.append(ipaddress.ip_address(item))
        elif isinstance(ip_range, list):
            self.host_ips = [ipaddress.ip_address(ip_str) for ip_str in ip_range]

    def hosts(self):
        for x in self.host_ips:
            yield x
