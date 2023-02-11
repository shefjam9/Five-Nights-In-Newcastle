import networkzero as nw0

address = nw0.advertise("hello")
while True:
    name = nw0.wait_for_message_from(address)
    nw0.send_reply_to(address, "Hello " + name)