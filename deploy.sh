#!/usr/bin/bash
IP=$1
echo "Setting IP from $1 to $2"
perl -p -i -e "s/$1/$2/g" dispatcher/index.html
perl -p -i -e "s/$1/$2/g" dispatcher/invoices.html
perl -p -i -e "s/$1/$2/g" dispatcher/importbookings.html
perl -p -i -e "s/$1/$2/g" bookingweb/index.html

