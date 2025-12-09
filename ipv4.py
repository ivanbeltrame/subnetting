from typing import Self
import math


class IP:
    def __init__(self, ip: str, cidr: int | None = None, bin: bool = False):
        self.ip = ip
        self.cidr = cidr
        self.bin = bin
        self._subnet_mask: SubnetMask | None = None
        self.octets = ip.split(".")

        self.__validate_ip()

    def __validate_ip(self) -> None:
        if len(self.octets) != 4:
            raise ValueError("IP must have 4 octets!")
        
        if self.bin:
            self.__convert_from_binary()

        for octet in self.octets:  # rewrite with range() and indexes
            try:
                octet_int = int(octet)
                # self.octets[self.octets.index(octet)] = int(octet)
            except ValueError:
                raise ValueError("Octets must be integers!")
            
            if octet_int < 0 or octet_int > 255:
                raise ValueError("Octets must be between 0 and 255")

    def __convert_from_binary(self) -> None:
        try:
            dec_octets = []
            for octet in self.octets:
                dec_octets.append(int(octet, 2))

            self.octets = dec_octets
        except ValueError:
            raise ValueError("IP isn't binary")

    def __str__(self):
        return f"{self.octets[0]}.{self.octets[1]}.{self.octets[2]}.{self.octets[3]}"
    
    def convert_to_binary(self) -> str:
        bin_octets = []
        for octet in self.octets:
            bin_octets.append(format(int(octet), '08b'))

        return ".".join(bin_octets)
    
    def get_class(self) -> str:
        first_bin_octet = self.convert_to_binary().split(".")[0]

        if first_bin_octet.startswith("0"):
            ip_class = "A"
        elif first_bin_octet.startswith("10"):
            ip_class = "B"
        elif first_bin_octet.startswith("110"):
            ip_class = "C"
        elif first_bin_octet.startswith("1110"):
            ip_class = "D"
        elif first_bin_octet.startswith("1111"):
            ip_class = "E"
        
        try:
            return ip_class
        except UnboundLocalError:
            raise ValueError("IP doesn't belong to any class?")
    
    def is_private(self) -> bool:
        is_private = False
        if self.is_between(IP("10.0.0.0"), IP("10.255.255.255")):
            is_private = True
        elif self.is_between(IP("172.16.0.0"), IP("172.31.255.255")):
            is_private = True
        elif self.is_between(IP("192.168.0.0"), IP("192.168.255.255")):
            is_private = True
        
        return is_private
    
    def is_between(self, start_addr: Self, end_addr: Self) -> bool:
        for i in range(4):
            if (not (self.octets[i] >= start_addr.octets[i])) or (not (self.octets[i] <= end_addr.octets[i])):
                return False
        return True

    def choose_subnet_mask(self) -> "SubnetMask":
        ip_class = self.get_class()
        if ip_class == "A":
            subnet_mask = SubnetMask("255.0.0.0")
        elif ip_class == "B":
            subnet_mask = SubnetMask("255.255.0.0")
        elif ip_class == "C":
            subnet_mask = SubnetMask("255.255.255.0")

        try:
            return subnet_mask
        except UnboundLocalError:
            raise ValueError("Can't choose a subnet mask to the IP")
        
    def get_inverted(self) -> Self:
        inverted_octets = []
        for octet in self.convert_to_binary().split("."):
            inverted_octet = ""
            for bit in octet:
                inverted_octet += "1" if bit == "0" else "0"
            inverted_octets.append(inverted_octet)
        return IP(".".join(inverted_octets), bin=True)
    
    def __add__(self, n: int) -> Self:
        added_octets = [int(x) for x in self.octets]
        for _ in range(n):
            added_octets[3] += 1
            if added_octets[3] == 256:
                added_octets[3] = 0
                added_octets[2] += 1
                if added_octets[2] == 256:
                    added_octets[2] = 0
                    added_octets[1] += 1
                    if added_octets[1] == 256:
                        added_octets[1] = 0
                        added_octets[0] += 1
                        if added_octets[0] == 256:
                            raise ValueError(f"Can't add {n} to IP")
        return IP(".".join([str(x) for x in added_octets]))
                        
    def __sub__(self, n: int) -> Self:
        subtracted_octets = [int(x) for x in self.octets]
        for _ in range(n):
            subtracted_octets[3] -= 1
            if subtracted_octets[3] == -1:
                subtracted_octets[3] = 255
                subtracted_octets[2] -= 1
                if subtracted_octets[2] == -1:
                    subtracted_octets[2] = 255
                    subtracted_octets[1] -= 1
                    if subtracted_octets[1] == -1:
                        subtracted_octets[1] = 255
                        subtracted_octets[0] -= 1
                        if subtracted_octets[0] == -1:
                            raise ValueError(f"Can't subtract {n} to IP")
        return IP(".".join([str(x) for x in subtracted_octets]))
        
    def __repr__(self):
        return f"IP(\"{self.octets[0]}.{self.octets[1]}.{self.octets[2]}.{self.octets[3]}\")"


class NetworkAddress(IP):
    def __init__(self, ip: str, cidr: int | None = None, bin: bool = False):
        super().__init__(ip, cidr, bin=bin)


class SubnetMask(IP):
    def __init__(self, ip: str, bin: bool = False):
        super().__init__(ip, bin=bin)
    
    def add_bits(self, n: int) -> "SubnetMask":
        added_ip = ""
        for bit in self.convert_to_binary():
            if bit == "0":
                if n > 0:
                    bit = "1"
                    n -= 1
            added_ip += bit
        if n > 0:
            raise ValueError("Can't add bits to subnet mask")
        return SubnetMask(added_ip, bin=True)
    
    def remove_bits(self, n: int) -> "SubnetMask":
        added_ip = ""
        for bit in self.convert_to_binary()[::-1]:
            if bit == "1":
                if n > 0:
                    bit = "0"
                    n -= 1
            added_ip += bit
        if n > 0:
            raise ValueError("Can't remove bits to subnet mask")
        return SubnetMask(added_ip[::-1], bin=True)
    
    def get_subnetting_octet(self) -> int:
        for i in range(len(self.octets)):
            if int(self.octets[i]) != 0 and int(self.octets[i]) != 255:
                return i
        raise ValueError("Can't use this subnet mask for subnetting")
    
    def convert_to_cidr(self) -> int:
        ones = 0
        for bit in self.convert_to_binary():
            if bit == "1":
                ones += 1
        return ones


def logicAND(a: IP, b: IP) -> IP:
    logic_and_octets = []
    a_bin_octets = a.convert_to_binary().split(".")
    b_bin_octets = b.convert_to_binary().split(".")

    for i in range(4):
        logic_and_octets.append(bin(int(a_bin_octets[i], 2) & int(b_bin_octets[i], 2))[2:])
    
    return IP(".".join(logic_and_octets), bin=True)


def logicOR(a: IP, b: IP) -> IP:
    logic_or_octets = []
    a_bin_octets = a.convert_to_binary().split(".")
    b_bin_octets = b.convert_to_binary().split(".")

    for i in range(4):
        logic_or_octets.append(bin(int(a_bin_octets[i], 2) | int(b_bin_octets[i], 2))[2:])
    
    return IP(".".join(logic_or_octets), bin=True)


def bits(n: int) -> int:
    if n < 0:
        raise ValueError("Only non-negative integers supported")
    if n == 0:
        return 1
    # return math.floor(math.log2(n)) + 1
    return math.ceil(math.log2(n))