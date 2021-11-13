from cryptography.substitution_cipher import SubCipher
from cryptography.caesars_cipher import Caesar
from cryptography.vigenere_cipher import Vigenere

# my_cyper = SubCipher(key='2tnZlQT&*r7OcYvUJC:jS+!iM@#}\n\rb;`EdGx/y6R_L{uzX3=%AK>NHP )kB$"-g8[m9os|.\'0F]eV?w\th\x0bp14\\~,qDW5(^a<\x0cfI')
# enc = my_cyper.encrypt("my encryption is working")
# dec = my_cyper.decrypt(enc)
# print(f"substitution_cipher:\n {enc}\n{dec}")

# cesar = Caesar(shift=1)
# enc = cesar.encrypt("abcd")
# dec = cesar.decrypt(enc)
# print(cesar.shift)

from protocol.messages import client, server

my_cyper = Vigenere(key="password")
print(my_cyper.encrypt("testing"))

messages = [
    client.connect("matej", "kodermac"),
    client.disconnect(),
    client.send("testing"),
    client.get_messages(),
    client.get_users(),
]

for i in messages:
    msg = i.decode()
    msg_enc = my_cyper.encrypt(msg)
    print(f"{msg_enc.encode()} -> {my_cyper.decrypt(msg_enc)[1]}")
