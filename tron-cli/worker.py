import os
import subprocess

from constants import *
from utils import download, success_msg, warnning_msg, msg

class Worker(object):
    """handler for manage multiple nodes in multiple processes"""
    def __init__(self, root_path):
        self.root_path = root_path
        self.processes = {}

    async def run(self, node_type):
        # self.processes['fullnode'] = self.start()
        pid = await self.start(node_type)
        success_msg('node running at pid:' + str(pid))

    async def start(self, node_type):
        """
        start a node and return its pid
        execute cmd to inherit the shell process, instead of having the shell launch a child process
        """
        if node_type == 'full':
            os.chdir(self.root_path + NODES_DIR + FULL_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR + \
                " -c " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG + " --witness" + \
                " -d " + self.root_path + NODES_DIR + FULL_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path + NODES_DIR)
        elif node_type == 'sol':
            os.chdir(self.root_path + NODES_DIR + SOLIDITY_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOLIDITY_NODE_JAR + \
                " -c " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG + " --witness" + \
                " -d " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path + NODES_DIR)
        else:
            warnning_msg('wrong node type')

        return _process.pid

    async def stop(self, pid):
        try:
            subprocess.Popen(["kill", "-15", pid])
        except OSError as err:
            warnning_msg('OSError -' + str(err))
        else:
            success_msg('process: ' + pid + ' is shutting down')

        
