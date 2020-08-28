#!/bin/bash

# This script will delete all user's account that  hasn't been logged in for the past 30 days.

# Make sure that script executes with roor priviligies (OPTIONAL)

if [[ "${UID}" -ne 0 ]]

then
        echo "You should run this script as a root!"
exit 1
fi

# First of all we need to know id limit (min & max)

# Get only numbers from each line

USER_MIN=$(grep -Po "^UID_MIN \K." /etc/login.defs)
USER_MAX=$(grep -Po "^UID_MAX \K." /etc/login.defs)

# Print all users accounts with id>=1000 and <=6000 (default).

# create an associative array, see: help declare
declare -A users
# read all users with its uid to this associative array

while IFS=":"
read -r user x uid x;
do users[$UA]="$uid";
done </etc/passwd

# remove all unwanted lines including headline. NR is line number
lastlog -b 30 | awk '! /*Never logged in*/ && NR>1 {print $1}' |
while read -r user;
do
if [[ ${users[$UA]} -ge $USER_MIN ]] && [[ ${users[$UA]} -le $USER_MAX ]]; then
      echo "delete user $user with uid ${users[$UA]}"
fi
done

# Make a color output
echo -e "\e[36mYou have successfully deleted all user's account which nobody logged in in the past 30 days.\e[0,"
exit 0
