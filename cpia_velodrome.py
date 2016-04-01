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
global pc_horsgel
global pc_Inoc_Chaud
global pc_Inoc_Froid

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
#m.write_register(280,1)
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
#	notWrite=False
#	ancienne=LireRegistre(Reg)
#	time.sleep(0.1)
#	if Reg==36:
#		if valeur<1000 or valeur >2000:
#			notWrite=True	
#			print 'J essaye d ecrire le Reg36 a la valeur = ' +str(ancienne) + ' qui etait a la valeur = ' + str(ancienne)
#        if (ancienne<>valeur) and not  notWrite:
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


def ReadRegisters(registre,nbreg):
        result=m.read_registers(registre,nbreg,functioncode=3)
#       print 'je lis registre ' + str(registre) + ' qui a la valeur ' + str(result)
        #if not isinstance(result,int):
        #        raise NoneException('NoneType eviter')
        #else:
        return result
def LireRegistres(registre,nbreg):
        while 1:
                try:
                        res=ReadRegisters(registre,nbreg)
                except NoneException:
                        print 'None eviter'
                except IOError:
                        print 'lecture Impossible du registre :'
                        print registre
                except ValueError:
                        print 'lecture Impossible du registre a cause du type de valeur :'
                        print registre
 #               except TypeError:
  #                      print 'EOF ERROR'
                else:
                        return res


def EcrireRegistre(Reg,valeur,sig=False):
        global Compt
	global Write
	
	Write=True
        while 1:
        	notWrite=False
	        try:
			ancienne=LireRegistre(Reg)
			time.sleep(0.1)
#        		if Reg==36:
#                		if valeur<1000 or valeur >2000:
#                        		notWrite=True
                        
#					print 'J essaye d ecrire le Reg36 a la valeur = ' +str(ancienne) + ' qui etait a la valeur = ' + str(ancienne)
#        		if Reg==37:
#				if valeur <2000 or valeur>3000:
#					notWrite=True
			if (ancienne<>valeur) and not  notWrite:

#			print 'je veux ecrire registre ' + str(Reg) + ' qui a la valeur ' + str(ancienne) + ' a la valeur ' + str(valeur)
			#if ancienne<>valeur:
	               		if sig:
        	               		m.write_register(Reg,valeur,signed=True)
               			else:
                       			m.write_register(Reg,valeur)
			else:
				Write=False
#				print 'je n ecris pas'
                except IOError:
                        Compt+=1
#			print 'ecriture Impossible du registre :'
#			print Reg
		except TypeError:
                        Compt+=1
   #                     print 'ecriture Impossible du registre a cause de type :'
    #                    print Reg
                except (ValueError):
                        Compt+=1
  #                      print 'Ecriture impossible a cause de valeur :'
 #                       print Reg
		else:
#			if Write:
#				print 'j ecris'
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
        if presZ1 <>0:
                z1=1
        else:
                z1=0
         #       z1C=0
        #        z1F=0
        if presZ2 <>0:
                z2=1
        else:
                z2=0
       #         z2C=0
      #          z2F=0
        if presZ3 <>0:
                z3=1
        else:
                z3=0
     #           z3F=0
    #            z3C=0
        if presZ4 <>0:
                z4=1
        else:
                z4=0
    
        if presZ5 <>0:
                z5=1
        else:
                z5=0
             
        global co_init
        if co<>co_init:
                if co==1:
                        decalage_temp_ete=2000-pc_ete
                        if z1:
				EcrireRegistre(148,decalage_temp_ete/10,sig=True)
                        if z2:
				EcrireRegistre(172,decalage_temp_ete/10,sig=True)
                        if z3:
				EcrireRegistre(196,decalage_temp_ete/10,sig=True)
                        if z4:
				EcrireRegistre(220,decalage_temp_ete/10,sig=True)
                        if z5:
				EcrireRegistre(244,decalage_temp_ete/10,sig=True)	
                        EcrireRegistre(36,2000-dec_ete,0)
                        EcrireRegistre(37,2000+dec_ete,0)
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_ete)
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_ete)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_ete)
			Blocage_fonctionnement=1
			if resistance:
		        	if Assemblage<>4:
                                	EcrireRegistre(33,4)
				if permResistance<>0:
					EcrireRegistre(50,0)
				if permVanneChaud<>0:
					EcrireRegistre(53,0)
			else:
				if Assemblage<>4:
					EcrireRegistre(33,4)
				
				
                else:

                        decalage_temp_hiver=max(min(1000,(2000-pc_hiver)),-1000)
                        if z1:
				EcrireRegistre(148,int(decalage_temp_hiver/10),sig=True)
                        if z2:
				EcrireRegistre(172,decalage_temp_hiver/10,sig=True)
                        if z3:
				EcrireRegistre(196,decalage_temp_hiver/10,sig=True)
                        if z4:
				EcrireRegistre(220,decalage_temp_hiver/10,sig=True)
                        if z5:
				EcrireRegistre(244,decalage_temp_hiver/10,sig=True)
                        EcrireRegistre(36,2000-dec_hiver,0)
                        EcrireRegistre(37,2000+dec_hiver)
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_hiver)
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_hiver)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_hiver)
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
        print 'inoc chaud'
        print pc_Inoc_Chaud
        print First_Reg[38]
        print 'inoc froid'
        print pc_Inoc_Froid
        print First_Reg[39]
        print 'antigel'
        print pc_horsgel
        print First_Reg[40]


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
	TEMP_R_Z1=tempZ1-dec_z1*10
        TEMP_R_Z2=tempZ2-dec_z2*10
        TEMP_R_Z3=tempZ3-dec_z3*10
        TEMP_R_Z4=tempZ4-dec_z4*10
        TEMP_R_Z5=tempZ5-dec_z5*10
	print "temperature reele z1 "+ str(TEMP_R_Z1) 

