"""
    Main CLI tool for the project
"""

import argparse
import os
import sys
import time
import logging
import json
import requests
import os

def showNotification(message, title="42CE", subtitle="Notification",sound="default"):
    titlePart = ''
    if (not title is None):
        titlePart = 'with title "{0}"'.format(title)
    subtitlePart = ''
    if (not subtitle is None):
        subtitlePart = 'subtitle "{0}"'.format(subtitle)
    soundPart = ''
    if (not sound is None):
        soundPart = 'sound name "{0}"'.format(sound)
        
    appleScriptNotify = 'display notification "{0}" {1} {2} {3}'.format(message, titlePart, subtitlePart, soundPart)
    os.system("osascript -e '{0}'".format(appleScriptNotify))

def check_evaluation(value):
    if not value:
        raise argparse.ArgumentTypeError("\033[31m[ERROR]:\033[0m Evaluator name is required")

def main():
    parser = argparse.ArgumentParser(prog="42CE", description="42CE is the CLI tool for the 42 Correction Enviroment project", add_help=True)
    
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")
    parser.add_argument("--login", help="Login to 42CE CLI with your 42 credentials", action="store_true")
    parser.add_argument("--start-evaluation", help="Start an evaluation for a project", nargs=2, metavar=("evaluator_name"), type=check_evaluation)
    parser.add_argument("-l", "--list", help="List all the evaluations you have", action="store_true")

    args = parser.parse_args()
    
    if args.login:
        showNotification("Login to 42CE CLI with your 42 credentials", "42CE", "Login")
        
        
        
if __name__ == "__main__":
    main()