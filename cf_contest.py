#!ng/usr/bin/env python3

from getpass import getpass
import argparse
from robobrowser import RoboBrowser
import requests
import json
import time
from requests.exceptions import ConnectionError
import click 

class Contest:
    def __init__(self, user):
        self.browser = user.browser
        self.contestid = user.get_contestid()
        self.user = user;

    def get_submission_data(self):
        req = requests.get('http://codeforces.com/api/user.status?handle={}&from=1&count=1'.format(self.user.get_user()))
        content = req.content.decode()
        data = json.loads(content)
        if 'status' not in data or data['status'] != 'OK':
            click.secho('Connection Error" :(((((( !', fd = 'red')
            return
        res = data['result'][0] 
        if 'verdict' not in res:
            res['verdict'] = 'IN QUEUE'
        return res['id'], res['problem'], res['verdict'], res['passedTestCount'], res['timeConsumedMillis'], res['memoryConsumedBytes']

    def GetCountDownTimer(self):
        self.browser.open('http://codeforces.com/contest/{}/submit'.format(self.contestid) )
        timer =  self.browser.parsed.find_all('span', class_='contest-state-regular countdown before-contest-{}-finish'.format(self.contestid))
        if(len(timer)> 0):
            return str(timer[0].get_text(strip=True))
        return '0'

    def watch(self):
        cnt =0
        while cnt < 50:
            id_, probject, verdict, passedTests, timeCon, memCon = self.get_submission_data()
            problem = str(probject['contestId'])+str(probject['index'])
            if verdict != 'TESTING' and verdict != 'IN QUEUE':
                if verdict != 'OK': 
                    click.secho('Subimission {} to problem {} has {} on test {}'.format(str(id_), problem, verdict, str(1 + passedTests) ), fg ='red') 
                    click.secho('Time: {} ms'.format(str(timeCon)), fg = 'red')
                    click.secho("Memory: {} kb".format(str(memCon/1024)), fg= 'red') 
                else:
                    click.secho('Subimission {} to problem {} has passed in all tests \o/!'.format(str(id_), problem),fg = 'green') 
                    click.secho('Time: {} ms'.format(str(timeCon)), fg = 'green')
                    click.secho("Memory: {} kb".format(str(memCon/1024)), fg= 'green') 
                break
            else:
                if(verdict=='TESTING'):
                    click.secho('Testing.....', fg = 'yellow')
                else: 
                    click.secho('In Queue.....', fg = 'blue')
                time.sleep(0.25)
                cnt+=1

    def submit(self, problem, source):
        click.secho('Submiting to problem {} as [{}]'.format(problem.upper(), self.user.get_user()) , fg = 'blue')
        self.browser.open('http://codeforces.com/contest/{}/submit/{}'.format(self.contestid, problem.upper()) )
        submission = self.browser.get_form(class_='submit-form')
        if submission is None:
            click.secho('Cannot find problem', fg = 'red')
            return
        langcode = self.user.get_langcode()
        submission["programTypeId"] = langcode
        try:                   
            submission['sourceFile'] = source 
        except Exception as e:
            click.secho('File {0} not found in current directory'.format(filename))
            return
        self.browser.submit_form(submission)
        if self.browser.url[-3:]!= '/my':
            click.secho('Failed to submit the code. Probably you have submitted it before')
        else:
            timer = self.GetCountDownTimer()
            click.secho('TIME LEFT: ' + timer, fg = 'green')
            self.watch()
