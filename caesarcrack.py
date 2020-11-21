#!/usr/bin/python2

import optparse
import os

class colors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	END = '\033[0m'

class status:
	SUCCESS = colors.GREEN+'[+]'+colors.END
	INFO = colors.YELLOW+'[!]'+colors.END
	FAIL = colors.RED+'[-]'+colors.END

def decipher(textFile, key):
	with open(textFile) as infile:
		cipherText = infile.read().replace('\n','')
	cipherASCII = [ord(c) for c in cipherText]
	plainText = ""
	for c in cipherASCII:
		if c >= ord('a') and c <= ord('z'):
			c -= key
			if c < ord('a'):
				c += 26
		if c >= ord('A') and c <= ord('Z'):
			c -= key
			if c < ord('A'):
				c += 26
		plainText += chr(c)
	return plainText

def encipher(textFile, key):
	with open(textFile) as infile:
		plainText = infile.read().replace('\n','')
	plainASCII = [ord(c) for c in plainText]
	cipherText = ""
	for c in plainASCII:
		if c >= ord('a') and c <= ord('z'):
			c += key
			if c > ord('z'):
				c -= 26
		if c >= ord('A') and c <= ord('Z'):
			c += key
			if c > ord('Z'):
				c -= 26
		cipherText += chr(c)
	return cipherText

def getChi(text):
	lFreq = {'A':8.55,'B':1.60,'C':3.16,'D':3.87,'E':12.20,'F':2.18,'G':2.09,'H':4.96,'I':7.33,'J':0.22,'K':0.81,'L':4.21,'M':2.53,'N':7.17,'O':7.47,'P':2.07,'Q':0.10,'R':6.33,'S':6.73,'T':8.94,'U':2.68,'V':1.06,'W':1.83,'X':0.19,'Y':1.72,'Z':0.11}
	chi = 0
	for letter in lFreq:
		x = len(text) * (lFreq[letter] / 100)
		chi += ((text.count(letter) - x) ** 2) / x
	return chi

def brute(textFile, outFile):
	i = 0
	bestChi = 0
	bestKey = 0
	while i < 26:
		maybePlain = decipher(textFile, i)
		maybePlain = maybePlain.replace(' ','')
		maybePlain = maybePlain.upper()
		chi = getChi(maybePlain)
		if bestChi == 0 or chi < bestChi:
			bestChi = chi
			bestKey = i
		i += 1
	print status.SUCCESS+" key found: "+str(bestKey)+"."
	return decipher(textFile, bestKey)

def main():
	parser = optparse.OptionParser('Usage ./caesarcrack.py -f <file> -k <key> -o <output> -d <decipher> -e <encipher>')
	parser.add_option('-f', dest='textFile')
	parser.add_option('-k', dest='key')
	parser.add_option('-o', dest='outFile')
	parser.add_option('-d', dest='decipher', action='store_true', default=False)
	parser.add_option('-e', dest='encipher', action='store_true', default=False)
	(options, args) = parser.parse_args()

	if options.textFile == None:
		print parser.usage
		exit(0)
	if not os.path.isfile(options.textFile):
		print status.FAIL+" Textfile does not exist."
		exit(0)
	if not os.access(options.textFile, os.R_OK):
		print status.FAIL+" Cannot read textfile."
		exit(0)

	if options.outFile:
		if os.path.isfile(options.outFile):
			print status.FAIL+" File already exists."
			exit(0)
		outPath = os.path.split(options.outFile)[0]

		if outPath:
			if not os.path.isdir(outPath):
				print status.FAIL+" Directory does not exist."
				exit(0)
		if not outPath:
			outPath = "."
		if not os.access(outPath, os.W_OK):
			print status.FAIL+" Cannot write outfile."
			exit(0)

	if options.key != None:
		try:
			key = int(options.key)
		except:
			print status.FAIL+" Key must be an integer between 0 and 26."
			exit(0)
		if key < 0 or key > 26:
			print status.FAIL+" Key must be an integer between 0 and 26."
			exit(0)

	if options.decipher == True and options.encipher == False:
		if options.key != None:
			print status.SUCCESS+" Deciphering using key: "+options.key+"."
			plainText = decipher(options.textFile, int(options.key))
			print plainText
			f = open(options.outFile, 'w')
			f.write(plainText)
			f.close()
		if options.key == None:
			print status.INFO+" No key provided. Brute forcing key."
			plainText = brute(options.textFile, options.outFile)
			print plainText
			if options.outFile:
				f = open(options.outFile, 'w')
				f.write(plainText)
				f.close()

	if options.encipher == True and options.decipher == False:
		if options.key != None:
			print status.SUCCESS+" Enciphering using key: "+options.key+"."
			cipherText = encipher(options.textFile, int(options.key))
			print cipherText
			if options.outFile:
				f = open(options.outFile, 'w')
				f.write(cipherText)
				f.close()
		if options.key == None:
			print status.FAIL+" Must provide a key to encipher."
			exit(0)

	if (options.encipher == True and options.decipher == True):
		print status.FAIL+" Cannot encipher and decipher."
		exit(0)
	if (options.encipher == False and options.decipher == False):
		print status.FAIL+" Must encipher or decipher."
		exit(0)

if __name__ == '__main__':
	main()
