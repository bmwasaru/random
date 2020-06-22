#!/usr/bin/env bash
# this is handing if you say have clone many repos in a single directory and want to do a git pull on all the repos

for i in */.git; do ( echo $i; cd $i/..; git pull; ); done
