import subprocess
from Decorators import *
popen_args = { "shell" : True, "stdout" : subprocess.PIPE }
running = "Running"
not_running = "Not running"
not_loaded = "No program loaded"
class ProgramManager:
    def __init__( self, name=not_loaded, program=None ):
        self.name = name
	self.program = program 
	self.proc = None
	self.status = not_running

    @ensureProgramExists("run")
    def run( self ):
        try: self.kill()
	except: pass
	if self.name == not_loaded: return
	self.proc = subprocess.Popen("exec " + self.program, **popen_args)
	self.status = running
	#print self.proc.__dict__

    @ensureProgramExists("kill")
    @ensureProcessExists("kill")
    def kill( self ):
        self.proc.kill()
	self.status = not_running

    @ensureProgramExists("read from")
    @ensureProcessExists("read from")
    def read_stdout(self):
        return self.proc.stdout.read()

