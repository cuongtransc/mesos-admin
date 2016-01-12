import re

def convert(data_input):
    data_output = re.sub('\n', ' ', data_input)
    data_output = re.sub('\s+', ' ', data_output)
    data_output = data_output.replace('\\', '\\\\').replace('"', '\\"')
    return data_output
