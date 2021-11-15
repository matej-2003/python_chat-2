from chat_server.chat_server import ChatServer
from cryptography.caesars_cipher import Caesar
from cryptography.substitution_cipher import SubCipher
from cryptography.vigenere_cipher import Vigenere

if __name__ == '__main__':
	import sys

	SERVER_HOST = "0.0.0.0"     # server's IP address
	SERVER_PORT = 5002
	if len(sys.argv) == 3:
		SERVER_HOST = str(sys.argv[1])
		SERVER_PORT = int(sys.argv[2])
	elif len(sys.argv) == 2:
		SERVER_PORT = int(sys.argv[1])
	else:
		print("""
		Correct ussage:
			'script IP PORT'
			'script IP'
			default port is 5002
		""")
	# my_cipher = Caesar(shift=13)
	# my_cipher = SubCipher(key='ryQ>H!Jw\rB#.<NEe9mpX;^~"C}\x0b5G2SWz_Z[3q$|0vIjuP@{8tsl-hFdo\'`:1fkbaDL,)K(7O*/MVUc?\n=Y%\x0cng6\\] +xAT\t&4Ri')
	my_cipher = Vigenere(key="matejkodermac")

	chat_server = ChatServer(host=SERVER_HOST, port=SERVER_PORT, encryption=my_cipher)
	chat_server.load_user_file("users.csv")
	print([i["username"] for i in chat_server.users])
	chat_server.start()