#<<<<<<< HEAD
	Z1_Derog=(mode_z1==2)
	Z2_Derog=(mode_z2==2)
        Z3_Derog=(mode_z3==2)
        Z4_Derog=(mode_z4==2)
        Z5_Derog=(mode_z5==2)
        Z1_Veille=(mode_z1==3) or fen_z1 or (fen_z2 and (presZ1==presZ2)) or (fen_z3 and (presZ1==presZ3)) or (fen_z4 and (presZ1==presZ4)) or (fen_z5 and (presZ1==presZ5))
        Z2_Veille=(mode_z2==3) or fen_z2 or (fen_z1 and (presZ1==presZ2)) or (fen_z3 and (presZ2==presZ3)) or (fen_z4 and (presZ2==presZ4)) or (fen_z5 and (presZ2==presZ5))
        Z3_Veille=(mode_z3==3) or fen_z3 or (fen_z1 and (presZ1==presZ3)) or (fen_z2 and (presZ2==presZ3)) or (fen_z4 and (presZ3==presZ4)) or (fen_z5 and (presZ3==presZ5))
        Z4_Veille=(mode_z4==3) or fen_z4 or (fen_z1 and (presZ1==presZ4)) or (fen_z2 and (presZ2==presZ4)) or (fen_z3 and (presZ3==presZ4)) or (fen_z5 and (presZ4==presZ5))
        Z5_Veille=(mode_z5==3) or fen_z5 or (fen_z1 and (presZ1==presZ5)) or (fen_z2 and (presZ2==presZ5)) or (fen_z3 and (presZ3==presZ5)) or (fen_z4 and (presZ4==presZ5))
	Zone_Derog=Z1_Derog or Z2_Derog or Z3_Derog or Z4_Derog or Z5_Derog
	print "derogation z1 = " + str(Z1_Derog) + " ,z2 = " + str(Z2_Derog) + " ,z3 = " + str(Z3_Derog)
	if not Zone_Derog:
	#Calcul Demande Zone 1 
		if (TEMP_R_Z1>PC_RE_Z1) and not Z1_Veille:
			z1C=0
			z1F=1
		elif (TEMP_R_Z1<PC_RH_Z1) and not Z1_Veille:
			z1F=0
			z1C=1
		else:
			z1C=0
			z1F=0
	#Zone 2 calcul demande
        	if (TEMP_R_Z2>PC_RE_Z2) and not Z2_Veille:
			z2C=0
                	z2F=1
        	elif (TEMP_R_Z2<PC_RH_Z2) and not Z2_Veille:
			z2F=0
                	z2C=1
        	else:
                	z2C=0
                	z2F=0
	#Calcul demande Zone3
        	if (TEMP_R_Z3>PC_RE_Z3) and not Z3_Veille:
			z3C=0
                	z3F=1
        	elif (TEMP_R_Z3<PC_RH_Z3) and not Z3_Veille:
			z3F=0
                	z3C=1
        	else:
                	z3C=0
                	z3F=0
	#Calcul demande zone4
        	if (TEMP_R_Z4>PC_RE_Z4) and not Z4_Veille:
			z4C=0
                	z4F=1
        	elif (TEMP_R_Z4<PC_RH_Z4) and not Z4_Veille:
			z4F=0
                	z4C=1
        	else:
                	z4C=0
                	z4F=0
	#calcul demande zone5
        	if (TEMP_R_Z5>PC_RE_Z5) and not Z5_Veille:
			z5C=0
                	z5F=1
        	elif (TEMP_R_Z5<PC_RH_Z5) and not Z5_Veille:
			z5F=0
                	z5C=1
        	else:
                	z5C=0
                	z5F=0
	else:
	        if (TEMP_R_Z1>PC_RE_Z1) and Z1_Derog  and not Z1_Veille :
                        z1C=0
                        z1F=1
                elif (TEMP_R_Z1<PC_RH_Z1) and Z1_Derog and not Z1_Veille:
                        z1F=0
                        z1C=1
                else:
                        z1C=0
                        z1F=0
        #Zone 2 calcul demande
                if (TEMP_R_Z2>PC_RE_Z2) and Z2_Derog and not Z2_Veille:
                        z2C=0
                        z2F=1
                elif (TEMP_R_Z2<PC_RH_Z2) and Z2_Derog and not Z2_Veille:
                        z2F=0
                        z2C=1
                else:
                        z2C=0
                        z2F=0
        #Calcul demande Zone3
                if (TEMP_R_Z3>PC_RE_Z3) and Z3_Derog and not Z3_Veille:
                        z3C=0
                        z3F=1
                elif (TEMP_R_Z3<PC_RH_Z3) and Z3_Derog and not Z3_Veille:
                        z3F=0
                        z3C=1
                else:
                        z3C=0
                        z3F=0
        #Calcul demande zone4
                if (TEMP_R_Z4>PC_RE_Z4) and Z4_Derog and not Z4_Veille:
                        z4C=0
                        z4F=1
                elif (TEMP_R_Z4<PC_RH_Z4) and Z4_Derog and not Z4_Veille:
                        z4F=0
                        z4C=1
                else:
                        z4C=0
                        z4F=0
        #calcul demande zone5
                if (TEMP_R_Z5>PC_RE_Z5) and Z5_Derog and not Z5_Veille:
                        z5C=0
                        z5F=1
                elif (TEMP_R_Z5<PC_RH_Z5) and Z5_Derog and not Z5_Veille:
                        z5F=0
                        z5C=1
                else:
                        z5C=0
                        z5F=0

	print "zone 1 F= " +str(z1F) + " en chaud = " + str(z1C)
        print "zone 2 F= " +str(z2F) + " en chaud = " + str(z2C)
        print "zone 3 F= " +str(z3F) + " en chaud = " + str(z3C)
	
        if co==1:
		print 'anticourcycle = '+str(anticourcycle)
                if ((z1F or z2F or z3F or z4F or z5F) and Assemblage==6 and ChangerTemp==0 and not anticourcycle):
                   	

			if Assemblage<>4:
                                EcrireRegistre(33,4)

                        ChangerTemp=1
			temps_dem=temps
			anticourcycle=True
			print 'TEmps dem='+str(temps_dem)
                elif  (not (z1F or z2F or z3F or z4F or z5F) and (z1C or z2C or z3C or z4C or z5C) and Assemblage==4 and ChangerTemp==0 and not anticourcycle):
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
                        print pc_Inoc_Chaud+decalage_temp_ete
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_ete)
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_ete)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_ete)
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
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_hiver)
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_hiver)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_hiver)
                        ChangerTemp=0
                        Blocage_fonctionnement=1
	if anticourcycle:
		if (temps>temps_dem+600):
			anticourcycle=False
	print "blocage = " + str(Blocage_fonctionnement)
	print "zone totale = " +str(zoneTot) + " zone init = " + str(zoneInit)
	print "bloquer = " + str(Bloquer)
        if Blocage_fonctionnement==1:

                if Bloquer<>2:
                        zoneInit=0
                        initZ1=0
                        initZ2=0
                        initZ3=0
                        initZ4=0
                        initZ5=0
			print "pourquoi je n ecris pas"
                        EcrireRegistre(32,2)
			#Bloquer=2
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
        print 'inoc chaud'
        print pc_Inoc_Chaud
        print First_Reg[71]
        print 'inoc froid'
        print pc_Inoc_Froid
        print First_Reg[39]
        print 'antigel'
        print pc_horsgel
        print First_Reg[40]


