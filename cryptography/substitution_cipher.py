from cryptography import Crypto, VEREFICATION_KEY, CHARS, verify_string
import random

class SubCipher(Crypto):
	"""
	SubCipher = substitution cipher
	"""
	
	def __init__(self, key=None, encode=False):
		super().__init__(encode=encode)
		self.key = key
		if not SubCipher.verify_key(key):
			self.key = list(CHARS)
			random.shuffle(self.key)
			self.key = ''.join(self.key)

	def encrypt(self, text):
		text = VEREFICATION_KEY + text
		encrypted_text = ""
		for i in text:
			encrypted_text += self.key[CHARS.index(i)]
		return self.encode_(encrypted_text)

	def decrypt(self, encrypted_text):
		text = ""
		for i in encrypted_text:
			text += CHARS[self.key.index(i)]
		return verify_string(text)

	@classmethod
	def verify_key(cls, key):
		if not not key:
			if len(CHARS) == len(key):
				for e in key:
					if e not in CHARS:
						return False
				return True
		else:
			return False