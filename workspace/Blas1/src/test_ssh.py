'''
Created on Aug 19, 2015

@author: franz
'''

import paramiko
privkey=paramiko.RSAKey.from_private_key(open("/home/franz/.ssh/id_rsa","r"))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="jwein2.iue.tuwien.ac.at", username="stuebler",pkey=privkey)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls")
