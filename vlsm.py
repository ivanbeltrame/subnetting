from typing import List
from copy import deepcopy
from ipv4 import IP, NetworkAddress, SubnetMask, bits

def main():
    start_addr = NetworkAddress("192.168.1.0", cidr=24)

    subnetworks_sizes = [2, 40, 2, 16, 76]
    subnetworks_sizes.sort(reverse=True)

    print(f"{start_addr}/{start_addr.choose_subnet_mask().convert_to_cidr()}")

    subnetworks: List[IP] = []
    for i in range(len(subnetworks_sizes)):
        if len(subnetworks) == 0:
            new_subnetwork = deepcopy(start_addr)
        else:
            new_subnetwork = subnetworks[-1] + 2**bits(subnetworks_sizes[i-1]+2)

        subnetwork_bits = bits(subnetworks_sizes[i]+2)
        new_subnet_mask = SubnetMask("255.255.255.255").remove_bits(subnetwork_bits)
        new_subnetwork.cidr = new_subnet_mask.convert_to_cidr()
        new_subnetwork._subnet_mask = new_subnet_mask # not clean code
        subnetworks.append(new_subnetwork)

    for i in range(len(subnetworks)):
        print(f"{i+1}\t", end="")
        print(f"{subnetworks[i]}/{subnetworks[i].cidr}  \t", end="")
        # print(f"{subnetworks[i]._subnet_mask}\t", end="")

        subnetworks_subnet_mask = subnetworks[i]._subnet_mask
        subnetting_octet = subnetworks_subnet_mask.get_subnetting_octet()
        block_size = 256 - subnetworks_subnet_mask.octets[subnetting_octet]
        broadcast_addr = subnetworks[i] + block_size -1
        print(f"{subnetworks[i].convert_to_binary().split(".")[subnetting_octet]}\t", end="")
        print(f"{broadcast_addr}\t", end="")
        print(f"{subnetworks[i] +1}\t", end="")
        print(f"{broadcast_addr -1}\t", end="")
        print(f"{block_size}")

if __name__ == "__main__":
    main()