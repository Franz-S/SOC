'''
Created on Aug 10, 2015

@author: franz
'''
import subprocess, time, Gnuplot
import os

print "Benchmarktest von Franz, BLAS1 "

directory="/home/franz/SOC/Franz/Benchmark/"+"BLAS1_"+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
if not os.path.exists(directory): #if the directory does not exist, it will be created
    os.makedirs(directory)
filename=directory+("file.txt") #path for datafile
scriptname=directory+("script.gp")#path for script
c_file="/home/franz/SOC/Franz/codeblocks/Vector 5/bin/Release/Vector"#path for the c++file


axis_titel=subprocess.check_output([c_file, str(0)]).split(',') #axis_titel from the c-programm, converted into a array, split when there is a ","
axis_titel.pop()#for removing the last element which is a ' '

output=open(filename,"w") #data file will be created
output.write("#")#a "#" for gnuplot that the first line is a comment
output.write("{:<8}".format("N"))#print the differnt methodnames
i=0
while i<len(axis_titel):
    output.write("{:<9}".format(axis_titel[i]))
    i=i+1
output.write("\n")

i=100 #start size for the vector
while i<1e6: #the loop
    data=subprocess.check_output([c_file, str(i)])
    output.write(data)
    output.write('\n')
    i=long(i*2)
    print str(i)+". size, finished"
    
output.close()

script=open(scriptname,"w") #the script for gnuplot will be created
script.write("""set xlabel"N"
set ylabel "GFlops/sec"
set logscale\n""")
#set the labeling and the graph to logarithmical 
i=0
while i<len(axis_titel): #creat for each data set a independent plot and a eps-file
    script.write("set terminal x11 "+str(i)+"\n")
    script.write("plot \""+filename+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
    script.write("set terminal postscript eps 25 color solid linewidth 3 enhanced\n")
    script.write("set output \""+directory+axis_titel[i]+".eps\"\n")
    script.write("plot \""+filename+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
    i=i+1

script.write("pause -1 \"Hit any key to continue\"\n")
script.close()

g = Gnuplot.Gnuplot(debug=0) #start gnuplot with the script
g.load(scriptname)
raw_input('Please press return to continue...\n')

