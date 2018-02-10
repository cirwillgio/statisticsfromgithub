# statisticsfromgithub
sript to estrapolate statiscs from github by a keyword

##Lo script da eseguire e' search.py, prende come parametro il path della cartella da usare per output


	es.	$ python search.py -i /home/prova/




##Per funzionare nella directory indicata sopra deve esserci un file aut.py con la seguente stringa all'interno:


aut='username:psw'

dove username e psw sono le credenziali dell'utente per accedere a github




##Statistiche aggiuntive eseguendo impl_url , prende come parametri path della cartella da usare per output


	es	$ python impl_url.py /home/prova 2015 user:git


###per funzionare necessita del file interm_file,generato dalla computazione di search,nella directory indicata sopra 
###inoltre per visualizzare le statistiche bisognerà successivamente lanciare lo script engineplus.py  prende come parametri :
###path della cartella da usare per output, anno da analizzare , user:psw




##La computazione effettua :

-1826 query iniziali(search.py) con lo scopo di sapere quante pagine di repository ci sono da analizzare per ogni giorno dal 2013-01-01 al 2017-12-31 

-3000 query circa(considerando che ogni giorno abbia ,1 pagina(2013 e 2014) o 2 pagine (resto del periodo) in media,di repository e quindi ci sia bisogno di 1 o 2 query per avere tutti i risultati relativi al giorno )

###Ogni query impiega circa 1sec per avere una risposta e viene rallentata di altri 2sec per rispettare il rate-limit di github, quindi in totale circa 4 ore di computazione



##Per test modificare in search.py 
-riga 36 e 37 , sostituire yy=2013(anno inizio) con un anno maggiore per restringere il range o end=2017 sempre restringendo il range.




##Lo script genera i seguenti file :


-cmd.sh		nel quale ogni riga � una query riguardante un giorno(un giorno pu� avere pi� query in base al num. di repository creati in quel giorno,100 risultati per query)


-a.out		nel quale sono presenti le risposte alle query sui singoli giorni


-stat_file.tsv	nel quale vengono mostrate le informazioni raccolte dalle query e organizzate




##Nel repository sono presenti i seguenti file :


-search.py		genera ed esegue comandi    


-engine.py		organizza e stampa risultati


-impl_url.py		crea comandi per statistiche aggiuntive


-engineplus.py		organizza e stampa statistiche aggiuntive	


-aut.py			con le credenziali github


-out.gitignore	per ignorare il file con le credenziali durante i commit
