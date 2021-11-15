from chat_client import ChatClient
from cryptography.caesars_cipher import Caesar
from cryptography.substitution_cipher import SubCipher
from cryptography.vigenere_cipher import Vigenere
import time

def main():
	import sys
	USERNAME = "matej"
	PASSWORD = "kodermac"
	HOST = "127.0.0.1"
	PORT = 5002
	# my_cipher = Caesar(shift=13)
	# my_cipher = SubCipher(key='ryQ>H!Jw\rB#.<NEe9mpX;^~"C}\x0b5G2SWz_Z[3q$|0vIjuP@{8tsl-hFdo\'`:1fkbaDL,)K(7O*/MVUc?\n=Y%\x0cng6\\] +xAT\t&4Ri')
	my_cipher = Vigenere(key="matejkodermac")
	
	cc = ChatClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, encryption=my_cipher)
	cc.connect()

	time.sleep(0.3)
	cc.send("1 testing...")
	time.sleep(0.3)
	cc.send("2 testing...")
	time.sleep(0.3)
	cc.send("3 testing...")
	time.sleep(0.3)
	cc.send("4 testing...")

	print(cc.users, cc.messages)
	time.sleep(0.5)
	cc.disconnect()

if __name__ == "__main__":
	main()
