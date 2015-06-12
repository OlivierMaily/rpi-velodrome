#!/usr/bin/env python
import minimalmodbus
import time
m=minimalmodbus.Instrument('/dev/ttyAMA0',1)
global co
global pc_ete
global pc_hiver
global dec_ete
global dec_hiver
global tempZ1
global pcZ1
global tempZ2
global pcZ2
global tempZ3
global pcZ3
global tempZ4
global pcZ4
global tempZ5
global pcZ5
global Assemblage
global Mode
global Priorite
global Bloquer
global comZ1
global comZ2
global comZ3
global comZ4
global comZ5
global presZ1
global presZ2
global presZ3
global presZ4
global presZ5

m.serial.baudrate =38400
m.serial.stopbits =2
m.serial.timeout=0.250
initZ1=0
initZ2=0
initZ3=0
initZ4=0
initZ5=0
z2F=0
z2C=0
Blocage_fonctionnement=1
z1F=0
z1C= 0 
temps_dem=0
z3C=0 
z3F=0 
z4C=0 
z4F=0 
z5C=0 
z5F=0
zoneInit=0
time_init=0
time_for_vanne=0
forcage_vanne=0
m.write_register(284,0,0)
#m.write_register(32,1,0)
co_init=2
ChangerTemp=0
compteur=0
Compt=0
anticourcycle=False
#Blocage_fonctionnement=0
Write=False
class NoneException(Exception):
	def _init_(self,raison):
		self.raison=raison
	def _str_(self):
		return self.raison
class Exception_valeur(Exception):
        def _init_(self,raison):
                self.raison=raison
        def _str_(self):
                return self.raison
def writeReg(Reg,valeur,sig=False):
	ancienne=LireRegistre(Reg)
	if Reg==36:
		print 'Reg36 = ' +str(ancienne)
        if ancienne<>valeur:
        	if sig:
                	m.write_register(Reg,valeur,signed=True)
                else:
                        m.write_register(Reg,valeur)
		raise Exception_valeur('Test')
def ReadRegister(registre):
	result=m.read_register(registre,0,signed=True)
#	print 'je lis registre ' + str(registre) + ' qui a la valeur ' + str(result)
	if not isinstance(result,int):
                raise NoneException('NoneType eviter')
	else:
		return result
def LireRegistre(registre):
	while 1:
		try:
        		res=ReadRegister(registre)
		except NoneException:
			print 'None eviter'
        	except IOError:
	                print 'lecture Impossible du registre :'
                	print registre
        	except ValueError:
                	print 'lecture Impossible du registre a cause du type de valeur :'
                	print registre
        	except TypeError:
                	print 'EOF ERROR'
		else:
			return res
def EcrireRegistre(Reg,valeur,sig=False):
        global Compt
	global Write
	Write=True
        while 1:
                try:
			ancienne=LireRegistre(Reg)
#			print 'je veux ecrire registre ' + str(Reg) + ' qui a la valeur ' + str(ancienne) + ' a la valeur ' + str(valeur)
			if ancienne<>valeur:
	               		if sig:
        	               		m.write_register(Reg,valeur,signed=True)
               			else:
                       			m.write_register(Reg,valeur)
			else:
				Write=False
				print 'je n ecris pas'
                except IOError:
                        Compt+=1
			print 'ecriture Impossible du registre :'
			print Reg
		except TypeError:
                        Compt+=1
                        print 'ecriture Impossible du registre a cause de type :'
                        print Reg
                except (ValueError):
                        Compt+=1
                        print 'Ecriture impossible a cause de valeur :'
                        print Reg
		else:
			if Write:
				print 'j ecris'
			Compt=0
			Write=False
			return

def vanne():
 #       time.sleep(0.1)
        global time_init
        global ts
        global time_for_vanne
        global forcage_vanne
        global ouv_vanne
        if ouv_vanne<10:
                if time_init==0:
                        time_init=time.time()
                else:
                        if ts>time_init+21600:
                                EcrireRegistre(284,2)
                                forcage_vanne=1
                                time_for_vanne=ts
        if forcage_vanne==1:
                if ts>time_for_vanne+600:
                        EcrireRegistre(284,0)
                        forcage_vanne=0
                        time_init=0
        if ouv_vanne>10 and forcage_vanne==0:
                time_init=0

