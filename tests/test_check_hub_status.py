#!/usr/bin/python3

import unittest
import check_hub_status as chs

class TestCode(unittest.TestCase):

    def setUp(self):
        self.hubline1 = ['   HubName   ', '  dchub://10.20.30.400:123\n']

    def test_getHubData(self):
        [name, protocol, ip, port] = chs.getHubData(self.hubline1)
        self.assertEqual('HubName', name)
        self.assertEqual('dchub', protocol)
        self.assertEqual('10.20.30.400', ip)
        self.assertEqual('123', port)


# if __name__ == '__main__':
#     unittest.main()

