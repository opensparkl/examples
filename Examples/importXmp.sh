#!/bin/bash

# The script connects and logs you in to SPARKL before copying the files
# It takes the arguments:
# URL - The URL that points at your instance of the Developer Console
# USER - Your username
# PASSWORD -  Your password

URL=$1
USER=$2
PASSWORD=$3

echo Logging in to ${URL} as ${USER}

sparkl connect ${URL}
sparkl login ${USER} ${PASSWORD}

echo Copying SPARKL configurations to the Scratch folder

sparkl put Discounts/DiscountsCalendar.xml Scratch
sparkl put EventLogger/Event_logger.xml Scratch
sparkl put FilteredVibrations/FilteredVibrations.xml Scratch
sparkl put HelloWorld/hello_world.xml Scratch
sparkl put Phidgets1/Phidgets1.xml Scratch
sparkl put Phidgets2/Phidgets2.xml Scratch
sparkl put Phidgets3/Phidgets3.xml Scratch
sparkl put PrimesExpr/Primes_expr.xml Scratch
sparkl put PrimesTabserver/Primes_tabserver.xml Scratch
sparkl put Robot/Robot.xml Scratch
sparkl put SecretSanta/SecretSanta.xml Scratch
sparkl put StockPortfolio/StockPortfolio.xml Scratch
sparkl put StockSMS/StockSMS.xml Scratch
sparkl put TinyTableExpr/TinyTable_expr.xml Scratch
sparkl put TinyTableTabserver/TinyTable_tabserver.xml Scratch
sparkl put TrafficLightsExpr/TrafficLightsExpr.xml Scratch
sparkl put TrafficSubr/Traf_Lig_Subr.xml Scratch
sparkl put TransactionLock/TransLock.xml Scratch
sparkl put TransportMeta/TransportMeta.xml Scratch
sparkl put VibrationAlerts/VibrationAlerts.xml Scratch

sparkl logout
sparkl close