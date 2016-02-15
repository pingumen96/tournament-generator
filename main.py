"""17/05/2015 - iniziata la creazione del costruttore
	18/05/2015 - aggiunto l'ordinamento alfabetico successivo all'inserimento dei dati
	09/06/2015 - aggiunto ciclo for con il quale diventa possibile generare le giornate
	25/06/2015 - completata la generazione delle giornate (anche con gestione squadre
				dispari) e dei gironi
	28/06/2015 - completata eliminazione diretta con controllo per fare in modo che il
				numero di squadre inserite sia potenza di due
	29/06/2015 - iniziata gestione dell'inserimento dati da parte dell'utente
	03/07/2015 - iniziata parte per la generazione di file esterno in XML
	04/07/2015 - correzione di un errore logico presente in avvio
	05/07/2015 - importata libreria SAX, corretto un bug nella generazione dei gironi,
				migliorata gestione file xml e corretti bug minori
	06/07/2015 - iniziata divisione tra classe Torneo e classe File, dichiarata funzione
				di lettura da xml, tolta importazione libreria SAX
	07/07/2015 - creata bozza di lettura da xml (solo per campionati), fixato (forse)
				un bug nella funzione type_selector riguardante il numero di gironi
	08/07/2015 - lettura da file xml è funzionante, la struttura dati memorizza quanto
				salvato in maniera corretta. Creata classe Menu per occuparsi
				dell'interazione iniziale con l'utente
	09/07/2015 - i bottoni iniziali son funzionanti, altrettanto per quanto riguarda
				l'apertura di un file esterno a scelta (utilizzo di filedialog)"""
from random import shuffle
from math import log
import xml.etree.ElementTree as ElementTree
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
class File:
	def load(self):
		filename=askopenfilename(filetypes=[('File XML','*.xml')])
		#funzione sulla quale bisogna lavorare ancora molto
		"""migliorare nomi variabili, vedere se è possibile strutturare la funzione in
		modo migliore"""
		#c=campionato, ed=eliminazione diretta, g=gironi
		self.f=open(filename,"r")
		tree=ElementTree.parse(filename)
		root=tree.getroot() #parte da <torneo>
		"""visualizzazione dei dati funziona correttamente, da fare salvataggio in
		struttura dati"""
		partite=[]
		if root.get('tipo')=='c':
			print(root.tag,root.attrib)
			#quello che segue legge i campionati
			for child in root.findall('giornata'):
				temp=[]
				print("Giornata",child.get('numero'))
				for x in child.findall('partita'):
					temp.append(x.text)
					print(x.text)
				partite.append(temp)
			#finita lettura campionati
		elif root.get('tipo')=='ed':
			print(root.get('nome'))
			#quello che segue legge i tornei a eliminazione diretta
			for child in root.findall('eliminazione_diretta'):
				for x in child.findall('partita'):
					partite.append(x.text)
					print(x.text)
			#fine lettura tornei a eliminazione diretta
		elif root.get('tipo')=='g':
			print(root.get('nome'))
			for child in root.findall('girone'):
				temp=[]
				print("Girone",child.get('nome_girone'))
				for x in child.findall('giornata'):
					temp2=[]
					print("Giornata",x.get('numero'))
					for y in x.findall('partita'):
						temp2.append(y.text)
						print(y.text)
						pass
					temp.append(temp2)
				partite.append(temp)
			print(partite)
			pass
		else:
			messagebox.showerror('File non valido','Il file xml aperto non è valido.')
		


	def new(self,filename,tournament_type):
		"""Fare try/except per creazione file, gestire file già presente"""
		try:
			self.f=open(filename+".xml","w")
			self.f.write('<?xml version="1.0"?>\n')
			self.f.write('<torneo nome="'+filename+'" tipo="'+tournament_type+'">\n')
		except IOError:
			print("Non è possibile creare il file.")
		else:
			print("Il file è stato creato con successo.")

	def append_function(self,xml_string):
		if self.f!=None:
			if xml_string!=None:
				self.f.write(xml_string)
			else:
				return 0;
	def __init__(self,filename,opening_mode): #parte da migliorare, non indispensabile per ora
		if opening_mode=="r":
			self.load(filename)
		elif opening_mode=="w":
			self.new(filename)
			pass
		else:
			print("Non è stata specificata alcuna modalità d'apertura.")
		pass

