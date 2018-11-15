import os
import shutil

from troncli import utils
from troncli.constants import *

class Init(object):
    """handler for init dirs and fetch code"""
    def __init__(self):
        self.root_path = os.getcwd()
        self.source_full_jar = 'java-tron.jar'
        self.source_sol_jar = 'SolidityNode.jar'

    def create_dirs(self):
        print('self.root_path: ', self.root_path)
        path = self.root_path
        try:
            os.mkdir(path + NODES_DIR)
            os.mkdir(path + NODES_DIR + FULL_NODE_DIR)
            os.mkdir(path + NODES_DIR + SOLIDITY_NODE_DIR)
        except OSError as err:
            utils.warnning_msg('OSError -' + str(err))
        else:
            utils.success_msg('Folders are created:')
            utils.msg(path + '/ ')
            utils.msg('└──' + NODES_DIR)
            utils.msg('    ├──' + FULL_NODE_DIR)
            utils.msg('    └──' + SOLIDITY_NODE_DIR)

    async def fetch_jars(self, version):
        """
        get release url
        """
        url = JAVA_TRON_RELEASES_URL
        if (version == 'lastest'):
            url += 'Odyssey-v' + JAVA_TRON_LASTEST_VERSION
        elif ('3.1.3' <= version <= '3.1.3'):
            url += 'Odyssey-v' + version
        """
        download
        """
        utils.msg('download fullnode jar might take a while')
        await utils.download(self.source_full_jar, url)
        utils.success_msg('.jar file of Fullnode is successfully downloaded')
        utils.msg('download solidity jar might take a while')
        await utils.download(self.source_sol_jar, url)
        utils.success_msg('.jar file of Soliditynode is successfully downloaded')

    async def move_jars(self):
        shutil.move(self.root_path + '/' + self.source_full_jar, 
            self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR)
        shutil.move(self.root_path + '/' + self.source_sol_jar, 
            self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOLIDITY_NODE_JAR)
        utils.success_msg('initialization finished')

