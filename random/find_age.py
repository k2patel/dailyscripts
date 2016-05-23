#!/usr/bin/env python
# Find your age based on no. of sloka in Bhagvad Gita.
# Total no. of sloka (115)
# This mechanism true till you are at age of 115
import sys
import argparse

parser = argparse.ArgumentParser(prog='find_age')
parser.add_argument('-n', '--name', dest='name', type=str, help='Enter your name', required=True)
parser.add_argument('-b', '--born', dest='born', type=int, help='Enter birth year', required=True)

args = parser.parse_args()

name = args.name
born_year = args.born
age = 115 - born_year

print 'Hello '+name + ', your age is ' + str(age) + '.'