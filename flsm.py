from typing import List
from copy import deepcopy
from prettytable import PrettyTable
from ipv4 import IP, NetworkAddress, logicOR, bits


def main():
    # start_addr = IP(input("Indirizzo di partenza: "))
    start_addr = NetworkAddress("20.0.0.0")
    subnetworks_num = 6

    subnet_mask = start_addr.choose_subnet_mask()
    broadcast_addr = logicOR(start_addr, subnet_mask.get_inverted())
    first_host_addr = start_addr + 1
    last_host_addr = broadcast_addr - 1
    subnetworks_bits = bits(subnetworks_num)
    new_subnet_mask = subnet_mask.add_bits(subnetworks_bits)
    block_size = 2**(8-subnetworks_bits)

    details_table = PrettyTable()
    details_table.add_rows([
        ["Network address", start_addr, start_addr.convert_to_binary()],
        ["Subnet mask", subnet_mask, subnet_mask.convert_to_binary()],
        ["Broadcast", broadcast_addr, broadcast_addr.convert_to_binary()],
        ["First host", first_host_addr, first_host_addr.convert_to_binary()],
        ["Last host", last_host_addr, last_host_addr.convert_to_binary()],
        ["Subnetworks", subnetworks_num, str(subnetworks_bits) + " bits"],
        ["New subnet mask", new_subnet_mask, new_subnet_mask.convert_to_binary()],
        ["Block size", block_size, ""]
    ])
    details_table.header = False
    details_table.align = "l"
    print(details_table)

    subnetting_octet = new_subnet_mask.get_subnetting_octet()
    subnetworks: List[IP] = []
    for i in range(subnetworks_num):
        new_octets = start_addr.octets
        new_octets[subnetting_octet] = str(i*block_size)
        subnetworks.append(IP(".".join(new_octets)))
    
    ips_table = PrettyTable()
    ips_table.field_names = ["Net num", "Network address", "Subnetting octet", 
                             "Broadcast", "First host address", "Last host address"]
    for i in range(len(subnetworks)):
        broadcast_subnetwork = deepcopy(subnetworks[i])
        
        # the subnetting octet is net + block size -1
        broadcast_subnetwork.octets[subnetting_octet] = str(int(
            broadcast_subnetwork.octets[subnetting_octet]) + block_size - 1)
        
        for j in range(subnetting_octet+1, 4):  # every octet to the right is 255
            broadcast_subnetwork.octets[j] = "255"

        ips_table.add_row([
            i+1,
            subnetworks[i],
            subnetworks[i].convert_to_binary().split(".")[subnetting_octet],
            broadcast_subnetwork,
            subnetworks[i]+1,
            broadcast_subnetwork-1
        ])
    
    print(ips_table)


if __name__ == "__main__":
    main()