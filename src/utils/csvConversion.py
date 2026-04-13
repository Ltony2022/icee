def csv_to_arrays(csv_file):
    csv = load_file(csv_file)
    lines = csv.split("\n")
    result = []
    for line in lines:
        if line == "":
            continue
        result.append(line.split(","))
    return result


def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Return a dictionary of the csv data
def csv_to_json(csv_file):
    csv = load_file(csv_file)
    lines = csv.split("\n")
    result = []
    headers = lines[0].split(",")
    for line in lines[1:]:
        if line == "":
            continue
        obj = {}
        values = line.split(",")
        for i in range(len(headers)):
            obj[headers[i]] = values[i]
        result.append(obj)
    return result
