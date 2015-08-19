'''
Created on Aug 19, 2015

@author: franz
'''
import commands

cmd="""'ls;cd viennacl;ls'"""

text=commands.getstatusoutput("scp stuebler@jwein2.iue.tuwien.ac.at:~/testfile.txt ~/")
print text

text=commands.getstatusoutput("ssh stuebler@jwein2.iue.tuwien.ac.at "+cmd)[1]
print text

