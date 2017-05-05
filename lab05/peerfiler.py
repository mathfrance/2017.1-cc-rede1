# coding=utf-8

from peernode import *

# ===============================
#     Handling Messages
# ===============================

# Quando um peer recebe uma mensagem NAME (e não há dados adicionais), ele simplesmente responde enviando
# de volta (em uma mensagem REPL) com seu peer_id, em uma string com o seguinte formato "host:port".
PEERNAME = "NAME"

# Quando um peer recebe uma mensagem LIST (e sem dados adicionais), ele responde primeiro enviando uma mensagem
# REPL com a quantidade de id's na sua lista de peers. Em seguida, ele envia muitas mensagens REPL adicionais,
# incluindo na parte de dados de cada mensagem uma seqüência de caracteres com o peer id, host e a porta
# (todos os três separados por espaço em branco) associado a cada conhecido peer em sua lista.
LISTPEERS = "LIST"

# Uma mensagem JOIN é acompanhada com dados adicionais especificando um id do peer de envio, um endereço IP e
# o número de porta. A mensagem JOIN é usada para solicitar que um peer insira o nó emissor na sua lista de peers
# conhecidos. Se a lista de peers já estiver cheia ou o ID especificado já estiver na lista (ou os argumentos
# especificados forem incorretos para a mensagem JOIN), uma mensagem ERRO será enviada de volta em uma resposta.
# Caso contrário, as informações do nó remoto serão adicionadas à lista e uma confirmação REPL será enviada.
INSERTPEER = "JOIN"

# A mensagem QUER é a mais complexa para manipular nessa aplicação. Após a recepção deste tipo de mensagem,
# e se o os dados fornecidos estiverem corretos (return-peer-id, key e ttl), então o peer responde
# simplesmente com uma mensagem de confirmação REPL; Caso contrário, uma mensagem ERRO é retornada.
# Antes de sair da rotina do manipulador para esse tipo de mensagem (e fechar a conexão do socket),
# uma thread separada é iniciada para realmente processar as informações de consulta.
QUERY = "QUER"

# Um peer receberá uma mensagem RESP em resposta a uma mensagem QUER que tinha enviado anteriormente para outros peers
# na rede. (O projeto de nosso protocolo aqui não exclui a possibilidade de peers receber RESP mensagens
# para arquivos que não tenham consultado - isso pode ser visto como uma feature ou um bug.) A mensagem RESP inclui
# um nome de arquivo e o peer_id do peer que possui uma cópia do arquivo. Ao receber uma mensagem RESP, um peer não
# precisa enviar nenhuma resposta; Se o nome do arquivo não estiver presente na lista de arquivos, uma entrada será
# adicionada à lista indicando que o arquivo pode ser encontrado no nó especificado.
QRESPONSE = "RESP"

# Os dados de uma mensagem FGET consistem em um nome de arquivo. Se o peer que recebe a mensagem FGET não possuir
# uma cópia do arquivo especificado ou se não é legível por algum motivo, uma resposta ERRO é enviada.
# Caso contrário, todo o arquivo é enviado à uma mensagem REPL.
FILEGET = "FGET"

# Uma mensagem QUIT, incluindo um peer id nos dados da mensagem, indica a um node que remova as informações do peer
# especificado da sua lista de peers conhecidos quando o peer se prepara para sair da rede. Observe que, como ocorre
# na maioria dos protocolos P2P, um nó também pode deixar a rede inesperadamente, então algum tipo de rotina de
# "estabilização" deve ser executado por cada peer para atualizar periodicamente sua lista de peers.
PEERQUIT = "QUIT"

REPLY = "REPL"
ERROR = "ERRO"


