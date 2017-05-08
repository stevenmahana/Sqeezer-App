#!flask/bin/python
# -*- coding: utf8 -*-
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

import os
import json
import time
import datetime
import unittest
from wsgi import app
from random import randint
from config import TestingConfig
from config import ProductionConfig
from werkzeug.security import gen_salt
from simpleflake import simpleflake, parse_simpleflake
from src.resource.models import User, Client

basedir = TestingConfig.BASE_PATH

class TestSqeezer(unittest.TestCase):
    """
    Tests:
     - Test CRUD on the User Table Only. Does not test registration
    """

    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        # we have a build script in search method
        pass

    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass

    # code that is run before each test
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # code that is run after each test
    def tearDown(self):
        pass

    @staticmethod
    def get_id():
        uid = simpleflake()
        p = parse_simpleflake(uid)
        s = simpleflake(timestamp=p[0], random_bits=6768802, epoch=p[1])
        return str(s)

    # test user table CRUD
    def test_user_table(self):

        """
        User().tear_down()  # drop the table
        User().build()  # build the table

        old_user = {
            "UUID": "12312992031208589474",
            'name': 'test testington',
            'username': 'testington',
            "email": "steve@sceene.com",
            'phone': '123.456.789',
            'password': 'call911',
            'public_key': gen_salt(40),
            'confirmation_token': str(randint(1000, 9999))
        }

        User().create_new_user(old_user)
        """

        test_user = {
            'UUID': '1111',
            'name': 'test tester',
            'username': 'tester',
            'phone': '123.456.789',
            'email': 'test@test.com',
            'password': '123456789456',
            'public_key': gen_salt(40),
            'confirmation_token': str(randint(1000, 9999))
        }

        print('>>> User Test Start <<<')
        print()

        # build source list
        users = []
        for u in User.query.all():
            user = u.__dict__
            del user['_sa_instance_state']
            users.append(user)

        print('build_user_list')
        assert isinstance(users, list)
        assert len(users) >= 1
        print(len(users))
        print()

        if len(users) >= 1:
            # backup to file
            _out = ProductionConfig.BASE_PATH + '/tmp/users.txt'
            with open(_out, 'w', encoding='utf-8') as outfile:
                json.dump(users, outfile, sort_keys=True, indent=2)
            print('backup_to_file_success')
            print()

        User().tear_down()  # drop the table
        print('drop_table_success')

        User().build()  # build the table
        print('build_table_success')
        print()

        if len(users) >= 1:

            # rebuild data
            User().add_new_user_list(users)

            # try searching for the user to ensure database was rebuilt
            check_user = User.query.filter_by(email=users[0]['email']).first()
            users = User.query.all()
            print('check_old_user')
            assert check_user in users
            print()
        return
        # add single user/ expect a row count = 1
        User().create_new_user(test_user)
        print('add_new_user')
        print()

        # try searching for the user we just added
        check_single_user = User.query.filter_by(email=test_user['email']).first()
        print('check_new_user')
        all_users = User.query.all()
        assert check_single_user in all_users
        print()

        # create duplicate user / expect a row count = 0
        duplicate_user = User().create_new_user(test_user)
        print('duplicate_user')
        assert duplicate_user is None
        print()

        # delete a user / expect a row count = 1
        delete_user = User().remove_user(test_user['UUID'])
        print('delete_new_single_user')
        assert isinstance(delete_user, bool)
        assert delete_user is True
        print(delete_user)
        print()

        print('table left whole with dataset in place')
        print('>>> User Test Complete <<<')



if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("\nHTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
