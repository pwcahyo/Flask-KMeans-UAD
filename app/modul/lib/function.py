def convertNumerictoAlphabet(listNumeric):
	dictAlphabet = {}
	for x, y in zip(range(1, 27), string.ascii_lowercase):
		dictAlphabet[x] = y

	alpha_list = []
	for i in listNumeric:
		alpha_list.append(dictAlphabet[int(i.encode('utf8'))])

	alphabet = ",".join(alpha_list)

	return alphabet