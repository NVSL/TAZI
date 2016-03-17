import subprocess
popen_args = { "shell" : True, "stdout" : subprocess.PIPE }
class ProgramStatus:
    def ensureProgramExists( f ):
        def decorator( self, *args ):
    	    if self.program is None: 
	        raise Exception("Tried to run an empty program!")
	    return f(self,*args)
        return decorator
    def __init__( self, name="No program loaded", program=None ):
        self.name = name
	self.program = program 
    @ensureProgramExists
    def run( self ):
	self.proc = subprocess.Popen([self.program], **popen_args)
    @ensureProgramExists
    def kill( self ):
        self.proc.kill()
    @ensureProgramExists
    def read_stdout(self):
        return self.proc.stdout.read()
