'''
Created on Aug 10, 2015

@author: franz
'''
#ACHTUNG KEINE LEERZEICHEN IM PFAD WEGEN commands

import commands,sys

buildfolder="~/viennacl/build/"#path to the build folder for cmake e.g


cmake_flag="cmake .. -DENABLE_OPENMP=OFF -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS=-Werror"
cmd="cd "+buildfolder+";"+cmake_flag+";make vector_float_double-test-cpu -j4"
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/vector_float_double-test-cpu"
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/vector_float_double-test-cpu"


cmake_flag="cmake .. -DENABLE_OPENMP=ON -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS=-Werror"

cmd="cd "+buildfolder+";"+cmake_flag+";make vector_float_double-test-cpu -j4"
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/vector_float_double-test-cpu"
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/vector_float_double-test-cpu"

print "finished everything"
