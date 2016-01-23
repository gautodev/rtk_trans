#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import json
import log
import time
from server_thread import ServerThread
from client_thread import ClientThread


class Rtk:
    def got_data_cb(self, data):
        log.debug('%s >> recv %d bytes' % (time.strftime('%Y-%m-%d %H:%M:%S'), len(data)))
        clients = self.server.clients.copy()
        for c in clients:
            try:
                c.sendall(data)
            except:
                pass

    def main(self):
        config_file_name = 'config.json'
        try:
            with open(config_file_name) as config_data:
                configs = json.load(config_data)
        except:
            print('load config fail.')
            return

        log.initialize_logging(configs['enableLog'].lower() == 'true')
        log.info('main: start')
        self.server = ServerThread(configs['listenPort'])
        self.client = ClientThread(configs['serverIpAddress'], configs['serverPort'], self.got_data_cb)
        self.server.start()
        self.client.start()

        print("enter 'q' to quit.")
        while input() != 'q':
            print("enter 'q' to quit.")

        self.client.running = False
        self.client.join()
        self.server.running = False
        self.server.join()
        log.info('main: bye')


if __name__ == '__main__':
    rtk = Rtk()
    rtk.main()