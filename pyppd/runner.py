import sys
import compressor

def run():
    output = open("ppds.pkl", "wb")
    output.write(compressor.compress(sys.argv[1]))
    output.close()
