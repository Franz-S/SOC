'''
Created on Aug 10, 2015

@author: franz
'''
import subprocess, time, Gnuplot
import os
import shutil

print "Benchmarktest von Franz"

directory="/home/franz/Franz/Benchmark/temp/"+"Bench"+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
if not os.path.exists(directory): #if the directory does not exist, it will be created
    os.makedirs(directory)
filename=directory+("file.txt") #path for datafile
scriptname=directory+("script.gp")#path for script
c_file="/home/franz/Franz/codeblocks/Vector 5/bin/Release/Vector"#path for the c++ file


subprocess.call([c_file, str(0)])#c-file aufrufen, es wird im python verzeichnis die file.txt erstellt


i=100 #start size for the vector
while i<1e6: #the loop
    subprocess.call([c_file, str(i)])
    i=long(i*2)
    print str(i)+". size, finished"
    
shutil.move(os.path.abspath(".")+"/file.txt",filename)#verschieben des file.txt in den richtigen ordner

axis_titel=open(filename, "r").readline().split(',')#file.txt erste zeile lesen und teilen
axis_titel.pop()#letzte element entfernen, wegen dem ","
axis_titel.pop(0)#erstes element loeschen weil "N"

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

axis_titel.close()