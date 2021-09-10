import socket


class HOST:
    
    def __init__(self,name,ip,username,password):
        self.name_to_func_mapping = {"command":self.__run_command_on_remote_machine,"upload":self.__upload_file_into_remote_machine,"download":self.__download_file_from_remote_machine}
        self.ssh = SSH(ip,username,password)
        self.name = name

    def __run_command_on_remote_machine(self,args):
        """
        param str command:  
            command to be run on a remote machine

        return output
        return error
        """
        try:
            command = args[0]
        except:
            raise Exception("Invalid argument for __run_command_on_remote_machine function")

        output = self.ssh.run_command(command)
        return output

    def __upload_file_into_remote_machine(self,args):
        try:
            local_path = args[0]
            remote_path = args[1]
        except:
            raise Exception("Invalid argument for __run_script_on_remote_machine function")

        self.ssh.upload_to_remote_machine(local_path,remote_path)


    def __download_file_from_remote_machine(self,args):
        try:
            remote_path = args[0]
            local_path = args[1]
        except:
            raise Exception("Invalid argument for __download_file_from_remote_machine function")

        self.ssh.download_from_remote_machine(remote_path,local_path)


    def run(self,func_name,*args):
        """
        runs a behaviour of a host

        param str func_name:
            functions name
        """
        return self.name_to_func_mapping[func_name](args)

    def get_name(self):
        """
        returns host's name
        """
        return self.name


class SSH:
    def __init__(self,ip,username,password,number_of_password_tries=3,timeout=1):
        self.ssh,_ = self.ssh_connect (ip,username,password,number_of_password_tries,timeout)

    def ssh_connect (self,ip,username,password,number_of_password_tries,timeout):
        import os
        import paramiko 
        import getpass 

        log_filename= "paramiko_log.txt"
        server=ip
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file(log_filename)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #In case the server's key is unknown,
        #we will be adding it automatically to the list of known hosts
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        #Loads the user's local known host file.
        for i in range(0,number_of_password_tries):
            try:
                if password is "":
                    password = getpass.getpass(prompt='Please Enter Remote Password:') 
                ssh.connect(server, username=username, password=password,timeout=timeout)
                break
            except socket.timeout as error:
               # print ('ERROR: {0}'.format(error))
                raise Exception(f'ERROR: {error} connecting to host {ip} through SSH')
            except Exception as error:# AuthenticationException:
                # if error.args[0] == 'timed out':
                #     break
                print ('ERROR: {0}'.format(error))
                password = ""                
            else:
                if i is number_of_password_tries-1:
                    return None,None
        return ssh,password

    def upload_to_remote_machine(self,local_path,remote_path):
        """
        upload_to_remote_machine uploads a file into a remote machine using sftp
        """ 
        sftp=self.ssh.open_sftp()
        sftp.put(local_path, remote_path)


    def download_from_remote_machine(self,remote_path,local_path):
        """
        download_from_remote_machine downloads a file from a remote machine using sftp
        """ 
        sftp=self.ssh.open_sftp()
        sftp.get(remote_path, local_path)


    def run_command(self,command):
        """
        run_command runs a command on a remote machine using ssh

        return str output
        """
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)

       # print ("output  ->  ", ssh_stdout.read()) #Reading output of the executed command
        output =  ssh_stdout.read()
        output = str(output,'utf-8')
        error = ssh_stderr.read()
        error = str(error,'utf-8')

        if error!='':
           raise Exception ("ERROR: {}".format(error))

        return output
