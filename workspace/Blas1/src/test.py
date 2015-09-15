'''
Created on Aug 10, 2015

@author: franz
'''
#ACHTUNG KEINE LEERZEICHEN IM PFAD WEGEN commands

import commands,sys
print "start"


buildfolder="~/viennacl/build/"#path to the build folder for cmake e.g
testfile=["vector_float_double-test-cpu","matrix_row_double-test-cpu","matrix_col_double-test-cpu","matrix_vector-test-cpu"][1]
cmake_flag="cmake .. -DENABLE_OPENMP=OFF -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS=-Werror"
cmd="cd "+buildfolder+";"+cmake_flag+";make "+testfile
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/"+testfile
text=commands.getstatusoutput(cmd)#start the test
print text[1]
if int(text[0])!=0:#check if the test has worked
        print text[0]
        print "Error during make :("
        sys.exit()


cmake_flag="cmake .. -DENABLE_OPENMP=ON -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS=-Werror"

cmd="cd "+buildfolder+";"+cmake_flag+";make "+testfile
text=commands.getstatusoutput(cmd)#cmake set flags and make the file
print text[1]
if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
cmd="~/viennacl/build/tests/"+testfile
text=commands.getstatusoutput(cmd)#start the test
print text[1]
if int(text[0])!=0:#check if the test has worked
        print text[0]
        print "Error during make :("
        sys.exit()

print "finished everything"
