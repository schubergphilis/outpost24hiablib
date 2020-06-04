import unittest
import logging
import logging.config
import sys
import os
from configparser import ConfigParser
import outpost24hiablib
from outpost24hiablib import Outpost24

class Test_Outpost24lib(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig('logging.conf')
        logger = logging.getLogger('simple')
        mode = os.environ["SYNC_MODE"]
        config = ConfigParser()
        config.read('config.ini')
        
        if mode not in config:
            logger.error("Please set SYNC_MODE environment variable to 'production' or 'acceptance' according to 'config.ini'")
            sys.exit(1)

        op24_url = config[mode]['op24_url']
        op24_token = os.environ['OP24_TOKEN']
        self.op24lib = Outpost24(op24_url, op24_token)

    @unittest.skip("Skip - remove this line if you have an Outpost24 HIAB test instance")
    def test_Users(self):
        usergroups = self.op24lib.get_usergroups()
        user = self.op24lib.create_user("testuser123_firstname", "testuser123_lastname", "testuser123@testuser123.com", "612950589", "nl", "testuser123", "testuser123password@#", usergrouplist = [usergroups[0]], allscanners = True)
        isdeleted = self.op24lib.delete_users([user])

        self.assertEqual(user.vcfirstname, 'testuser123_firstname')
        self.assertEqual(user.vclastname, 'testuser123_lastname')
        self.assertEqual(user.vcusername, 'TESTUSER123')
        self.assertTrue(isdeleted)
       
    @unittest.skip("Skip - remove this line if you have an Outpost24 HIAB test instance")
    def test_Targets(self):
        targetgroup = self.op24lib.get_targetgroups()[0]
        scanner = self.op24lib.get_scanners()[0]
        tg = ["test.outpost24.com"]
        targets = self.op24lib.create_targets(tg, targetgroup, False, scanner)
        isdeleted = self.op24lib.delete_targets(targets)

        self.assertEqual(targets[0].hostname, 'test.outpost24.com')
        self.assertTrue(isdeleted)

    @unittest.skip("Skip - remove this line if you have an Outpost24 HIAB test instance")
    def test_Targetgroups(self):
        targetgroup = self.op24lib.create_targetgroup("test1")
        isdeleted = self.op24lib.delete_targetgroups([targetgroup])
        
        self.assertEqual(targetgroup.name, 'test1')
        self.assertTrue(isdeleted)

if __name__ == '__main__':
    unittest.main()
