__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

nl = "\n"
def a( string ): return nl+string
def createComment( comment, dash="-", l="/", r="/", leftCentered=False):
    dashes = (35-len(comment)/2)*dash
    if len(comment) % 2 == 0: comment+=dash
    if leftCentered:
        return l+"** "  + comment + 2*dashes + " **"+r 
    return l+"** " + dashes + "" + comment + "" + dashes + " **"+r 
def createSectionHeader( comment, description=None ):
    rv = createComment("", dash="=", r="\\")
    rv += a(createComment(" " + comment + " ", l="|", r="|"))
    if description is not None:
        rv += a(createComment("", l="|", r="|", dash="%"))
        rv += a(createComment(" Description ", l="|", r="|", dash="."))
	acc = ""
	for w in description.split(" "):
	    if len( w + acc ) > 70:
                rv += a(createComment(acc, l="|", r="|", dash=" ", leftCentered=True))
		acc = ""
	    acc += w + " "
        rv += a(createComment(acc, l="|", r="|", dash=" ", leftCentered=True))
        rv += a(createComment("", l="|", r="|", dash="%"))
    rv += a(createComment("", dash="=", l="\\"))
    return nl + rv + nl
def createRobotHeader( name ):
    rv = createComment(" Robot Name ", dash="#", r="\\") 
    rv += a(createComment("*"*len(name), dash="~", l="|", r="|"))
    rv += a(createComment("/"+" "*(len(name))+"\\", dash="~", l="|", r="|"))
    rv += a(createComment("{ "+name+" }", dash="=", l="|", r="|"))
    rv += a(createComment("\\"+" "*(len(name))+"/", dash="~", l="|", r="|"))
    rv += a(createComment("*"*len(name), dash="~", l="|", r="|"))
    rv += a(createComment("["*(len(name)/2) +"^_^"+ "]"*(len(name)/2), dash="#", l="\\")) 
    return rv
