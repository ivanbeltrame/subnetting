from pytest import raises
from ipv4 import *

def main():
    test_validating()
    test_convert_from_binary()
    test_convert_to_binary()
    test_get_class()
    test_is_private()
    test_is_between()
    test_choose_subnet_mask()
    test_get_inverted()
    test_add()
    test_subtract()
    test_get_subnetting_octet()

def test_validating():
    with raises(ValueError):
        IP("")
        IP("0.0.0")
        IP("a.0.0.0")
        IP("-1.0.0.0")
        IP(".0.0.0")
        IP("0.0.0.256")
        IP("...")
        IP(".0.0.")
        IP("0.0")
    assert str(IP("0.0.0.0")) == "0.0.0.0"
    assert str(IP("0.54.0.0")) == "0.54.0.0"
    assert str(IP("0.64.64.0")) == "0.64.64.0"
    assert str(IP("255.255.255.255")) == "255.255.255.255"

def test_convert_from_binary():
    assert str(IP("00000000.00000000.00000000.00000000", bin=True)) == "0.0.0.0"

def test_convert_to_binary():
    pass

def test_get_class():
    pass

def test_is_private():
    pass

def test_is_between():
    pass

def test_choose_subnet_mask():
    pass

def test_get_inverted():
    pass

def test_add():
    pass

def test_subtract():
    pass

def test_get_subnetting_octet():
    with raises(ValueError):
        SubnetMask("255.255.255.0").get_subnetting_octet()
        SubnetMask("255.0.0.0").get_subnetting_octet()
    assert SubnetMask("255.255.255.5").get_subnetting_octet() == 3
    assert SubnetMask("255.255.55.0").get_subnetting_octet() == 2
    assert SubnetMask("255.90.0.0").get_subnetting_octet() == 1
    assert SubnetMask("192.0.0.0").get_subnetting_octet() == 0

if __name__ == "__main__":
    main()