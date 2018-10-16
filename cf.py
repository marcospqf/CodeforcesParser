#!/usr/bin/env python3
import sys
import os
import os.path
import argparse
import re
from robobrowser import RoboBrowser
import cf_contest
import cf_login
import click

def submit(args):
    problem, filename = args
    if os.path.isfile(filename) :
        user = cf_login.User()
        user.login()
        contest = cf_contest.Contest(user)
        contest.submit(problem, filename)
    else: 
        click.echo('This filepath does not exists')

def change_user_info():
    user = cf_login.User()
    user.change_user_info()

def change_user_contest():
    user = cf_login.User()
    user.change_contest_info()


@click.command()
@click.option('-s', 'submit_problem', nargs=2)
@click.option('-c', 'change_config', flag_value=True)
@click.option('-cc','change_contest', flag_value=True)
@click.option('-w', 'watch_standings', flag_value = False)
def main(submit_problem, change_config, change_contest, watch_standings):
    if submit_problem: 
        submit(submit_problem)
    if change_config:
        change_user_info()
    if change_contest:
        change_user_contest()
    if watch_standings:
        print(":((((")


    
""" END """ 
if __name__ == "__main__":	
    main()
