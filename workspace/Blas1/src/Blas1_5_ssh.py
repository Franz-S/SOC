'''
Created on Aug 10, 2015

@author: franz
'''
#ACHTUNG KEINE LEERZEICHEN IM PFAD WEGEN commands

import commands, time, Gnuplot,sys
import os

start=time.time()
directory=[1,2,3]#initiate the arrays
filename=[1,2,3]
scriptname=[1,2,3]
readmename=[1,2,3]
op_choice=0#0:testing,1:Vector,2:Matrix coloum mayor,3:Matrix row mayor 
remote_address=["stuebler@krupp2.iue.tuwien.ac.at","stuebler@jwein2.iue.tuwien.ac.at","localhost"][2]

print "Benchmarktest von Franz"

openmp=0#0:kein open mp,1 openmp#dont change because you need it for the loop
while openmp<2:
    if op_choice==0 :
        min_loop=10
        max_loop=5e3
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
    
    directory[openmp]="/home/franz/Franz/Benchmark/temp/"+remote_address+"/"+foldername+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
    if not os.path.exists(directory[openmp]): #if the directory does not exist, it will be created
        os.makedirs(directory[openmp])
    filename[openmp]=directory[openmp]+("file.txt") #path for datafile
    scriptname[openmp]=directory[openmp]+("script.gp")#path for script
    readmename[openmp]=directory[openmp]+("readme.txt")#path for readme
    buildfolder="~/viennacl/build/"#path to the build folder for cmake e.g
    c_file=buildfolder+"examples/benchmarks/franz-bench-cpu"#path for the c++ file
    remote="ssh "+remote_address+" "
    werror="-Werror"
    readme=open(readmename[openmp],"w")
    if openmp==1:#set the flags for cmake and write something into readme.txt
        cmake_flag="cmake .. -DENABLE_OPENMP=ON -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS="+werror
        readme.write("""VIENNACL_WITH_OPENMP\n"""+remote_address)
    elif openmp==0:
        cmake_flag="cmake .. -DENABLE_OPENMP=OFF -DCMAKE_BUILD_TYPE=Release -DENABLE_PEDANTIC_FLAGS=ON -DCMAKE_CXX_FLAGS="+werror
        readme.write("""NO_VIENNACL_WITH_OPENMP\n"""+remote_address)
    readme.close()
    
    cmd="cd "+buildfolder+";"+cmake_flag+";make franz-bench-cpu"
    text=commands.getstatusoutput(remote+"'"+cmd+"'")#cmake set flags and make the file
    print text[1]
    if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
    
    cmd=c_file+" "+str(0)+" "+str(op_choice)
    text=commands.getstatusoutput(remote+"'"+cmd+"'")#c-file aufrufen, es wird im python verzeichnis die file.txt erstellt
    print text[1]
    if int(text[0])!=0:#check if the make process has worked
        print text[0]
        print "Error during make :("
        sys.exit()
    
    cmd=""#delet the content
    
    i=min_loop #set i to the start size for the vector
    while i<max_loop: #the loop
        cmd=c_file+" "+str(i)+" "+str(op_choice)
        text=commands.getstatusoutput(remote+"'"+cmd+"'")
        print text[1]
        if int(text[0])!=0:#check if the make process has worked
            print text[0]
            print "Error during make :("
            sys.exit()
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



directory[openmp]="/home/franz/Franz/Benchmark/temp/"+remote_address+"/"+foldername+"_combi"+time.strftime("%d.%m.%Y__%H_%M_%S")+"/" # current date and time for the directory
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
print "Zeit:"+str(time.time()-start)
        
