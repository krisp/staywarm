Stay Warm

A python script to issue heater commands at a regular interval to keep a 
CraftBot from going into power-save mode and turning off the heaters before 
it reaches target temperature.

Requires OctoPrint and uses their REST API to query the target temperature 
and issue a temperature set command.

It be called from OctoPrint's event system by adding the lines on config.yaml 
to your ~/.octoprint/config.yaml. My config has it start when a file is loaded
and stop when a print starts.

Stand-alone usage: 

To start:
python staywarm.py 

To stop:
python staywarm.py off

If a start is called while the script is already running, the original will be
killed and the newly started will take over.
