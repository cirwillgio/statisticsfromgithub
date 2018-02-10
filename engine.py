from __future__ import division
from aut import aut
import sys
import os
import re
import time
import datetime

### contatore tutti linguaggi non studiati   , variabili tot_complessivo



cmd_file=sys.argv[1]+'cmd_file.sh'
a_out=sys.argv[1]+'a.out'
stat_file=sys.argv[1]+'stat_file.tsv'
interm_file=sys.argv[1]+'interm_file'
months= ['0','January','February','March','April','May','June','July','August ','September','October','November','December']  
day_m= [0,31,28,31,30,31,30,31,31,30,31,30,31]  		
languages=['\"Shell\"','\"Python\"','\"JavaScript\"','\"PHP\"','\"Ruby\"','\"Makefile\"','\"Java\"','\"Go\"','null']	 		 	 	 	
statistics=['\"total_count\":','\"items\":','\"language\":','\"stargazers_count\":','\"full_name\":' ]   #,'\"id\":','\"full_name\":'  
end='END'
count=1
shell=0
python=0
javascript=0
php=0
ruby=0
makefile=0
java=0
go=0
null=0
others=0
c_month=1
tot_rep=''
yy=sys.argv[2] 
end_year=sys.argv[3]
start=yy
top=True
end_month=False
tot_language_year=[0,0,0,0,0,0,0,0,0,0]
tot_rep_year=0
ccc=0
tot_rep_month=0
tmp_yy=yy
cont_mese=0
per_page='&per_page=1\''
rep_star=0
n_rep=1
tot_average_year=1.0







#####to respect github rate-limit  2 sec delay for every query, the results are writes in a.out 




with open ( cmd_file , 'r' ) as r :
	for line in r.readlines() :
		os.system(line)
		time.sleep(2)












#read every elements and for each one write in interm_file the statistics that interest us 

with open (a_out, 'r') as a :
	with open (interm_file,'a') as st  :
 		for line in a.readlines() :
			tmp=line.replace(" ","").replace('\n','')

		
					
			for stat in statistics :
				match=re.match(stat,tmp) 
				if not match == None :
					if stat== statistics[0]:
						st.write(months[ count ]+'\n')

					
					if stat==statistics[3] :
						tmp=line.replace('\"stargazers_count\":','').replace(' ','').replace(',','').replace('\n','')
						rep_star+=int(tmp)
						n_rep+=1

							
					if stat==statistics[2] :
						cont_mese+=1
						tmp=line.replace('\"language\":','').replace(' ','').replace(',','').replace('\n','')
					

					st.write(tmp+'\n')	
					continue
				
		
			mamatch=re.match('EENNDD',line)
			if not mamatch==None :
				ccc+=1


			m=re.match('ENDMONTH',line)
			if not m==None :
				st.write('CONTATIMESE:' + str (cont_mese ) + '\n')
				st.write('MEDIASTELLEMESE:' + str (rep_star/n_rep ) + '\n')
				st.write(end + '\n')
				rep_star=0
				n_rep=0
				ccc=0
				cont_mese=0
				count+=1
				if count==13 :
					tmp_yy=int(tmp_yy)+1
					count=1
					if tmp_yy==2016 :
						day_m[2]=29
					else :
						day_m[2]=28





######### read interm_file line by line and build the stat_file.tsv


with open (interm_file , 'r') as interm :
	with open (stat_file , 'a') as st :
		st.write('MONTH\tYEAR\tTOTAL COUNT\tMONTHLY  STAR AVERAGE\tShell\tPython\tJavascript\tPHP\tRuby\tMakefile\tJava\tGo\tNull\tOthers\n')
		for line in interm.readlines() :
			

			
			for language in languages :
				l=re.match(language,line)
				if not l == None :
					if language==languages[0] :
						shell+=1
					elif language==languages[1] :
						python+=1
					elif language==languages[2] :
						javascript+=1
					elif language==languages[3] :
						php+=1
					elif language==languages[4] :
						ruby+=1
					elif language==languages[5] :
						makefile+=1
					elif language==languages[6] :
						java+=1
					elif language==languages[7] :
						go+=1
					elif language==languages[8] :
						null+=1

					continue



			
			s=re.match('MEDIASTELLEMESE:',line)
			if not s==None :
				tmp_s=line
				average= float( tmp_s.replace('MEDIASTELLEMESE:','').replace('\n','')  )
				continue
			
						
			
	
			
			
			t=re.match('CONTATIMESE:',line)
			if not t == None :
				tot_rep=line
				tot_rep_month= int(  tot_rep.replace('CONTATIMESE:','').replace('\n','')  )
				continue 



			eq=re.match('END',line)
			if not eq==None :
				others=tot_rep_month-(shell+python+javascript+php+ruby+makefile+java+go+null)
				st.write( months[ c_month ] + " \t" + str ( yy ) + '\t'  + str( tot_rep_month ) + '\t'  + str(int(average)) +'\t'+  str( shell ) + '\t' + str( python ) + '\t'  + str( javascript ) + '\t' + str( php ) + '\t' + str( ruby ) + ' \t' + str( makefile ) + '\t' + str( java ) + '\t' + str( go ) + '\t' + str( null ) + '\t' + str( others ) +  '\n'  )
				tot_language_year[0]+=shell
				tot_language_year[1]+=python
				tot_language_year[2]+=javascript
				tot_language_year[3]+=php
				tot_language_year[4]+=ruby
				tot_language_year[5]+=makefile
				tot_language_year[6]+=java
				tot_language_year[7]+=go
				tot_language_year[8]+=null
				tot_language_year[9]+=others
				tot_rep_year+= tot_rep_month
				c_month+=1
				tot_average_year+=average
				if c_month==13 :
					st.write( '\n' + 'YEAR : ' + str( yy ) + '\t\t'+ 'total_count:' + str( tot_rep_year ) + '\t' + 'year star average:' + str(tot_average_year/12) + '\t\t' + str(tot_language_year[0] ) + '\t' + str(tot_language_year[1] ) + '\t'  + str( tot_language_year[2] ) + '\t\t' + str(tot_language_year[3] ) + '\t' + str( tot_language_year[4] ) + '\t' + str( tot_language_year[5] ) + '\t' + str( tot_language_year[6] ) + '\t' + str( tot_language_year[7] ) + '\t' + str( tot_language_year[8] )  + '\t' + str( tot_language_year[9] )  + '\n\n'  )					
					tot_average_year=0
					tot_rep_year=0
					tot_language_year=[0,0,0,0,0,0,0,0,0,0]					
					yy=int(yy)+1
					if yy==2016 :
						day_m[2]=29
					else :
						day_m[2]=28

					if yy==(int(end_year)+1) :
						end_month=True
					c_month=1
				tot_rep_month=0
				tot_rep=''
				shell=0
				python=0
				javascript=0
				php=0
				ruby=0
				makefile=0
				java=0
				go=0
				others=0
				null=0
				average=0
			



							



#os.system('rm '+interm_file)




				

			






			
			

		
