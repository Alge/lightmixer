
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn = s.connect(("127.0.0.1", 9001))

message = """
    name("hej")
    repeat(10)
    for(n = 0; n<1; n++){
        instruction(0,n,100, now, 4000)
    }

    wait(2000)
    for(n = 5; n<10; n++){
        instruction(0,n,100, now, 4000)
    }

/*
    wait(2000)

    for(n = 0; n<1; n++){
        instruction(0,n,50, now, 4000)
    }
    wait(2000)
    for(n = 5; n<10; n++){
        instruction(0,n,25, now, 4000)
    }

    */
    """

message = message.encode()

s.send(message)
#s.close()




