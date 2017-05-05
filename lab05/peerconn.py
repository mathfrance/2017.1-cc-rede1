# coding=utf-8

import socket
import struct
import threading
import traceback


class PeerConnection:

    def __init__(self, peer_id, host, port, sock=None, debug=True):
        # quaisquer exceções serão lançadas para cima

        self.id = peer_id
        self.debug = debug

        if not sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, int(port)))
        else:
            self.sock = sock

        self.sd = self.sock.makefile('rw', 0)

    @staticmethod
    def __make_msg(msg_type, msg_data):
        msg_len = len(msg_data)
        msg = struct.pack("!4sL%ds" % msg_len, msg_type, msg_len, msg_data)
        return msg

    def __debug(self, msg):
        if self.debug:
            """ Prints a messsage to the screen with the name of the current thread """
            print "[%s] %s" % (str(threading.currentThread().getName()), msg)

    def send_data(self, msg_type, msg_data):
        """
        send_data( message type, message data ) -> boolean status
        
        Enviar uma mensagem através de uma conexão peer. 
        Retorna True em caso de sucesso ou False se houver um erro.
        """

        try:
            msg = self.__make_msg(msg_type, msg_data)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return False
        return True

    def recv_data(self):
        """
        recv_data() -> (msg_type, msg_data)

        Receber uma mensagem de uma conexão peer. 
        Retorna (None, None) se houver algum erro.
        """

        try:
            msg_type = self.sd.read(4)
            if not msg_type:
                return None, None

            len_str = self.sd.read(4)
            msg_len = int(struct.unpack("!L", len_str)[0])
            msg = ""

            while len(msg) != msg_len:
                data = self.sd.read(min(2048, msg_len - len(msg)))
                if not len(data):
                    break
                msg += data

            if len(msg) != msg_len:
                return (None, None)

        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return None, None

        return msg_type, msg

    def close(self):
        """
        close()

        Feche a conexão peer.
         Os métodos send e recv não funcionarão após esta chamada
        """

        self.sock.close()
        self.sock = None
        self.sd = None

    def __str__(self):
        return "|%s|" % self.id
