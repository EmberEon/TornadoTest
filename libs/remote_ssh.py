import paramiko

from forum.utils import file_log


class SSHConnects:
    def __init__(self):
        self.__ssh_data = {}
        self.__cur_conn = None
        self.__host = ''
        self.__port = 0
        self.__usr = ''
        self.__pwd = ''
        self.__key_file = ''
        self.__p_key = None

    async def set_conn(self, host="", port=0, usr="", pwd="", key_file=None):
        if not host:
            host = self.__host
        if not port:
            port = self.__port
        if not usr:
            usr = self.__usr
        if not pwd:
            pwd = self.__pwd
        if not key_file:
            key_file = self.__key_file
        if not host or not port or not usr:
            return
        ssh_name = "{0}_{1}".format(host, port)
        self.__cur_conn = self.__ssh_data.get(ssh_name)
        if self.__cur_conn:
            trans_conn = self.__cur_conn.get_transport()
            if trans_conn and trans_conn.is_active:
                return self.__cur_conn
        conn = await self.__ssh_connect(host, port, usr, pwd=pwd, key_file=key_file)
        self.__ssh_data[ssh_name] = conn
        return conn

    async def __ssh_connect(self, host: str, port: int, usr: str, pwd="", key_file=None):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if key_file:
                if not self.__p_key:
                    self.__p_key = paramiko.RSAKey.from_private_key_file('./configs/{0}'.format(key_file))
                conn.connect(hostname=host, port=port, username=usr, pkey=self.__p_key)
            else:
                self.__p_key = None
                conn.connect(hostname=host, port=port, username=usr, password=pwd)
            conn.get_transport().set_keepalive(60)
            self.__host, self.__port, self.__usr, self.__pwd, self.__key_file = host, port, usr, pwd, key_file
        except Exception as err:
            file_log.failed(
                'SSH连接失败:', err, 'host', host, 'port', port, 'username', usr, 'pkey_file', key_file, 'password', pwd)
            return
        try:
            self.__cur_conn = conn
            return conn
        except Exception as err:
            file_log.failed('SSH访问失败:', err)
            return

    async def exec_cmd(self, cmd: str):
        """
        :return (str, str) 0: 命令执行结果，1：命令执行错误结果
        """
        if not self.__cur_conn:
            return None, None
        _, stdout, stderr = self.__cur_conn.exec_command(cmd)
        result = stdout.read()
        err = stderr.read()
        return result.decode('utf-8'), err.decode('utf-8')

    async def upload_local_file(self, file: str, r_path='/', file_name=''):
        """上传本地文件，目前支支持单线程"""
        res, err = await self.exec_cmd('ls {0}'.format(r_path))
        if res is None or not self.__cur_conn:
            return False
        if err:
            res, err = self.exec_cmd('mkdir {0}'.format(r_path))
        if not err:
            sftp = paramiko.SFTPClient.from_transport(self.__cur_conn.get_transport())
            if r_path[-1] != '/':
                r_path += '/'
            if not file_name:
                file_name = file.split('/')[-1]
            try:
                sftp.put(file, r_path + file_name)
                return True
            except Exception as err:
                file_log.failed("文件上传失败:", err)
                return False

    async def make_path(self, r_path: str):
        res, err = await self.exec_cmd('ls {0}'.format(r_path))
        if res is None or not self.__cur_conn:
            return False
        if err:
            dir_list = r_path.split('/')
            set_path = ''
            for file_dir in dir_list:
                if file_dir:
                    set_path += '/' + file_dir
            res, err = await self.exec_cmd('mkdir {0}'.format(set_path))
            if err:
                file_log.failed("远程服务器创建目录失败:", err, set_path)
                return False
        return True

    async def upload_file(self, file, file_name: str, r_path='/'):
        """上传内存读取的文件，只支持单线程上传"""
        sta = await self.make_path(r_path)
        if sta:
            sftp = paramiko.SFTPClient.from_transport(self.__cur_conn.get_transport())
            if r_path[-1] != '/':
                r_path += '/'
            try:
                sftp.putfo(file, r_path + file_name)
                return True
            except Exception as err:
                file_log.failed("文件上传失败:", err)
                return False
        return False

    async def copy_file(self, source: str, target: str, target_root: str, base_root='/'):
        sta = await self.make_path(target_root)
        if sta:
            cmd = "cp {0}{1} {0}{2}".format(base_root, source, target)
            res, err = await self.exec_cmd(cmd)
            if err:
                file_log.failed('远程资源服务器资源拷贝失败:', err)
                return False
            return True
        return False

    async def remove_file(self, path_list: list, base_root: str):
        if not path_list:
            return
        cmd, can_ex = "rm ", 0
        for item in path_list:
            if item.strip().find('-r') == -1 and item.strip().find('-f') == -1:
                cmd += "{}{} ".format(base_root, item)
                can_ex = 1
        if can_ex:
            res, err = await self.exec_cmd(cmd)
            if err:
                file_log.failed("远程移除文件失败:", err)
                return 0
            return 1

    def close_conn(self, host=None, port=0):
        if (not host or not port) and self.__cur_conn:
            return self.__cur_conn.close()
        ssh_name = "{0}_{1}".format(host, port)
        conn = self.__ssh_data.get(ssh_name)
        conn and conn.close()
