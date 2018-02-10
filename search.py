import sys
import os , getopt
import time
import re 
from aut import aut

usage = 'usage: '+ sys.argv[0] + ' -i <input dir path>  -s <start year> -e <endyear> -k <key word>\n\n'+'OPTIONS : \n' + '-i,--input          path of directory\n ' + '-s,--start          start year\n ' + '-e,--end          end year\n ' + '-k,--key          keyword to search\n ' 
path_name=''
info=''
strt_yy=0
end_yy=0
key=''
############lanciare engine cosi

try:
	opts, args = getopt.getopt(sys.argv[1:],'hi:s:e:k:', ['help','input=','start=','end=','key='])	
except getopt.GetoptError:
	print usage
	sys.exit(2)
for opt, arg in opts:
        if opt == '-h':
        	print usage
        	sys.exit()
      	elif opt in ('-i', '--input'):
         	path_name = arg
	elif opt in ('-s', '--start'):
         	strt_yy = arg
	elif opt in ('-e', '--end'):
         	end_yy = arg
	elif opt in ('-k', '--key'):
         	key = arg

if path_name=='' or strt_yy==0 or end_yy==0 or key=='' :
	print usage
	sys.exit()

cmd_string='curl -u ' + aut + ' \'https://api.github.com/search/repositories?q=' + key + '+created%3A'
cmd_string_info='curl -u ' + aut + ' -I \'https://api.github.com/search/repositories?q=' + key + '+created%3A' 
per_page='&per_page=100\''
cmd_file=path_name+'cmd_file.sh'
a_out=path_name+'a.out'
info_out=path_name+'info.out'
day_m=[0,31,28,31,30,31,30,31,31,30,31,30,31]
day=1
yy=strt_yy 		
end=end_yy




def write_cmd (page,tmp_yy,mm,day) :
	i=1
	cmd=''
	if mm <10 :
		mm='0'+ str (mm)
	if day <10 :
		day='0'+ str (day)
	for _ in range(int(page))	:
		if i<10 :
			i='0'+str(i)
					
		cmd+= cmd_string  + str( tmp_yy ) + '-' + str ( mm ) + '-' + str( day ) + per_page.replace('\'','') + and_page + i + '\'' + '>>' + a_out +  '\n'
		i=int(i)+1
	cmd+='echo EENNDD >>'+a_out+'\n'
	return cmd





# take info about number of repository pages and write it in info.out


with open (cmd_file, 'a') as out :
	os.system( 'chmod u+x ' + cmd_file )
	tmp_yy=yy   
	mm=1
	while  ( tmp_yy <= end ) :   
		for i in range(12) :   
			if mm <= 9 : 
				mm='0'+ str ( mm )
			
			loop_day=str (mm).replace('0','')
			for _ in range (day_m[int (loop_day ) ]) :
				if day <= 9 : 
					day='0'+ str ( day )
				
				cmd=cmd_string_info + str( tmp_yy ) + '-' + str ( mm ) + '-' + str( day ) + per_page + ' >> '+info_out 	
				os.system(cmd)
				time.sleep(2)
				day= int (day)+1
			mm  = int ( mm ) +1
			day=1
		tmp_yy  +=1
		mm  =1
	

	










#####reads info.out and write cmd.sh (one string to one repository page )

##################################
tmp_yy=yy
item=False
complete=False
first=True
mm=1
http='HTTP'
and_page='&page='
link_string='Link:' 
remove= link_string + str( tmp_yy ) + '-' + str ( mm ) + '-' + str( day ) + per_page
remove_string='>; rel=\"next\", <https://api.github.com/search/repositories?q=' + key + '+created%3A' 
remove_string3='>; rel=\"last\"'
end_month='echo ENDMONTH >>'+a_out+'\n'
#################################

with open (cmd_file , 'a') as out :
	with open(info_out , 'r' ) as r :
		for line in r.readlines() :
			match1=re.match(http,line)
			if not match1==None :
				if not complete :
					if not first :
						cmd=write_cmd(1,tmp_yy,mm,day)
						out.write(cmd)
						complete=False
						day+=1
						if day > day_m[mm] :  
							day=1
							out.write(end_month)
							mm+=1
							if mm==13 :
								mm=1
								tmp_yy+=1
								if tmp_yy==2016 :
									day_m[2]=29
								else :
									day_m[2]=28


					else :
						first=False
				item=True
				continue
			

			i=1
			match2=re.match( link_string , line )
			if not match2==None :
				complete=True
				page= line.replace( remove_string3,'').replace('\n','')
				page=page[len(page)-2]
				cmd = write_cmd(page,tmp_yy,mm,day)
				out.write(cmd)
				day+=1
				if day > day_m[mm] : 
					out.write(end_month)
					day=1
					mm+=1
					if mm==13 :
						mm=1
						tmp_yy+=1
						if tmp_yy==2016 :
							day_m[2]=29
						else :
							day_m[2]=28
	




os.system('python engine.py '+ path_name + ' ' + str(yy) + ' ' + str(end) +'\n' ) 

#os.system('rm '+info_out)



