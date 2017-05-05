# -*- coding: utf-8 -*-
import socket
import threading
import traceback
import time
from peerconn import PeerConnection


def log(msg):
    print msg


class PeerNode(object):
    def __init__(self, server_port, server_host=None, peer_id=None, max_peers=0):
        """
        :param server_port: Porta do servidor que o peer deve ouvir as conexões.
        :param server_host: Endreço do servidor do node.
        :param peer_id: Identificador do peer. Caso não seja definido, será (host:port) do node.
        :param max_peers: Número máximo de peers que esse node é capaz de catalogar. 
        Caso seja definido como 0 pode permitir um número ilimitado de peers.
        """

        self.server_port = server_port
        self.server_host = server_host if server_host is not None else self.__get_server_host()
        self.peer_id = peer_id if peer_id is not None else '%s:%d' % (self.server_host, self.server_port)
        self.max_peers = max_peers

        #
        self.peers = {}  # lista dos peers que esse node conhece.

        # Handles | contém as funções que devem ser executadas a partir do "tipo de messagens" que são definidas
        # para se comportar como o protocolo de comunicação entre os peers.
        self.handlers = {}
        self.router = None

        # Thread | atributo para controle da thread do servidor desse node
        self.shutdown = False  # utilizado para parar a thread principal desse node.
        self.peer_lock = threading.Lock()  # para garantir o acesso adequado à lista de peers

    def set_peer_id(self, peer_id):
        self.peer_id = peer_id

    # --------------------------------------------------------------------------
    @staticmethod
    def __get_server_host():
        """
        Realiza a conexão com um host da Internet para determinar 
        o endereço IP da máquina local.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com", 80))
        return s.getsockname()[0]

    # --------------------------------------------------------------------------
    def add_handler(self, msg_type, handler):
        """
        Registrar o handler para um determinado tipo de mensagem.
        
        :type handler: function
        :param handler: Função para ser executada por determinado handler.
        :type msg_type: str
        :param msg_type: Tipo de mensagem, nome atribuido pelo protocolo de comunicação. Ex: NAME, LIST, QUIT.
        """
        assert len(msg_type) == 4
        self.handlers[msg_type] = handler

    # --------------------------------------------------------------------------
    def add_router(self, router):
        """ 
        Registra uma função de roteamento com este peer. A configuração para a função de roteamento 
        é a seguinte: Este peer mantém uma lista de outros pares conhecidos (em self.peers).
        1) A função de roteamento deve levar o nome de um peer (que pode não estar necessariamente 
        presente em self.peers) e decidir qual dos peer conhecidos uma mensagem deve ser encaminhada 
        a fim de (esperamos) alcançar o peer desejado. 
        3) A função de roteamento deve retornar uma tupla de três valores:  (next-peer-id, host, port). 
        4) Se a mensagem não puder ser encaminhada, o next-peer-id deve ser None.
        
        :type router: function
        """
        self.router = router

    # --------------------------------------------------------------------------
    def add_peer(self, peer_id, host, port):
        """
        Adiciona um peer na lista de peerd conhecidos. O peer será mapeado como peer_id=(host:port)
        
        :type peer_id: str
        :param peer_id: Identificador do peer que deve ser adicionado. 
        :type host: str
        :param host:  Host do peer a ser adicionado.
        :type port: int
        :param port: Porta do peer a ser adicionado.
        :return: bool
        """
        if peer_id not in self.peers and (self.max_peers == 0 or len(self.peers) < self.max_peers):
            self.peers[peer_id] = (host, int(port))
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    def get_peer(self, peer_id):
        """ 
        Retorna a tupla (host, port) para um dado peer.
        
        :type peer_id: str
        :param peer_id: Identificador do peer que deseja obter as informações.
        :return: tuple
        """
        assert peer_id in self.peers
        return self.peers[peer_id]

    # --------------------------------------------------------------------------
    def remove_peer(self, peer_id):
        """ 
        Remove o peer da lista de peers conhecidos.
        
        :type peer_id: str
        :param peer_id: Identificador do peer que deseja remover.
        """
        if peer_id in self.peers:
            del self.peers[peer_id]

    # --------------------------------------------------------------------------
    def get_peer_ids(self):
        """ 
        Retorna uma lista com todos os identificadores dos peers conhecidos.
        
        :rtype list
        """
        return self.peers.keys()

    # --------------------------------------------------------------------------
    def number_of_peers(self):
        """
        Total de peers conhecidos.
        
        :rtype int
        """
        return len(self.peers)

    # --------------------------------------------------------------------------
    def max_peers_reached(self):
        """
        Retorna True se o número max_peers de peers foi adicionado à lista de peers. Sempre retorna True se max_peers 
        estiver definido como 0.
        
        :rtype bool
        """
        assert self.max_peers == 0 or len(self.peers) <= self.max_peers
        return self.max_peers > 0 and len(self.peers) == self.max_peers

    # --------------------------------------------------------------------------
    def send_to_peer(self, peer_id, msg_type, msg_data, wait_reply=True):
        """
        send_to_peer( peer id, message type, message data, wait for a reply )
        -> [ ( reply type, reply data ), ... ] 
        
        Envia uma mensagem para o peer. Para decidir como enviar a mensagem, o router handler 
        para este peer será chamado. Se nenhuma função do router tiver sido registrada, ela 
        não funcionará. A função do router deve fornecer o próximo peer imediato a quem a 
        mensagem deve ser encaminhada. A resposta do peer, se for esperada, será devolvida.

        Retorna None se a mensagem nao puder ser encaminhada.
        """

        host, port = None, None
        if self.router:
            next_pid, host, port = self.router(peer_id)
        if not self.router or not next_pid:
            print 'Unable to route %s to %s' % (msg_type, peer_id)
            return None
        # host,port = self.peers[nextpid]
        return self.connect_and_send(host, port, msg_type, msg_data, pid=next_pid, wait_reply=wait_reply)

    # --------------------------------------------------------------------------
    @staticmethod
    def connect_and_send(host, port, msg_type, msg_data, pid=None, wait_reply=True):
        """
        connect_and_send( host, port, message type, message data, peer id,
        wait for a reply ) -> [ ( reply type, reply data ), ... ]
        
        Conecta e envia uma mensagem para host:port. A resposta do host, 
        se for esperado, será retorna como uma lista de tuplas.
        """
        msg_reply = []
        try:
            peer_conn = PeerConnection(pid, host, port, debug=True)
            peer_conn.send_data(msg_type, msg_data)
            print 'Sent %s: %s' % (pid, msg_type)

            if wait_reply:
                one_reply = peer_conn.recv_data()
                while one_reply != (None, None):
                    msg_reply.append(one_reply)
                    print 'Got reply %s: %s' % (pid, str(msg_reply))
                    one_reply = peer_conn.recv_data()
            peer_conn.close()
        except KeyboardInterrupt:
            raise
        except:
            print "Não é possível conectar e/ou enviar os dados para (%s:%s)" % (host, port)

        return msg_reply

    # --------------------------------------------------------------------------
    def check_live_peers(self):
        """
        Reliza tentativas de fazer ping a todos os peers atualmente conhecidos para 
        garantir que eles ainda estejam ativos. Remove qualquer um da lista os peers que não responde. 
        Esta função pode ser usada como um estabilizador simples, ou seja, ser executa por uma thread
        a cada x segundos.
        """
        pass

    # --------------------------------------------------------------------------
    def mainloop(self):
        s = self.make_server_socket(self.server_port)
        s.settimeout(2)
        print 'peer_node::Servidor inicado: %s (%s:%d)' % (self.peer_id, self.server_host, self.server_port)

        while not self.shutdown:
            try:
                print 'peer_node::Esperando por conexões...'
                client_sock, client_addr = s.accept()
                client_sock.settimeout(None)

                t = threading.Thread(target=self.__handle_peer_messages, args=[client_sock])
                t.start()
            except KeyboardInterrupt:
                print 'peer_node::KeyboardInterrupt: stopping mainloop'
                self.shutdown = True
                continue
            except:
                # Se o timeout do socket expirar dispara uma execeção, no entanto, para a nossa aplicação isso não
                # é um erro, pois esperamos esse comportamento, para não bloquear a porta do socket.
                continue

        # end while loop
        print 'peer_node::Fechando main loop'
        s.close()

    # --------------------------------------------------------------------------
    @staticmethod
    def make_server_socket(port, backlog=5):
        """ 
        Construir e preparar um socket servidor para escutar em uma determinada porta.
        
        :param port: 
        :param backlog: 
        :return: 
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s

    # --------------------------------------------------------------------------
    def __handle_peer_messages(self, client_sock):
        """
        handle_peer_messages( new socket connection ) -> ()

        Dispara mensagens do socket conectado

        :param client_sock: socket do peer conectado
        """

        print "peer_node::__handle_peer"
        print 'peer_node:: New message:', str(threading.currentThread().getName())
        print 'peer_node:: Client connected:', str(client_sock.getpeername())

        # Inica uma conexão com o cliente
        host, port = client_sock.getpeername()
        peer_conn = PeerConnection(None, host, port, client_sock, debug=False)

        try:
            # Recebe a mensagem enviada
            msg_type, msg_data = peer_conn.recv_data()
            # Verifica se o tipo da mensagem pertence ao protocolo de comunicação
            if msg_type:
                msg_type = msg_type.upper()
            if msg_type not in self.handlers:
                print 'Not handled: %s: %s' % (msg_type, msg_data)
            else:
                # Executa o método assinado para determinda messagem
                print 'Handling peer msg: %s: %s' % (msg_type, msg_data)
                self.handlers[msg_type](peer_conn, msg_data)
        except KeyboardInterrupt:
            raise
        except:
            # if self.debug:
            traceback.print_exc()

        print 'Disconnecting ' + str(client_sock.getpeername())
        peer_conn.close()

    # --------------------------------------------------------------------------
    def every(self, stabilizer, delay):
        """ 
        Registra e inicia uma função <stabilizer> com esse peer.
        A função irá ser executada a cada <delay> segundos.
        """
        t = threading.Thread(target=self.__run_function_every, args=[stabilizer, delay])
        t.start()

    # --------------------------------------------------------------------------
    def __run_function_every(self, stabilizer, delay):
        while not self.shutdown:
            stabilizer()
            time.sleep(delay)
