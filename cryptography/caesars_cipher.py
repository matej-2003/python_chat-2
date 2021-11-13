from cryptography import Crypto, VEREFICATION_KEY, CHARS, verify_string
import random

class Caesar(Crypto):
	"""
	Caesar cipher, also known as Caesar's cipher, the shift cipher, Caesar's code or Caesar shift
	"""
	
	def __init__(self, shift=None):
		if not self:
			self.shift = random.randint(0, len(CHARS))
		else:
			self.shift = shift % len(CHARS)

	def encrypt(self, text):
		text = VEREFICATION_KEY + text
		encrypted_text = ""
		for i in text:
			new_index = (CHARS.index(i) + self.shift) % len(CHARS)
			encrypted_text += CHARS[new_index]
		return encrypted_text

	def decrypt(self, encrypted_text):
		text = ""
		for i in encrypted_text:
			new_index = (CHARS.index(i) - self.shift) % len(CHARS)
			text += CHARS[new_index]
		return verify_string(text)