import json
import os

resource_dir = "Resources"

blocks_file = os.path.join( resource_dir, "_Blocks.json" )
blocks_out_file = os.path.join( resource_dir, "Blocks.json" )



# Open the file
blocks_fd = open(blocks_file) # File Descriptor
blocks = json.load(blocks_fd)

# Close the file so we can write to it later
blocks_fd.close()
print type(blocks)


#for key,value in blocks.items():
#    print key

for element in blocks["DistanceSensor"]:
    print element.keys()
    element["message0"] += " (cm) " 
    print element["message0"]

# Write the blocks to the resource file
blocks_fd = open(blocks_out_file,"w+" ) # File Descriptor
json.dump(blocks, blocks_fd)
blocks_fd.close()
