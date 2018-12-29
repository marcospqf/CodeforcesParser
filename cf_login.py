#! /usr/bin/env python3

from getpass import getpass
import argparse
from robobrowser import RoboBrowser
import requests
import json
import time
from requests.exceptions import ConnectionError
import click 
from pathlib import Path
import os
class User:
    def __init__(self):
        self._jsonpath = os.path.dirname(os.path.realpath(__file__)) + '/user_info.json'
        self._username, self._password, self._langcode, self._contestid = self._dump_data()
        self.browser = RoboBrowser(parser = 'html5lib')
    def _dump_data(self):
        with open(self._jsonpath, 'r') as f:
            data = json.load(f)
        return data['username'],data['password'],data['langcode'], data['contestid']
    
    def get_user(self):
        return self._username

    def get_langcode(self):
        return self._langcode

    def get_contestid(self):
        return self._contestid

    def change_user_info(self):
        self._username = input("Enter your codeforces username: ")
        self._password = input("Enter your codeforces password: ")
        self._langcode = input("Enter your codeforces langcode, C++11= 50, C++14 = 54: ")
        self._contestid = input("Enter the contest id: ")

        with open(self._jsonpath, 'w') as f:
            json.dump({'username':self._username, 'password':self._password, 'langcode':self._langcode, 'contestid':self._contestid}, f, indent=4)
        f.close()
        
    def change_contest_info(self):
        with open(self._jsonpath, 'r') as f:
            data = json.load(f)
        self._contestid = input("Enter the contest id: ")
        f.close()

        data['contestid'] = self._contestid
        with open(self._jsonpath, 'w') as f:
            json.dump(data, f, indent=4)
     
    def set_contest_info(self):
        with open(self._jsonpath, 'r') as f:
            data = json.load(f)
        f.close()

        data['contestid'] = self._contestid
        with open(self._jsonpath, 'w') as f:
            json.dump(data, f, indent=4)
            

    def login(self):
        self.browser.open('http://codeforces.com/enter')
        enter_form = self.browser.get_form('enterForm')
        enter_form['handleOrEmail'] = self._username
        enter_form['password'] = self._password
        self.browser.submit_form(enter_form)
        try:
            checks = list(map(lambda x: x.getText()[1:].strip(), self.browser.select('div.caption.titled')))
            if self._username not in checks:
                click.secho('Login Failed.. Wrong password.', fg = 'red')
                click.secho('Note that username is case sensitive.', fg = 'red')

                return
        except Exception as e:
            click.secho('Login Failed.. Maybe wrong id/password.', fg = 'red')
            return 
        click.secho('[{0}] login successful! '.format(self._username), fg = 'green')
