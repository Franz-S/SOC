'''
Created on Aug 10, 2015

@author: franz
'''
#ACHTUNG KEINE LEERZEICHEN IM PFAD WEGEN commands

import commands, time, Gnuplot
import os


directory=[1,2,3]
filename=[1,2,3]
scriptname=[1,2,3]
readmename=[1,2,3]
op_choice=2#0:testing,1:Vector,2:Matrix coloum mayor,3:Matrix row mayor 
remote_address="stuebler@krupp2.iue.tuwien.ac.at"
#remote_address="stuebler@jwein2.iue.tuwien.ac.at"
#remote_address="localhost"
openmp=0#0:kein open mp,1 openmp
while openmp<2:
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
        foldername="Matrix_coloum_mayor"
    elif op_choice==3 :
        min_loop=10
        max_loop=5e3
        foldername="Matrix_row_mayor"
    
    directory[openmp]="/home/franz/Franz/Benchmark/temp/"+foldername+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
    if not os.path.exists(directory[openmp]): #if the directory does not exist, it will be created
        os.makedirs(directory[openmp])
    filename[openmp]=directory[openmp]+("file.txt") #path for datafile
    scriptname[openmp]=directory[openmp]+("script.gp")#path for script
    readmename[openmp]=directory[openmp]+("readme.txt")#path for readme
    buildfolder="~/viennacl/build/"#path to the build folder for cmake e.g
    c_file=buildfolder+"examples/benchmarks/franz-bench-cpu"#path for the c++ file

    remote="ssh "+remote_address+" "
    
    readme=open(readmename[openmp],"w")
    if openmp==1:
        cmake_flag="cmake .. -DENABLE_OPENMP=ON -DCMAKE_BUILD_TYPE=Release"
        readme.write("""VIENNACL_WITH_OPENMP\n"""+remote_address)
    elif openmp==0:
        cmake_flag="cmake .. -DENABLE_OPENMP=OFF -DCMAKE_BUILD_TYPE=Release"
        readme.write("""NO_VIENNACL_WITH_OPENMP\n"""+remote_address)
    readme.close()
    
     
    print "Benchmarktest von Franz"
    
    cmd="cd "+buildfolder+";"+cmake_flag+";make franz-bench-cpu"
    
    text=commands.getstatusoutput(remote+"'"+cmd+"'")[1]
    print text
    
    cmd=c_file+" "+str(0)+" "+str(op_choice)
    
    text=commands.getstatusoutput(remote+"'"+cmd+"'")[1]#c-file aufrufen, es wird im python verzeichnis die file.txt erstellt
    print text
    
    cmd=""
    
    
    
    
    i=min_loop #start size for the vector
    while i<max_loop: #the loop
        cmd=c_file+" "+str(i)+" "+str(op_choice)
        text=commands.getstatusoutput(remote+"'"+cmd+"'")[1]
        print text
        print str(i)+". size, finished"
        i=long(i*1.3)
    
    text=commands.getstatusoutput("scp "+remote_address+":~/file.txt "+filename[openmp])[1]
    print text
    
    axis_titel=open(filename[openmp], "r").readline().split(',')#file.txt erste zeile lesen und teilen
    axis_titel.pop()#letzte element entfernen, wegen dem ","
    axis_titel.pop(0)#erstes element loeschen weil "N"
    
    
    if True:
        script=open(scriptname[openmp],"w") #the script for gnuplot will be created
        script.write("""set xlabel"N"
        set ylabel "GB/sec"
        set logscale\n""")
        #set the labeling and the graph to logarithmical 
        i=0
        if True:
            while i<len(axis_titel): #creat for each data set a independent plot and a eps-file
                script.write("set terminal x11 "+str(i)+"\n")
                #script.write("plot \""+filename[openmp]+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
                script.write("set terminal postscript eps 25 color solid linewidth 3\n")
                script.write("set output \""+directory[openmp]+axis_titel[i]+".eps\"\n")
                script.write("plot \""+filename[openmp]+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
                i=i+1
        
        #script.write("pause -1 \"Hit any key to continue\"\n")
        script.close()
        
        g = Gnuplot.Gnuplot(debug=0) #start gnuplot with the script
        g.load(scriptname[openmp])
        #raw_input('Please press return to continue...\n')
    openmp=openmp+1



directory[openmp]="/home/franz/Franz/Benchmark/temp/"+foldername+"_combi"+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
filename[openmp]=directory[openmp]+("file.txt") #path for datafile
scriptname[openmp]=directory[openmp]+("script.gp")#path for script
readmename[openmp]=directory[openmp]+("readme.txt")#path for readme
if not os.path.exists(directory[openmp]): #if the directory does not exist, it will be created
    os.makedirs(directory[openmp])
script=open(scriptname[openmp],"w") #the script for gnuplot will be created
script.write("""set xlabel"N"
set ylabel "GB/sec"
set logscale\n""")
#set the labeling and the graph to logarithmical 
i=0

readme=open(readmename[openmp],"w")
readme.write("""combination\n"""+remote_address)
readme.close()


while i<len(axis_titel): #creat for each data set a independent plot and a eps-file
    #script.write("set terminal x11 "+str(i)+"\n")
    #script.write("plot \""+filename[openmp]+"\" using 1:"+ str(i+2)+" title '"+axis_titel[i]+"' with linespoints\n")
    script.write("set terminal postscript eps 25 color solid linewidth 3\n")
    script.write("set output \""+directory[openmp]+axis_titel[i]+".eps\"\n")
    script.write("plot \""+filename[0]+"\" u 1:"+ str(i+2)+" title '"+axis_titel[i]+" no openmp"+"' w lp, \""+filename[1]+"\" u 1:"+ str(i+2)+" title '"+axis_titel[i]+" openmp"+"' w lp\n")
    i=i+1
    
    
g = Gnuplot.Gnuplot(debug=0) #start gnuplot with the script
g.load(scriptname[openmp])
script.close()
print "finished everything"

        
