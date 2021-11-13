import random

CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
KEY_ERROR = "key error"
# VEREFICATION_KEY = str(random.randint(0, 10000))
VEREFICATION_KEY = str(123456789)

	
def generate_key_():
	key = random.shuffle(list(CHARS))
	return ''.join(key)

def gen_key(length=1):
	l = length // len(CHARS)
	r = length % len(CHARS)
	key = ""
	for i in range(l):
		key += random.shuffle(list(CHARS))
	if not not r:
		key += random.shuffle(list(CHARS))[:r]

def verify_string(text):
	for i, e in enumerate(list(VEREFICATION_KEY)):
		if text[i] != e:
			return (KEY_ERROR, text)
	return (None, text[len(VEREFICATION_KEY):])

class Crypto:
	""""
		VEREFICATION_KEY append it to the start of every string and then encrypt it.
		to quickly verify the string after decryption.
	"""
	def __init__(self):
		pass
	
	def encrypt(self, text):
		return text

	def decrypt(self, text):
		return text
	