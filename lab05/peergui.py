#!/usr/bin/python
# coding=utf-8

"""
Module implementing simple BerryTella GUI for a simple p2p network.
"""

import sys
import threading
from Tkinter import *
from random import *
from peerfiler import *


class PeerGui(Frame):
    def __init__(self, tracker_peer, hops=2, max_peers=5, server_port=5678, master=None):
        Frame.__init__(self, master)

        # --------------------------------------------------------------------------
        # PeerFiler
        # --------------------------------------------------------------------------
        # PeerFiler | Criar object
        self.btpeer = PeerFiler(server_port=server_port, max_peers=max_peers)
        # PeerFiler | Build peers
        host, port = tracker_peer.split(':')
        self.btpeer.build_peers(host, int(port), hops=hops)

        # --------------------------------------------------------------------------
        # View
        # --------------------------------------------------------------------------
        # View | Criar
        self.grid()
        self.create_widgets()
        self.master.title("Filer GUI %d" % server_port)
        # View | Listeners
        self.bind("<Destroy>", self.__onDestroy)
        # View | Atualizar lista de peers
        self.update_peer_list()

        # --------------------------------------------------------------------------
        # Iniciar thread para o servidor P2P desse peer
        # --------------------------------------------------------------------------
        t = threading.Thread(target=self.btpeer.mainloop, args=[])
        t.start()

        # --------------------------------------------------------------------------
        # Atualizações da View | lista de peers, lista de arquivos
        # --------------------------------------------------------------------------
        # Checar a conexão com peers ativos a cada 3 segundos
        self.btpeer.every(self.btpeer.check_live_peers, 3)
        # Atualizar a lista de peers e arquivos da View a cada 3 segundos
        self.after(3000, self.onTimer)

    # --------------------------------------------------------------------------
    def __onDestroy(self, event):
        self.btpeer.shutdown = True

    # --------------------------------------------------------------------------
    def onTimer(self):
        self.onRefresh()
        self.after(3000, self.onTimer)

    # --------------------------------------------------------------------------
    def onRefresh(self):
        self.update_peer_list()
        self.update_file_list()

    # --------------------------------------------------------------------------
    def onAdd(self):
        file = self.addfileEntry.get()
        if file.lstrip().rstrip():
            filename = file.lstrip().rstrip()
            self.btpeer.add_local_file(filename)  # Adiciona um arquivo localmente disponibilizando para ser consultado
        self.addfileEntry.delete(0, len(file))
        self.update_file_list()

    # --------------------------------------------------------------------------
    def onSearch(self):
        key = self.searchEntry.get()
        self.searchEntry.delete(0, len(key))

        for peer_id in self.btpeer.get_peer_ids():
            self.btpeer.send_to_peer(peer_id, QUERY, "%s %s 4" % (self.btpeer.peer_id, key))  # Busca de um arquivo a partir de uma chave de busca

    # --------------------------------------------------------------------------
    def onFetch(self):
        sels = self.fileList.curselection()
        if len(sels) == 1:
            sel = self.fileList.get(sels[0]).split(':')  # file_name:host:port
            if len(sel) > 2:  # file_name:host:port
                file_name, host, port = sel
                resp = self.btpeer.connect_and_send(host, port, FILEGET, file_name)  # Obter o arquivo selecionado
                if len(resp) and resp[0][0] == REPLY:
                    fd = file(file_name, 'w')
                    fd.write(resp[0][1])
                    fd.close()
                    self.btpeer.files[file_name] = None  # porque o arquivo é local agora!
    #                 O arquivo é local, mas esse peer não pode compartilhar o arquivo?

    # --------------------------------------------------------------------------
    def onRemove(self):
        selected_peers = self.peerList.curselection()
        if len(selected_peers) == 1:
            peer_id = self.peerList.get(selected_peers[0])
            self.btpeer.send_to_peer(peer_id, PEERQUIT, self.btpeer.peer_id)  # Fechar a conexão com o peer
            self.btpeer.remove_peer(peer_id)  # Remove o peer da lista de peers

    # --------------------------------------------------------------------------
    def onRebuild(self):
        if not self.btpeer.max_peers_reached():
            peer_id = self.rebuildEntry.get()
            self.rebuildEntry.delete(0, len(peer_id))
            peer_id = peer_id.lstrip().rstrip()
            try:
                host, port = peer_id.split(':')
                # print "doing rebuild", peerid, host, port
                self.btpeer.build_peers(host, port, hops=3)  # Reconstruir a conexão e listar todos os peers
            except:
                # if self.btpeer.debug:
                traceback.print_exc()

    # --------------------------------------------------------------------------
    def update_peer_list(self):
        if self.peerList.size() > 0:
            self.peerList.delete(0, self.peerList.size() - 1)
        for p in self.btpeer.get_peer_ids():
            self.peerList.insert(END, p)

    # --------------------------------------------------------------------------
    def update_file_list(self):
        if self.fileList.size() > 0:
            self.fileList.delete(0, self.fileList.size() - 1)
        for f in self.btpeer.files:
            p = self.btpeer.files[f]
            if not p:
                p = '(local)'
            self.fileList.insert(END, "%s:%s" % (f, p))

    # --------------------------------------------------------------------------
    def create_widgets(self):
        """
        Set up the frame widgets
        """
        fileFrame = Frame(self)
        peerFrame = Frame(self)

        rebuildFrame = Frame(self)
        searchFrame = Frame(self)
        addfileFrame = Frame(self)
        pbFrame = Frame(self)

        fileFrame.grid(row=0, column=0, sticky=N + S)
        peerFrame.grid(row=0, column=1, sticky=N + S)
        pbFrame.grid(row=2, column=1)
        addfileFrame.grid(row=3)
        searchFrame.grid(row=4)
        rebuildFrame.grid(row=3, column=1)

        Label(fileFrame, text='Available Files').grid()
        Label(peerFrame, text='Peer List').grid()

        fileListFrame = Frame(fileFrame)
        fileListFrame.grid(row=1, column=0)
        fileScroll = Scrollbar(fileListFrame, orient=VERTICAL)
        fileScroll.grid(row=0, column=1, sticky=N + S)

        self.fileList = Listbox(fileListFrame, height=5,
                                yscrollcommand=fileScroll.set)

        self.fileList.grid(row=0, column=0, sticky=N + S)
        fileScroll["command"] = self.fileList.yview

        self.fetchButton = Button(fileFrame, text='Fetch',
                                  command=self.onFetch)
        self.fetchButton.grid()

        self.addfileEntry = Entry(addfileFrame, width=25)
        self.addfileButton = Button(addfileFrame, text='Add',
                                    command=self.onAdd)
        self.addfileEntry.grid(row=0, column=0)
        self.addfileButton.grid(row=0, column=1)

        self.searchEntry = Entry(searchFrame, width=25)
        self.searchButton = Button(searchFrame, text='Search',
                                   command=self.onSearch)
        self.searchEntry.grid(row=0, column=0)
        self.searchButton.grid(row=0, column=1)

        peerListFrame = Frame(peerFrame)
        peerListFrame.grid(row=1, column=0)
        peerScroll = Scrollbar(peerListFrame, orient=VERTICAL)
        peerScroll.grid(row=0, column=1, sticky=N + S)

        self.peerList = Listbox(peerListFrame, height=5,
                                yscrollcommand=peerScroll.set)
        # self.peerList.insert( END, '1', '2', '3', '4', '5', '6' )
        self.peerList.grid(row=0, column=0, sticky=N + S)
        peerScroll["command"] = self.peerList.yview

        self.removeButton = Button(pbFrame, text='Remove',
                                   command=self.onRemove)
        self.refreshButton = Button(pbFrame, text='Refresh',
                                    command=self.onRefresh)

        self.rebuildEntry = Entry(rebuildFrame, width=25)
        self.rebuildButton = Button(rebuildFrame, text='Rebuild',
                                    command=self.onRebuild)
        self.removeButton.grid(row=0, column=0)
        self.refreshButton.grid(row=0, column=1)
        self.rebuildEntry.grid(row=0, column=0)
        self.rebuildButton.grid(row=0, column=1)
