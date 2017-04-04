import os

def execute_command(command_str):
	'''
	Executes the command and returns the output
	'''
	return os.system(command_str)

def beep(vol=1, duration=0.4):
    command = "play -n synth {} sine 800 vol {}".format(duration, vol)
    os.system(command)
