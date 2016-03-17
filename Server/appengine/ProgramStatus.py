import subprocess
from Decorators import *
popen_args = { "shell" : True, "stdout" : subprocess.PIPE }
class ProgramStatus:
    def __init__( self, name="No program loaded", program=None ):
        self.name = name
	self.program = program 
	self.proc = None

    @ensureProgramExists("run")
    def run( self ):
        try: self.kill()
	except: pass
	self.proc = subprocess.Popen("exec " + self.program, **popen_args)
	print self.proc.__dict__

    @ensureProgramExists("kill")
    @ensureProcessExists("kill")
    def kill( self ):
        self.proc.kill()

    @ensureProgramExists("read from")
    @ensureProcessExists("read from")
    def read_stdout(self):
        return self.proc.stdout.read()

