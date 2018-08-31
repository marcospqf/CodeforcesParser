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
        contest = cf_contest.Contest(user)
        contest.submit(problem, filename)
    else: 
        click.echo('This filepath does not exists')


@click.command()
@click.option('-s', 'submit_problem', nargs=2)
@click.option('-c', 'change_user', nargs=2)
@click.option('-w', 'watch_standings', flag_value = False)
def main(submit_problem, change_user, watch_standings):
    if submit_problem: 
        submit(submit_problem)
    if change_user:
        print('TODO: Unfortunately')
    if watch_standings:
        print(":((((")


    
""" END """ 
if __name__ == "__main__":	
    main()
