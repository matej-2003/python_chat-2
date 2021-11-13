from cryptography import Crypto, VEREFICATION_KEY, CHARS, verify_string

class Vigenere(Crypto):
	"""
	The Vigenère cipher (French pronunciation: ​[viʒnɛːʁ]) is a method of encrypting
	alphabetic text by using a series of interwoven Caesar ciphers, based on the
	letters of a keyword. It employs a form of polyalphabetic substitution.[1][2]
	source: https://en.wikipedia.org/wiki/Vigenère_cipher
	"""
	def __init__(self, key="a"):
		self.key = key

	def encrypt(self, text):
		text = VEREFICATION_KEY + text
		encrypted_text = ""
		for i, e in enumerate(text):
			# get the index of the letter from the text than use % with length of the key
			letter_from_key = self.key[i % len(self.key)]

			# shit if the index from the letter_from_key CHARS
			shift = CHARS.index(letter_from_key)

			#new letter index is the index of the letter itself + the shif value
			new_index = (CHARS.index(e) + shift) % len(CHARS)
			encrypted_text += CHARS[new_index]
		return encrypted_text

	def decrypt(self, encrypted_text):
		text = ""
		for i, e in enumerate(encrypted_text):
			letter_from_key = self.key[i % len(self.key)]
			shift = CHARS.index(letter_from_key)

			new_index = (CHARS.index(e) - shift) % len(CHARS)
			text += CHARS[new_index]
		return verify_string(text)