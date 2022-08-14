import json


def parse_json(file):
	file = open(file)
	data = json.load(file)
	file.close()

	return data
