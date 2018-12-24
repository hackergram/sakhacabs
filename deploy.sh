#!/usr/bin/bash
IP=$1
echo "Setting IP from $1 to $2"
perl -p -i -e "s/$1/$2/g" dispatcher/index.html
perl -p -i -e "s/$1/$2/g" dispatcher/importbookings.html
perl -p -i -e "s/$1/$2/g" dispatcher/managebookings.html
perl -p -i -e "s/$1/$2/g" dispatcher/managevehicles.html
perl -p -i -e "s/$1/$2/g" dispatcher/managedrivers.html
perl -p -i -e "s/$1/$2/g" dispatcher/manageproducts.html
perl -p -i -e "s/$1/$2/g" dispatcher/managecustomers.html
perl -p -i -e "s/$1/$2/g" dispatcher/manageinvoices.html
perl -p -i -e "s/$1/$2/g" bookingweb/index.html