# ==============================================================================
class PeerFiler(PeerNode):
    # ==============================================================================
    """ 
    Implementa uma entidade peer-to-peer de compartilhamento de arquivos.
    """

    # --------------------------------------------------------------------------
    def __init__(self, server_port, max_peers):
        """ 
        Inicializa o peer para suportar conexões até número máximo de peers 'max_peers', 
        com seu servidor escutando em uma porta especificada. Também define a tablea de
        arquivos locais para vazio e adiciona handlers ao PeerNode.
        """
        PeerNode.__init__(self, server_port, max_peers=max_peers)

        self.files = {}  # arquivos disponiveis: name --> peer_id (host:port)

        self.add_router(self.__router)

        handlers = {
            LISTPEERS: self.__handle_list_peers,
            INSERTPEER: self.__handle_insert_peer,
            PEERNAME: self.__handle_peer_name,
            QUERY: self.__handle_query,
            QRESPONSE: self.__handle_query_response,
            FILEGET: self.__handle_get_file,
            PEERQUIT: self.__handle_quit
        }

        for mt in handlers:
            self.add_handler(mt, handlers[mt])

    # --------------------------------------------------------------------------
    @staticmethod
    def __debug(msg):
        print 'PeerFiler::', msg

    # --------------------------------------------------------------------------
    def __router(self, peer_id):
        if peer_id not in self.get_peer_ids():
            return None, None, None
        else:
            rt = [peer_id]
            rt.extend(self.peers[peer_id])
            return rt

    # INSERTPEER arguments: "peer_id host port"
    # --------------------------------------------------------------------------
    def __handle_insert_peer(self, peer_conn, data):
        """ 
        Porcessa o tipo de mensagem INSERTPEER. 
        Os dados da mensagem devem ser  uma string contendo "peer_id host port", 
        onde peer_id é o nome canônico do  peer que deseja ser adicionado a esta 
        lista de peers, host e porta  são os dados necessários para se conectar ao peer.
        """

        self.peer_lock.acquire()

        self.__debug("Não é possível adicionar o peer, na lista de peers, porque '__handle_insert_peer' não foi implementada")
        self.__debug("Descomente as linhas em '__handle_insert_peer' para adicionar o peer na lisa de peers")

        try:
            try:
                pass  # remove essa linha depois de descomentar as linhas nos itens abaixo

                # -----------------------
                # 1) primeiro precisamos obter peer_id, host, port dos dados. Dica:
                # utilize a função split para remover os espaco e obter os 3 valores.
                # -----------------------

                # peer_id, host, port = data.split()

                # -----------------------
                # 2) Verificar se não atingiu a capacidade máxima de conexões suportadas pelo peer.
                # Caso tenha atingido o limite enviar mensagem de error para o peer_conn e finalizar
                # a execução dessa função inserindo uma linha com 'return'.
                # -----------------------

                # if self.max_peers_reached():
                #     self.__debug('maxpeers %d reached: connection terminating'
                #                  % self.max_peers)
                #     peer_conn.send_data(ERROR, 'Join: too many peers')
                #     return

                # -----------------------
                # 3) Adicionar o peer na lista de peer conhecidos, utilizando self.add_peer(peer_id, host, port).
                # Retornar uma resposta ao peer_conn sobre a realização da inserção, e caso não seja adicionado,
                # enviar um error.
                # Dica: tratar essa inserção para não adicionar peers já estejam na lista e o proprio self.peer_id.
                # -----------------------

                # if peer_id not in self.get_peer_ids() and peer_id != self.peer_id:
                #     self.add_peer(peer_id, host, port)
                #     self.__debug('added peer: %s' % peer_id)
                #     peer_conn.send_data(REPLY, 'Join: peer added: %s' % peer_id)
                # else:
                #     peer_conn.send_data(ERROR, 'Join: peer already inserted %s'
                #                         % peer_id)

            except:
                self.__debug('invalid insert %s: %s' % (str(peer_conn), data))
                peer_conn.send_data(ERROR, 'Join: incorrect arguments')
        finally:
            self.peer_lock.release()

    # --------------------------------------------------------------------------
    def __handle_peer_name(self, peer_conn, data):
        """ 
        Processa o tipo de mensagem NAME. Os dados da mensagem não são utilizados. 
        """
        self.__debug("__handle_peer_name")

        # Responda a requisição enviando o nome (self.peer_id) desse peer. Utilize a seguinte função:
        # peer_conn.send_data(REPLY, <peer_id>)

        #  *** Implemente aqui ***
        pass  # remove essa linha depois de implementar as alterações

    # --------------------------------------------------------------------------
    def __handle_list_peers(self, peer_conn, data):
        """ 
        Processa o tipo de mensagem LISTPEERS. Os dados da mensagem não são utilizados.
        """
        self.__debug("__handle_list_peers")

        self.peer_lock.acquire()
        try:
            pass  # remove essa linha depois de implementar as alterações

            # -----------------------
            # 1) Implemente aqui a resposta para a lita de peers. Lembrando que se deve iterar sobre para depois
            # implementar os próximos itens:
            # -----------------------
            # self.get_peer_ids()

                # -----------------------
                # 2) Obtenha o host e a port com:
                # -----------------------
                # host, port = self.get_peer(pid)

                # -----------------------
                # 3) Envie a mensagem para cada pid utilizando a função:
                # -----------------------
                # peer_conn.send_data(REPLY, '%s %s %d' % (pid, host, port))

        finally:
            self.peer_lock.release()

    # --------------------------------------------------------------------------
    def check_live_peers(self):
        """
        Reliza tentativas de fazer ping a todos os peers atualmente conhecidos para garantir que 
        eles ainda estejam ativos. Remove qualquer um da lista os peers que não responde. 
        Esta função pode ser usada como um estabilizador simples, ou seja, ser executa por uma thread
        a cada x segundos.
        """
        self.__debug("check_live_peers")

        # -----------------------
        # 1) Lista que deve conter todos os peers a serem deletados
        # -----------------------

        to_delete = []

        # -----------------------
        # 2) Iterar sobre todos os peers conhecidos
        # -----------------------

        for pid in self.peers:
            is_connected = False
            peer_conn = None
            try:

                # -----------------------
                # 3) Conectar nesses peers e enviar uma mensagem de PING para verificar se estão ativos.
                # Utilizando a classe PeerConnection e a funação dessa classe send_data para enviar "PING".
                # Essa mensagem pode ser aleatória, qualquer messagem. Estamos apenas testando se é possível
                # conectar com esse peer.
                #
                # 4) Caso não seja possível conectar  será disparado uma except assim o peer é adicionado
                # na lista para exclusão.
                # -----------------------

                #  *** Implemente aqui ***
                pass  # remove essa linha depois de implementar as alterações

            except:
                to_delete.append(pid)
            if is_connected:
                peer_conn.close()

        self.peer_lock.acquire()
        # -----------------------
        # 5) Descobindo todos os peers para serem excluidos, remova esses peers da lista de self.peers.
        # -----------------------
        try:

            #  *** Implemente aqui ***
            pass  # remove essa linha depois de implementar as alterações

        finally:
            self.peer_lock.release()

    # QUERY arguments: "return-peer_id key ttl"
    # --------------------------------------------------------------------------
    def __handle_query(self, peer_conn, data):
        """ 
        Processa o tipo de mensagem QUERY. 
        Os dados da mensagem devem estar no formato de uma string, "return-peer_id key ttl", 
        onde return-peer-id é o nome do peer que iniciou a consulta, key é o (parte do) nome do arquivo 
        e ttl é quantos outros níveis de peers que essa consulta deve ser propagada.
        """
        self.__debug("__handle_query")

        try:
            peer_id, key, ttl = data.split()
            peer_conn.send_data(REPLY, 'Query ACK: %s' % key)

            # Iniciar thread para processar a query
            t = threading.Thread(target=self.__process_query, args=[peer_id, key, int(ttl)])
            t.start()
        except:
            self.__debug('query invalida %s: %s' % (str(peer_conn), data))
            peer_conn.send_data(ERROR, 'Query: argumentos incorretos')

    # --------------------------------------------------------------------------
    def __process_query(self, peer_id, key, ttl):
        # --------------------------------------------------------------------------
        """ 
        Realiza o processamento de uma mensagem de consulta depois que ela foi recebida 
        e confirmada, respondendo a uma mensagem QRESPONSE se o arquivo for encontrado na 
        lista local de arquivos ou propagando a mensagem para todos os vizinhos imediatos.
        
        :type key: str
        :type peer_id: str
        :type ttl: int
        :param peer_id: Peer de origem (host,port) que está realizando a query.
        :param key: Chave de busca para o nome do arquivo a ser encontrado.
        :param ttl: 
        """
        self.__debug("__process_query")

        # -----------------------
        # 1) Obtem todos os nomes da tabela de arquivos.
        # -----------------------

        for file_name in self.files.keys():

            # -----------------------
            # 2) Se a key de busca pertencer ao arquivo, envie a resposta para o peer_id
            # -----------------------

            if key in file_name:

                # -----------------------
                # 3) Obtem o arquivo da lista de arquivos. Tratar para caso o arquivo seja local, pois ele é mapeado
                # tem valor = None.
                # -----------------------

                # *** Implemente 3 aqui ***

                # -----------------------
                # 4) obter os valores de host e port do peer_id utiliznado o split(:) separado por ':'
                # -----------------------

                # *** Implemente 4 aqui ***

                # -----------------------
                # 5) Enviar um QRESPONSE para o peer_id no seguinte formato. '%s %s' % (file_name, file_peer_id)
                # Não se pode usar self.send_to_peer aqui porque peer_id não é necessariamente um vizinho imediato
                # portanto utilize self.connect_and_send e finalize a execução da função QRESPONSE
                # -----------------------

                # *** Implemente 5 aqui ***

                return

        # -----------------------
        # 6) Caso a chave não seja encontrada, então devemos propagar a consulta para os vizinhos.
        # -----------------------

        if ttl > 0:

            # -----------------------
            # 7) Formatar a mensagem a ser enviada. Observe que no ttl está contabilizado a execuçao nesse peer.
            # Deve ser decrementado o valor para que a chamada dessa query pare de ser propagada.
            # -----------------------

            msg_data = '%s %s %d' % (peer_id, key, ttl - 1)

            # -----------------------
            # 8) Enviar com send_to_peer a QUERY de busca para a lista de peers
            # -----------------------

            # *** Implemente 8 aqui ***

    # QRESPONSE arguments: "file_name peer_id"
    # --------------------------------------------------------------------------
    def __handle_query_response(self, peer_conn, data):
        # --------------------------------------------------------------------------
        """ 
        Processa o tipo de mensagem QRESPONSE.
        Os dados de mensagem devem estar no formato de uma string, "file_name peer_id",
        onde file_name é o arquivo que foi consultado e peer_id é o nome do peer que 
        tem uma cópia do arquivo.
        """
        self.__debug("__handle_query_response")

        try:

            #  *** Implemente aqui ***
            pass  # remove essa linha depois de implementar as alterações

        except:
            # if self.debug:
            traceback.print_exc()

    # --------------------------------------------------------------------------
    def __handle_get_file(self, peer_conn, data):
        """
        Processa o tipo de mensagem FILEGET. 
        Os dados da mensagem devem estar no formato de uma string, "file_name", onde file_name 
        é o nome do arquivo a ser buscado.
        """
        self.__debug("__handle_get_file")

        file_name = data
        if file_name not in self.files:
            self.__debug('Arquivo nao foi encontrado: %s' % file_name)
            peer_conn.send_data(ERROR, 'Arquivo nao foi encontrado')
            return
        try:
            fd = file(file_name, 'r')
            file_data = ''
            while True:
                data = fd.read(2048)
                if not len(data):
                    break
                file_data += data
            fd.close()
        except:
            self.__debug('Erro ao ler o arquivo %s' % file_name)
            peer_conn.send_data(ERROR, 'Erro ao ler o arquivo')
            return

        peer_conn.send_data(REPLY, file_data)

    # --------------------------------------------------------------------------
    def __handle_quit(self, peer_conn, data):
        """ 
        Processa o tipo de mensagem QUIT. 
        Os dados da mensagem devem estar no formato de uma string, "peer_id", onde peer_id é o 
        nome canônico do peer que deseja ser removido do diretório deste peer.
        """
        self.__debug("__handle_quit")

        self.peer_lock.acquire()
        try:
            peer_id = data.lstrip().rstrip()  # removendo espaços em brando na esquerda e da direita dessa string.
            if peer_id in self.get_peer_ids():
                msg = 'Quit: peer removido: %s' % peer_id
                self.__debug(msg)
                peer_conn.send_data(REPLY, msg)
                self.remove_peer(peer_id)
            else:
                msg = 'Quit: peer nao foi encontrado: %s' % peer_id
                self.__debug(msg)
                peer_conn.send_data(ERROR, msg)
        finally:
            self.peer_lock.release()

    # --------------------------------------------------------------------------
    def build_peers(self, host, port, hops=1):
        """ 
        build_peers(host, port, hops) 
    
        Tenta construir a lista local de peers até o limite máximo permitido por self.max_peers,
        utuilizando primeiro uma pesquisa em profundidade simples, passando um host inicial e a porta 
        como ponto de partida. A profundidade da pesquisa é limitada pelo parâmetro hops.
        """

        # Verifica se atingiu o limite de peers e se o parâmetro de hops apresenta um valor None,
        # caso True, para a execução dessa função.

        if self.max_peers_reached() or not hops:
            return

        peer_id = None

        self.__debug("Contruindo peers de (%s,%s)" % (host, port))

        try:
            _, peer_id = self.connect_and_send(host, port, PEERNAME, '')[0]

            self.__debug("peer contactado: " + peer_id)
            resp = self.connect_and_send(host, port, INSERTPEER,
                                         '%s %s %d' % (self.peer_id,
                                                       self.server_host,
                                                       self.server_port))[0]
            self.__debug(str(resp))
            if (resp[0] != REPLY) or (peer_id in self.get_peer_ids()):
                return

            self.add_peer(peer_id, host, port)

            # Fazer uma pesquisa em profundidade recursiva primeiro para adicionar mais peers.
            resp = self.connect_and_send(host, port, LISTPEERS, '', pid=peer_id)
            print "resposta com lista de peers", resp
            if len(resp) > 1:
                resp.reverse()
                resp.pop()  # remover da resposta o cabeçalho contendo o número de elementos retornados da lista
            while len(resp):
                next_pid, host, port = resp.pop()[1].split()
                if next_pid != self.peer_id:
                    self.build_peers(host, port, hops - 1)
        except:
            self.remove_peer(peer_id)

    def add_local_file(self, filename):
        """ 
        Registra um arquivo armazenado localmente com o peer.
        """

        self.files[filename] = None
        self.__debug("Arquivo local adicionado %s" % filename)
