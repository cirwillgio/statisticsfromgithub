import sys
import os
import re



interm_file=sys.argv[1]+'interm_file'
end='END'
str_url='https://github.com/'		###################
url_out=[sys.argv[1]+'2013.out',sys.argv[1]+'2014.out',sys.argv[1]+'2015.out',sys.argv[1]+'2016.out',sys.argv[1]+'2017.out']	



#str_cmd='curl -u ' + aut[0] +' '
n_url=0
m_url=1







with open (interm_file , 'r') as interm :
	for line in interm.readlines() :
		match=re.match('\"full_name\":',line)
		if not match==None :
			tmp= line.replace('\"full_name\":','').replace(' ','').replace(',','').replace('\n','').replace('{/sha}','').replace('\'','').replace('\"','')
			
			cmd= str_url + tmp
			os.system( 'echo ' + cmd +  ' >>' + url_out[n_url] +'\n' )
			continue

		mm=re.match(end,line)
		if not mm==None :
			os.system('echo '+ end + ' >>' + url_out[n_url] +'\n'  )
			m_url+=1
			end.replace('\n','')
			if m_url==13 :
				n_url+=1
				m_url=1
						










