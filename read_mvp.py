FILEPATH = "/tmp/a.csv"


def main():
	with open(FILEPATH, 'r') as f:
		for line in f:
			print line.split(',')


if __name__ == '__main__':
    main()