#EcrireRegistre(71,0)
#EcrireRegistre(72,0)
resistance_init=LireRegistre(285)
while 1:
#	time.sleep(0.5)
	First_Reg=LireRegistres(0,85)
#	time.sleep(0.5)
	Second_Reg=LireRegistres(140,84)
#	time.sleep(0.5)
	Third_Reg=LireRegistres(229,57)
        pc_hiver=First_Reg[81]
        pc_ete=First_Reg[82]
        dec_hiver=First_Reg[83]
        dec_ete=First_Reg[84]
        ouv_vanne=First_Reg[21]
        co=First_Reg[12]
        pc_horsgel= First_Reg[69]
        pc_Inoc_Chaud=First_Reg[71]*100
        pc_Inoc_Froid=First_Reg[72]*100
        if First_Reg[71]==720:
        	EcrireRegistre(72,29)
        	EcrireRegistre(69,1600)
		EcrireRegistre(71,16)
        print 'inoc chaud'
        print pc_Inoc_Chaud
        print First_Reg[38]
        print 'inoc froid'
        print pc_Inoc_Froid
        print First_Reg[39]
        print 'antigel'
        print pc_horsgel
        print First_Reg[40]
        tempZ1=Second_Reg[146-140]
	print tempZ1
        pcZ1=Second_Reg[147-140]
        tempZ2=Second_Reg[170-140]
        pcZ2=Second_Reg[171-140]
        tempZ3=Second_Reg[194-140]
        pcZ3=Second_Reg[195-140]
        tempZ4=Second_Reg[218-140]
        pcZ4=Second_Reg[219-140]
        tempZ5=Third_Reg[242-229]
        pcZ5=Third_Reg[243-229]
        Assemblage=First_Reg[33]
        Mode=First_Reg[70]
        Priorite=First_Reg[34]
