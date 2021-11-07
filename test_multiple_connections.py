from ChatClient.chat_client import ChatClient
import time

user_names = ["liam", "noah", "oliver", "william", "elijah", "james", "benjamin", "lucas", "john"]

client_c = []
for i in user_names:
    c = ChatClient(username=i, password=i)
    client_c.append(c)

count = 0

for i in client_c:
    i.connect()
    # i.get_messages()
    i.get_user_data()
    
    i.send(f"{count} testing ...")
    print(f"{count} connection client...")
    count += 1
    time.sleep(1)

for i in client_c:
    i.disconnect()
    print(f"{count} disconnect client...")
    count -= 1
    time.sleep(1)