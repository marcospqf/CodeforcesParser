#! /usr/bin/env python3

from getpass import getpass
import argparse
from robobrowser import RoboBrowser
import requests
import json
import time
import user_info
from requests.exceptions import ConnectionError
import click 


class User:
    def __init__(self):
        self._username, self._password, self._langcode, self._contestid = self._dump_data()
        self.browser = RoboBrowser(parser = 'html5lib')
        self.login()

    def _dump_data(self):
        return user_info.username,user_info.password,user_info.langcode, user_info.contestid
    
    def get_user(self):
        return self._username

    def get_langcode(self):
        return self._langcode

    def get_contestid(self):
        return self._contestid

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
                return
        except Exception as e:
            click.secho('Login Failed.. Maybe wrong id/password.', fg = 'red')
            return 
        click.secho('[{0}] login successful! '.format(self._username), fg = 'green')
