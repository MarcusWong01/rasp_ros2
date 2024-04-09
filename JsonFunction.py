import json

def load_json():
    output_file = 'runs/predictions.json'
    return open(output_file, 'a')

def writeJson(outfile,bboxes):
    # Serializing json
    json_object = json.dumps(bboxes, indent=4)
    # Writing to sample.json
    outfile.write(json_object)
    outfile.write('\n')  # Add a newline between predictions from different frames