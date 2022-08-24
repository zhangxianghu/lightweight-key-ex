#!/bin/bash

pip3 install pandas
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
pip3 pycryptodome
