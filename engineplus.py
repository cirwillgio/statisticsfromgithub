from lxml import html
from datetime import datetime
import sys
import os
import re
import time


yy=sys.argv[2]
a=sys.argv[3]
url_out=sys.argv[1]+yy+'.out'
s_cmd='curl -u '+a+' '
h=sys.argv[1]+'html.out'
stat_csv=sys.argv[1]+'stat'+yy+'.tsv'
commit_path='/html/body/div[4]/div/div/div[2]/div[1]/div[3]/div/div/ul/li[1]/a/span/text()'
contributors_path='/html/body/div[4]/div/div/div[2]/div[1]/div[3]/div/div/ul/li[4]/a/span/text()'
last_commit_path='/html/body/div[4]/div/div/div[2]/div[1]/div[6]/span[1]/span/relative-time/@datetime'
end='END'
day_m= [0,31,28,31,30,31,30,31,31,30,31,30,31]  		
m=1
n_commit=0
n_contributors=0
active=0
morti=0
tot_rep=0

os.system('echo \'COMMIT DAY AVERAGE\tCOMMIT REPO AVERAGE\tCONTRIBUTORS AVERAGE\tACTIVE REPO\tDEAD REPO\' >>'+stat_csv)
with open (url_out, 'r') as u :
	with open (stat_csv, 'a' ) as out :
		
		for line in u.readlines() :
			match=re.match(end,line)
			if not match==None :
				average_commit_day=n_commit/day_m[m]
				average_commit_rep=n_commit/tot_rep
				average_contributors=n_contributors/tot_rep
				os.system('echo \''+ str(average_commit_day) +'\t'+ str(average_commit_rep) +'\t' +str(average_contributors)  +'\t'+str(active)+'\t'+str(morti)+'\' >>'+stat_csv)
				#out.write(str(average_commit_day)+'\t'+str(average_commit_rep)+'\t'+str(average_contributors)+'\t'+str(vivi)+'\t'+str(morti)+'\n')
				active=0
				morti=0
				n_contributors=0
				tot_rep=0
				n_commit=0
				m+=1
				continue

			tot_rep+=1
			cmd= s_cmd +'\''+ line.replace('\n','')+'\'' + ' >'+ h
			os.system(cmd)
			time.sleep(2)
			with open (h,'r') as ht :
				rr=ht.read()
				tree = html.fromstring(rr)
				x_c=tree.xpath(commit_path)
				x_p=tree.xpath(contributors_path)
				x_l=tree.xpath(last_commit_path)
				if len(x_c)<1 :
					x_c='1'
				if len (x_p)<1 :
					x_p='1'
				if len(x_l)<1 :
					x_l=['2013-01-01',0]
				n_commit+= int ( x_c[0].replace('\n','').replace(' ','').replace(',','') )
				n_contributors+= int ( x_p[0].replace('\n','').replace(' ','').replace(',','') )
				l_com= x_l[0]
				l_commit=l_com[:10].replace('-',',')
				day=int ( l_commit[8:] )
				month=int( l_commit[5:7]) 
				year=int( l_commit[:4])
				if datetime(year,month,day)<datetime(2017,1,1) :
					morti+=1
				else :
					active+=1
