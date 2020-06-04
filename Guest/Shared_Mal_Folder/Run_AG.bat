:loop
	ping -n 2 8.8.8.8 | find /I "Lost = 0"  
	if %errorlevel% == 0 goto OK
	timeout 2
	goto loop
:OK
Z:
AG_ActionMaker.py