#       Reg36=First_Reg[36]
        Bloquer=First_Reg[32]
        comZ1=Second_Reg[157-140]
        comZ2=Second_Reg[181-140]
        comZ3=Second_Reg[205-140]
        comZ4=Third_Reg[229-229]
        comZ5=Third_Reg[253-229]
        presZ1=Second_Reg[140-140]
	print comZ1
	print comZ2
        presZ2=Second_Reg[164-140]
	Bloquer= First_Reg[32]
        print Bloquer
	presZ3=Second_Reg[188-140]
        presZ4=Second_Reg[212-140]
        presZ5=Third_Reg[236-229]
        permResistance=First_Reg[50]
        permVanneChaud=First_Reg[53]
	if Second_Reg[148-140]<32768:
        	dec_z1=Second_Reg[148-140]
	else:
		dec_z1=Second_Reg[148-140]-65536
        if Second_Reg[172-140]<32768:
                dec_z2=Second_Reg[172-140]
        else:
                dec_z2=Second_Reg[172-140]-65536
        if Second_Reg[196-140]<32768:
                dec_z3=Second_Reg[196-140]
        else:
                dec_z3=Second_Reg[196-140]-65536
        if Second_Reg[222-140]<32768:
                dec_z4=Second_Reg[222-140]
        else:
                dec_z4=Second_Reg[222-140]-65536
        if Third_Reg[246-229]<32768:
                dec_z5=Third_Reg[246-229]
        else:
                dec_z5=Third_Reg[246-229]-65536
        mode_z1=Second_Reg[150-140]
        mode_z2=Second_Reg[174-140]
        mode_z3=Second_Reg[198-140]
        mode_z4=Second_Reg[222-140]
        mode_z5=Third_Reg[246-229]
        fen_z1 = Second_Reg[154-140]
        fen_z2=Second_Reg[178-140]
        fen_z3=Second_Reg[202-140]
        fen_z4=LireRegistre(226)
        fen_z5=Third_Reg[250-229]
#       print "z1 ="+str[mode_z1] print "z2 = "+ str[mode_z2] sonde_gtc=LireRegis
        print "decalage zone1 = " +str(dec_z1)
        autor_res=Third_Reg[285-229]
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


#       eg36=First_Reg[36] ts=time.time()
        vanne()
        consigne()
        if resistance:
                mode()