class Torneo(File):
	"""Gestione torneo"""
	"""La funzione championship deve, data una lista di squadre come parametro, generare
		le giornate per tutto il campionato"""
	def championship(self,lista):
		partite=[]
		shuffle(lista)
		for i in range(len(lista)-1):
			giornata=[]
			print("Giornata",i+1)
			self.append_function('\t<giornata numero="'+str(i+1)+'">\n\t')
			for j in range(round(len(lista)/2)):
				if i%2 or lista[j]=="Riposo":
					print(lista[len(lista)-j-1],"-",lista[j])
					giornata.append((lista[len(lista)-j-1]+"-"+lista[j]))
					self.append_function('\t\t<partita>'+lista[len(lista)-j-1]+"-"+lista[j]+"</partita>\n\t")
				else:
					print(lista[j],"-",lista[len(lista)-j-1])
					giornata.append((lista[j]+"-"+lista[len(lista)-j-1]))
					self.append_function('\t\t<partita>'+lista[j]+"-"+lista[len(lista)-j-1]+"</partita>\n\t")
			self.append_function('\t</giornata>\n')
			partite.append(giornata)
			temp=lista.pop()
			lista.insert(1,temp)
		return partite;
	"""La funzione rounds deve splittare la lista e crearne altre, generando così i gironi e dando
		a questi un nome."""
	def rounds(self,lista,pl_per_girone):
		shuffle(lista)
		alfabeto=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
		partite=[]
		pl_gironi=[] #questa lista conterrà i gironi
		l_pl_gironi=[] #questa lista conterrà le squadre di ogni girone
		i=0
		for x in range(round(len(lista)/pl_per_girone)):
			self.append_function('\t<girone nome_girone="'+alfabeto[x]+'">\n\t')
			print("Girone",alfabeto[x])
			for y in range(i,pl_per_girone+i):
				l_pl_gironi.append(lista[y])
			i=i+pl_per_girone
			if len(l_pl_gironi)%2:
				lista.append("Riposo")
			pl_gironi.append(l_pl_gironi)
			partite.append(self.championship(l_pl_gironi))
			l_pl_gironi=[]
			self.append_function('</girone>\n')
	"""La funzione ko_stage deve, data una lista di squadre in input (che dev'essere potenza
		di 2), generare un tabellone"""
	def ko_stage(self,lista):
		if log(len(lista),2)%1==0:
			shuffle(lista)
			partite=[]
			self.append_function('\t<eliminazione_diretta>\n\t')
			for x in range(round(len(lista)/2)):
				print(lista[len(lista)-x-1],"-",lista[x])
				partite.append((lista[len(lista)-x-1],"-",lista[x]))
				self.append_function('\t<partita>'+lista[len(lista)-x-1]+'-'+lista[x]+'</partita>\n\t')
			self.append_function('</eliminazione_diretta>\n')
		else:
			print("La lista è di una dimensione non corretta")
		pass
	def type_selector(self,type):
		#c = campionato, g = gironi, ed = eliminazione diretta
		if type=="c":
			self.championship(self.players)
		elif type=="g":
			print("Quante squadre vuoi avere in ogni girone?")
			while True:
				try:
					teams_per_round=int(input("Inserisci un numero: "))
					break
				except ValueError:
					print("Si prega di inserire un numero.")
			while (teams_per_round>len(self.players)/2 and len(self.players)%2==0) or len(self.players)%teams_per_round>=1 or len(self.players)%teams_per_round==teams_per_round-1:
				print("Non è possibile creare i gironi con il numero di squadre scelto. Riprovare.")
				teams_per_round=int(input())
				pass
			self.rounds(self.players,teams_per_round)
		elif type=="ed":
			self.ko_stage(self.players)
		else:
			print("La tipologia di torneo inserita non è corretta")

	"""INIZIALIZZAZIONE CLASSE"""
	def __init__(self):
		"""Costruttore, crea nuovo torneo prendendo in input numero dei partecipanti.
		Utilizzo delle liste. Si deve occupare di predisporre una struttura dati
		adatta a contenere i nomi dei partecipanti."""
		print("Per prima cosa, dai un nome al torneo.")
		self.nome_torneo=input()
		print("Adesso decidi il numero di partecipanti.")
		print("Ricorda che per poter creare un torneo a eliminazione diretta è necessario che il numero sia una potenza di 2.")
		while True:
			try:
				self.n_players=int(input("Inserisci un numero: "))
				break
			except ValueError:
				print("Si prega di inserire un numero.")
		print("Ora decidi la tipologia di torneo seguendo questa legenda:")
		print("c = campionato")
		print("g = gironi")
		print("ed = torneo ad eliminazione diretta")
		type=input()
		while type!="ed" and type!="c" and type!="g":
			print("La tipologia di torneo inserita non è valida. Riprovare.")
			type=input()
			pass
		while type=="ed" and log((self.n_players),2)%1!=0:
			print("Inserire un numero di partecipanti corretto (potenza di 2).")
			while True:
				try:
					self.n_players=int(input())
					break
				except ValueError:
					print("Si prega di inserire un numero.")
		self.players=[]
		for x in range(0,self.n_players):
			print("Inserisci nome del",x+1,"partecipante")
			y=input()
			while y=='':
				y=input("Partecipante non inserito. Riprova.")
			self.players.append(y)
		if len(self.players)%2:
			self.players.append("Riposo")
		print(len(self.players))
		self.f=None
		risp=input("Si vuole salvare il torneo in un file esterno? (s/n)")
		while risp!="s" and risp!="n":
			print("Inserire risposta corretta.")
			risp=input()
		if risp=="s":
			self.new(self.nome_torneo,type)
			pass
		self.type_selector(type)
		self.append_function("</torneo>")
		if self.append_function(None):
			self.f.close()

"""INIZIO PARTE WORK IN PROGRESS"""
#template per il wizard della creazione dei tornei
class WizardStepTemplate():
	#480x360
	def __init__(self,master=None):
		tk.Frame.__init__(self,master)
		pass
	pass
"""FINE PARTE WORK IN PROGRESS"""

#la classe Menu si dovrà occupare SOLO dell'interazione con l'utente
#c'è molto da lavorarci
class Menu(Torneo,tk.Frame):
	#rendere disponibili caricamento di torneo esterno o creazione nuovo torneo
	def __init__(self,master=None):
		tk.Frame.__init__(self,master)
		self.grid() #gestisce la geometria della finestra
		self.createWidgets()
	def createWidgets(self):
		self.benvenuto=tk.Label(self,text='Benvenuto nel software di creazione dei tornei!')
		self.newbutton=tk.Button(self,text='Nuovo torneo',anchor='center',command=lambda:Torneo.__init__(self)) #funziona
		self.newbutton.grid()
		self.loadbutton=tk.Button(self,text='Carica torneo',anchor='center',command=lambda:self.load())
		self.loadbutton.grid()

def main():

	print("Benvenuto in Generatore Campionati & Tornei 0.4.0")
	print("In questo software potrai generare un campionato, dei gironi o un torneo a eliminazione diretta.")
	torneo=Menu()
	torneo.master.title('Generatore tornei 0.4.0')
	torneo.mainloop()
main()
