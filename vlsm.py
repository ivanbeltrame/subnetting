from copy import deepcopy
from prettytable import PrettyTable
from ipv4 import IP, NetworkAddress, SubnetMask, bits


def vlsm(network_address: str, subnetworks_sizes: list[int], cidr: int = 24):
    start_addr = NetworkAddress(network_address, cidr)

    subnetworks_sizes.sort(reverse=True)

    print(f"{start_addr}/{start_addr.choose_subnet_mask().convert_to_cidr()}")

    subnetworks: list[IP] = []
    for i in range(len(subnetworks_sizes)):
        if len(subnetworks) == 0:
            new_subnetwork = deepcopy(start_addr)
        else:
            new_subnetwork = subnetworks[-1] + 2**bits(subnetworks_sizes[i-1]+2)

        subnetwork_bits = bits(subnetworks_sizes[i]+2)
        new_subnet_mask = SubnetMask("255.255.255.255").remove_bits(subnetwork_bits)
        new_subnetwork.cidr = new_subnet_mask.convert_to_cidr()
        new_subnetwork._subnet_mask = new_subnet_mask  # not clean code
        subnetworks.append(new_subnetwork)

    table = PrettyTable()
    table.field_names = ["Net num", "Network address", "Subnetting octet",
                         "Broadcast", "First host address", "Last host address", "Block size"]
    for i in range(len(subnetworks)):
        subnetworks_subnet_mask = subnetworks[i]._subnet_mask
        subnetting_octet = subnetworks_subnet_mask.get_subnetting_octet()
        block_size = 256 - subnetworks_subnet_mask.octets[subnetting_octet]
        broadcast_addr = subnetworks[i] + block_size - 1

        table.add_row([
            i+1,
            f"{subnetworks[i]}/{subnetworks[i].cidr}",
            subnetworks[i].convert_to_binary().split(".")[subnetting_octet],
            broadcast_addr,
            subnetworks[i] + 1,
            broadcast_addr - 1,
            block_size
        ])
    print(table)