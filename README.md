# nagios-rpi-ledmatrix
Nagios and Rpi Sense Hat Led Matrix integration

The idea of this project is to use RaspberryPi Sense Hat
(https://www.raspberrypi.org/products/sense-hat/) to view the number and status of the alarms of our nagios server.

In this way it is possible to have a first synoptic information of what happens to the services monitored by nagios.

The status of critical services are mapped with red LEDs, warnings with yellow, unknowns with orange and hosts down in blue.

All colors are configurable.

The last row of the matrix (8x8) can be to report other information.


INSTALLATION

Edit the file and set nagios user and  nagios ip.
You can set html file.

This project use nagios4stat command.

Insert in cron this line:
*/2 * * * * user python nagios-rpi-matrix.py > /dev/null

USE

Without parameters, the status of the matrix is updated:
python nagios-rpi.matrix.py


Parameters:

--web create a html file with the matrix state
--view print on screen the matrix state


