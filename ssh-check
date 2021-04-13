#!/bin/bash
 
IP=${1}
 
nc -w 1 -z ${IP} 22 &>/dev/null
 
NC_CODE=${?}
 
if [ ${NC_CODE} -eq 1 ]
then
  #echo "${IP}: not listening on port 22"
  exit 0
fi
 
timeout 5 ssh \
  -o PreferredAuthentications=password,keyboard-interactive \
  -o StrictHostKeyChecking=no ${IP} &>/dev/null
 
SSH_CODE=${?}
 
if [ ${SSH_CODE} -eq 124 ]
then
  echo "${IP}: *** accepts a password for ssh logins ***"
  exit 0
fi
 
echo "${IP}: running sshd but is okay (no password methods)"
