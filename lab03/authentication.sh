#!/bin/bash

# see in: http://stackoverflow.com/a/36296872

# Asks for a username and password, then spits out the encoded value for
# use with authentication against SMTP servers.

echo -n "Email (shown): "
read email
echo -n "Password (hidden): "
read -s password
echo

TEXT="\0$email\0$password"

echo -ne $TEXT | base64
