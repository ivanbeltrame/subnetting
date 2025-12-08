from typing import List
from copy import deepcopy
from ipv4 import IP, NetworkAddress, logicOR, bits

def main():
    # start_addr = IP(input("Indirizzo di partenza: "))
    subnetworks_num = 38
    start_addr = NetworkAddress("172.20.0.0")
    print(f"Network address:\t {start_addr}\t{start_addr.convert_to_binary()}")

    subnet_mask = start_addr.choose_subnet_mask()
    print(f"Subnet mask: \t\t {subnet_mask}\t{subnet_mask.convert_to_binary()}")
    
    broadcast_addr = logicOR(start_addr, subnet_mask.get_inverted())
    print(f"Broadcast:   \t\t {broadcast_addr}\t{broadcast_addr.convert_to_binary()}")

    first_host_addr = start_addr + 1
    print(f"First host:  \t\t {first_host_addr}\t{first_host_addr.convert_to_binary()}")

    last_host_addr = broadcast_addr - 1
    print(f"Last host:   \t\t {last_host_addr}\t{last_host_addr.convert_to_binary()}")

    subnetworks_bits = bits(subnetworks_num)
    print(f"Subnetworks: {subnetworks_num}; bits: {subnetworks_bits}")

    new_subnet_mask = subnet_mask.add_bits(subnetworks_bits)
    print(f"New subnet mask:   \t {new_subnet_mask}\t{new_subnet_mask.convert_to_binary()}")

    block_size = 2**(8-subnetworks_bits)
    print(f"Block size: {block_size}")
    subnetting_octet = new_subnet_mask.get_subnetting_octet()
    subnetworks: List[IP] = []
    for i in range(1, subnetworks_num+1):
        new_octets = start_addr.octets
        new_octets[subnetting_octet] = str(i*block_size)
        subnetworks.append(IP(".".join(new_octets)))
    
    for i in range(len(subnetworks)):
        print(f"{i+1}\t", end="")
        print(f"{subnetworks[i]}\t", end="")
        print(f"{subnetworks[i].convert_to_binary().split(".")[subnetting_octet]}\t", end="")
        broadcast_subnetwork = deepcopy(subnetworks[i])
        broadcast_subnetwork.octets[subnetting_octet] = str(int(broadcast_subnetwork.octets[subnetting_octet]) + block_size - 1) # the subnetting octet is net + block size -1
        for j in range(subnetting_octet+1, 4): # every octet to the right is 255
            broadcast_subnetwork.octets[j] = "255"

        print(f"{broadcast_subnetwork}\t", end="")
        print(f"{subnetworks[i]+1}\t", end="")
        print(f"{broadcast_subnetwork-1}\t")


if __name__ == "__main__":
    main()