'''
Created on Aug 10, 2015

@author: franz
'''
#ACHTUNG KEINE LEERZEICHEN IM PFAD WEGEN commands

import commands, time, Gnuplot
import os
import shutil



op_choice=1#0:testing,1:Vector,2:Matrix coloum mayor,3:Matrix row mayor 
openmp=0#0:kein open mp,1 openmp
if op_choice==0 :
    min_loop=100
    max_loop=1e7
    foldername="testing"
elif op_choice==1 :
    min_loop=100
    max_loop=1e7
    foldername="Vector"
elif op_choice==2 :
    min_loop=10
    max_loop=5e3
    foldername="Matrix coloum mayor"
elif op_choice==3 :
    min_loop=10
    max_loop=5e3
    foldername="Matrix row mayor"

if openmp==1:
    cmake_flag="cmake .. -DENABLE_OPENMP=ON -DCMAKE_BUILD_TYPE=Release"
elif openmp==0:
    cmake_flag="cmake .. -DENABLE_OPENMP=OFF -DCMAKE_BUILD_TYPE=Release"


 
directory="/home/franz/Franz/Benchmark/temp/"+foldername+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
if not os.path.exists(directory): #if the directory does not exist, it will be created
    os.makedirs(directory)
filename=directory+("file.txt") #path for datafile
scriptname=directory+("script.gp")#path for script
readmename=directory+("readme.txt")#path for readme
buildfolder="/home/franz/viennacl/build/"#path to the build folder for cmake e.g
c_file=buildfolder+"examples/benchmarks/franz-bench-cpu"#path for the c++ file

readme=open(readmename,"w")
readme.write("""VIENNACL_WITH_OPENMP""")
readme.close()
    
print "Benchmarktest von Franz"



text=commands.getstatusoutput("cd "+buildfolder+";"+cmake_flag)[1]
print text

text=commands.getstatusoutput("cd "+buildfolder+";make franz-bench-cpu")[1]
print text


text=commands.getstatusoutput(c_file+" "+str(0)+" "+str(op_choice))[1]#c-file aufrufen, es wird im python verzeichnis die file.txt erstellt
print text

i=min_loop #start size for the vector
while i<max_loop: #the loop
    text=commands.getstatusoutput(c_file+" "+str(i)+" "+str(op_choice))[1]
    print text
    print str(i)+". size, finished"
    i=long(i*1.3)
    
shutil.move(os.path.abspath(".")+"/file.txt",filename)#verschieben des file.txt in den richtigen ordner

axis_titel=open(filename, "r").readline().split(',')#file.txt erste zeile lesen und teilen
axis_titel.pop()#letzte element entfernen, wegen dem ","
axis_titel.pop(0)#erstes element loeschen weil "N"



script=open(scriptname,"w") #the script for gnuplot will be created
script.write("""set xlabel"N"
set ylabel "GB/sec"
set logscale\n""")
#set the labeling and the graph to logarithmical 
i=0
if True:
    while i<len(axis_titel): #creat for each data set a independent plot and a eps-file
        script.write("set terminal x11 "+str(i)+"\n")
        script.write("plot \""+filename+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
        script.write("set terminal postscript eps 25 color solid linewidth 3 enhanced\n")
        script.write("set output \""+directory+axis_titel[i]+".eps\"\n")
        script.write("plot \""+filename+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
        i=i+1
else:
    script.write("plot \"/home/franz/Franz/Benchmark/file.txt\" u 1:3 title 'd.y=x_old' w lp, \""+filename+"\" u 1:3 title 'd.y=x_new' w lp\n")

script.write("pause -1 \"Hit any key to continue\"\n")
script.close()

g = Gnuplot.Gnuplot(debug=0) #start gnuplot with the script
g.load(scriptname)
raw_input('Please press return to continue...\n')
    