def consigne():
#        time.sleep(0.1)
        global co_init
        if co<>co_init:
                if co==1:
                        decalage_temp_ete=2000-pc_ete
                        EcrireRegistre(148,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(172,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(196,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(220,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(244,decalage_temp_ete/10,sig=True)	
                        EcrireRegistre(36,2000-dec_ete,0)
                        EcrireRegistre(37,2000+dec_ete,0)
			Blocage_fonctionnement=1
			if resistance:
		        	if Assemblage<>5:
                                	EcrireRegistre(33,5)
                        	if Priorite<>2:
                                	EcrireRegistre(34,2)

				if permResistance<>0:
					EcrireRegistre(50,0)
				if permVanneChaud<>0:
					EcrireRegistre(53,0)
			else:
				if Assemblage<>4:
					EcrireRegistre(33,4)
				
				
                else:

                        decalage_temp_hiver=max(min(1000,(2000-pc_hiver)),-1000)
                        EcrireRegistre(148,int(decalage_temp_hiver/10),sig=True)
                        EcrireRegistre(172,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(196,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(220,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(244,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(36,2000-dec_hiver,0)
                        EcrireRegistre(37,2000+dec_hiver)
			Blocage_fonctionnement=1
			if resistance:
				if Assemblage<>5:
                                	EcrireRegistre(33,5)
                        	if Priorite<>3:
                                	EcrireRegistre(34,3)
				if permResistance<>5:
					EcrireRegistre(50,5)
				if permVanneChaud<>2:
					EcrireRegistre(53,2)

			else:
				if Assemblage<>3:
					EcrireRegistre(33,3)

                co_init=co


def mode():
        global z2F
        global z2C
        global z1F
        global z1C
        global z3C
        global z3F
        global z4C
        global z4F
        global z5F
        global z5C
#       time.sleep(0.5)
        if presZ1 <>0:
                z1=1
        else:
                z1=0
		z1C=0
		z1F=0
        if presZ2 <>0:
                z2=1
        else:
                z2=0
		z2C=0
		z2F=0
        if presZ3 <>0:
                z3=1
        else:
                z3=0
		z3F=0
		z3C=0
        if presZ4 <>0:
                z4=1
        else:
                z4=0
		z4C=0
		z4F=0
        if presZ5 <>0:
                z5=1
        else:
                z5=0
		z5C=0
		z5F=0
        zoneTot=z1+z2+z3+z4+z5
	temps=time.time()
	global anticourcycle
        global zoneInit
        global Blocage_fonctionnement
	global temps_dem
        global initZ1
        global initZ2
        global initZ3
        global initZ4
        global initZ5
	global ChangerTemp
	DEC_PC_Z1=pcZ1-2000
	PC_RE_Z1=pc_ete+DEC_PC_Z1
	PC_RH_Z1=pc_hiver+DEC_PC_Z1
	DEC_PC_Z2=pcZ2-2000
        PC_RE_Z2=pc_ete+DEC_PC_Z2
        PC_RH_Z2=pc_hiver+DEC_PC_Z2
	DEC_PC_Z3=pcZ3-2000
        PC_RE_Z3=pc_ete+DEC_PC_Z3
        PC_RH_Z3=pc_hiver+DEC_PC_Z3
	DEC_PC_Z4=pcZ4-2000
        PC_RE_Z4=pc_ete+DEC_PC_Z4
        PC_RH_Z4=pc_hiver+DEC_PC_Z4
	DEC_PC_Z5=pcZ5-2000
        PC_RE_Z5=pc_ete+DEC_PC_Z5
        PC_RH_Z5=pc_hiver+DEC_PC_Z5
	TEMP_R_Z1=tempZ1-dec_z1
        TEMP_R_Z2=tempZ2-dec_z2
        TEMP_R_Z3=tempZ3-dec_z3
        TEMP_R_Z4=tempZ4-dec_z4
        TEMP_R_Z5=tempZ5-dec_z5
	#Calcul Demande Zone 1 
	if TEMP_R_Z1>PC_RE_Z1:
		z1C=0
		z1F=1
	elif TEMP_R_Z1<PC_RH_Z1:
		z1F=0
		z1C=1
	else:
		z1C=0
		z1F=0
	#Zone 2 calcul demande
        if TEMP_R_Z2>PC_RE_Z2:
		z2C=0
                z2F=1
        elif TEMP_R_Z2<PC_RH_Z2:
		z2F=0
                z2C=1
        else:
                z2C=0
                z2F=0
	#Calcul demande Zone3
        if TEMP_R_Z3>PC_RE_Z3:
		z3C=0
                z3F=1
        elif TEMP_R_Z3<PC_RH_Z3:
		z3F=0
                z3C=1
        else:
                z3C=0
                z3F=0
	#Calcul demande zone4
        if TEMP_R_Z4>PC_RE_Z4:
		z4C=0
                z4F=1
        elif TEMP_R_Z4<PC_RH_Z4:
		z4F=0
                z4C=1
        else:
                z4C=0
                z4F=0
	#calcul demande zone5
        if TEMP_R_Z5>PC_RE_Z5:
		z5C=0
                z5F=1
        elif TEMP_R_Z5<PC_RH_Z5:
		z5F=0
                z5C=1
        else:
                z5C=0
                z5F=0

	print 'z1 Chaud = ' + str(z1C) + ' // Froid = ' +str(z1F)
        print 'z2 Chaud = ' + str(z2C) + ' // Froid = ' +str(z2F)
        print 'z3 Chaud = ' + str(z3C) + ' // Froid = ' +str(z3F)
	
        if co==1:
		print 'anticourcycle = '+str(anticourcycle)
                if ((z1F or z2F or z3F or z4F or z5F) and Assemblage==6 and ChangerTemp==0 and not anticourcycle):
                   	
			if Assemblage<>5:
                                EcrireRegistre(33,5)
                        if Priorite<>3:
                                EcrireRegistre(34,2)
			
                        ChangerTemp=1
			temps_dem=temps
			anticourcycle=True
			print 'TEmps dem='+str(temps_dem)
                elif  (not (z1F or z2F or z3F or z4F or z5F) and (z1C or z2C or z3C or z4C or z5C) and Assemblage==5 and ChangerTemp==0 and not anticourcycle):
                        if Assemblage<>6:
                                EcrireRegistre(33,6)
                        if Mode<>1:
                                EcrireRegistre(70,1)
                        ChangerTemp=2
			temps_dem=temps
			print 'Temps_dem ='+str(temps_dem)
			anticourcycle=True
                if ChangerTemp==1:
                        decalage_temp_ete=2000-pc_ete
                        EcrireRegistre(148,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(172,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(196,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(220,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(244,decalage_temp_ete/10,sig=True)
                        EcrireRegistre(36,2000-dec_ete)
                        EcrireRegistre(37,2000+dec_ete)
                        ChangerTemp=0
                        Blocage_focntionnement=1
                elif ChangerTemp==2:
			decalage_temp_hiver=2000-pc_hiver
                        EcrireRegistre(148,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(172,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(196,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(220,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(244,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(36,2000-dec_hiver)
                        EcrireRegistre(37,2000+dec_hiver)
                        ChangerTemp=0
                        Blocage_fonctionnement=1
	if anticourcycle:
		if (temps>temps_dem+600):
			anticourcycle=False
        if Blocage_fonctionnement==1:
                if Bloquer<>2:
                        zoneInit=0
                        initZ1=0
                        initZ2=0
                        initZ3=0
                        initZ4=0
                        initZ5=0
                        EcrireRegistre(32,2)
                if z1==1 and comZ1<2 and initZ1==0:
                        initZ1=1
                        zoneInit+=1
                if z2==1 and comZ2<2 and initZ2==0:
                        zoneInit+=1
                        initZ2=1
                if z3==1 and comZ3<2 and initZ3==0:
                        zoneInit+=1
                        initZ3=1
                if z4==1 and comZ4<2 and initZ4==0:
                        zoneInit+=1
                        initZ4=1
                if z5==1 and comZ5<2 and initZ5==0:
                        zoneInit+=1
                        initZ5=1
                if zoneInit==zoneTot:
                        if Bloquer<>1:
                                EcrireRegistre(32,1)
                                Blocage_fonctionnement=0


EcrireRegistre(71,0)
EcrireRegistre(72,0)
resistance_init=LireRegistre(285)
while 1:
	time.sleep(0.5)
	test=LireRegistre(148)
	pc_hiver=LireRegistre(81)
        pc_ete=LireRegistre(82)
        dec_hiver=LireRegistre(83)
	dec_ete=LireRegistre(84)
	ouv_vanne=LireRegistre(21)
        co=LireRegistre(12)
        tempZ1=LireRegistre(146)
        pcZ1=LireRegistre(147)
        tempZ2=LireRegistre(170)
        pcZ2=LireRegistre(171)
        tempZ3=LireRegistre(194)
        pcZ3=LireRegistre(195)
        tempZ4=LireRegistre(218)
        pcZ4=LireRegistre(219)
        tempZ5=LireRegistre(242)
        pcZ5=LireRegistre(243)
        Assemblage=LireRegistre(33)
        Mode=LireRegistre(70)
        Priorite=LireRegistre(34)
	Reg36=LireRegistre(36)
        Bloquer=LireRegistre(32)
        comZ1=LireRegistre(157)
        comZ2=LireRegistre(181)
        comZ3=LireRegistre(205)
        comZ4=LireRegistre(229)
        comZ5=LireRegistre(253)
        presZ1=LireRegistre(140)
        presZ2=LireRegistre(164)
        presZ3=LireRegistre(188)
        presZ4=LireRegistre(212)
        presZ5=LireRegistre(236)
	permResistance=LireRegistre(50)
	permVanneChaud=LireRegistre(53)
	dec_z1=LireRegistre(148)*10
        dec_z2=LireRegistre(172)*10
        dec_z3=LireRegistre(196)*10
        dec_z4=LireRegistre(220)*10
        dec_z5=LireRegistre(244)*10
	autor_res=LireRegistre(285)
	print "autorisation resistance= " + str(autor_res)
	if LireRegistre(77)==0:
		EcrireRegistre(285,2)
		EcrireRegistre(77,1)
	if resistance_init<>autor_res:
		co_init=3
		resistance_init=autor_res
	if co==0:
		if autor_res==3 or autor_res==2:
			resistance=True
		else:
			resistance=False
	else:
		if autor_res==4 or autor_res==2:
			resistance=True
		else:
			resistance=False 
        time.sleep(0.5)
        ts=time.time()

        vanne()
        consigne()
	if resistance:
	        mode()
