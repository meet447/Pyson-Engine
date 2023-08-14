import json

def pyson_parser(txt):
    # Read the script.txt file
    with open(txt, "r") as file:
        lines = file.readlines()
        print(lines)
        
        
    
pyson_parser(txt="scene.txt")