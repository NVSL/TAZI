############################# Decorators ############################# 
def ensureXExists(errorMsg, X):
    def decorator(f):
        def decorated( self, *args ):
    	    if self.__dict__[X] is None: 
	        raise Exception("Tried to " + errorMsg + " an empty " + X)
	    return f(self,*args)
	return decorated
    return decorator
def ensureProgramExists( errorMsg ):
    return ensureXExists( errorMsg, "program" )
def ensureProcessExists( errorMsg ):
    return ensureXExists( errorMsg, "proc" )
