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
global Assemblage
global Mode
global Priorite
global Bloquer
global comZ1
global comZ2
global comZ3
global comZ4
global presZ1
global presZ2
global presZ3
global presZ4
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
zoneInit=0
time_init=0
time_for_vanne=0
forcage_vanne=0
m.write_register(284,0,0)
co_init=2
ChangerTemp=0
compteur=0
Compt=0

anticourcycle=False

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
        if sig:
                m.write_register(Reg,valeur,signed=True)
        else:
                m.write_register(Reg,valeur)
        raise Exception_valeur('Test')
def ReadRegister(registre):
        result=m.read_register(registre,0,signed=True)
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
                        if (ancienne<>valeur) and not  notWrite:
                                if sig:
                                        m.write_register(Reg,valeur,signed=True)
                                else:
                                        m.write_register(Reg,valeur)
                        else:
                                Write=False
                except IOError:
                        Compt+=1
                except TypeError:
                        Compt+=1
                except (ValueError):
                        Compt+=1
                else:
                        Compt=0
                        Write=False
                        return

def vanne():
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
        if presZ1 <>0:
                z1=1
        else:
                z1=0
        if presZ2 <>0:
                z2=1
        else:
                z2=0
        if presZ3 <>0:
                z3=1
        else:
                z3=0
        if presZ4 <>0:
                z4=1
        else:
                z4=0
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
                        EcrireRegistre(36,2000-dec_ete,0)
                        EcrireRegistre(37,2000+dec_ete,0)
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_ete)
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_ete)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_ete)
                        Blocage_fonctionnement=1
                        EcrireRegistre(33,4)
                else:
                        decalage_temp_hiver=max(min(1000,(2000-pc_hiver)),-1000)
                        if z1:
                                EcrireRegistre(148,decalage_temp_hiver/10,sig=True)
                        if z2:
                                EcrireRegistre(172,decalage_temp_hiver/10,sig=True)
                        if z3:
                                EcrireRegistre(196,decalage_temp_hiver/10,sig=True)
                        if z4:
                                EcrireRegistre(220,decalage_temp_hiver/10,sig=True)
                       
                        EcrireRegistre(36,2000-dec_hiver,0)
                        EcrireRegistre(37,2000+dec_hiver)
                        EcrireRegistre(39,pc_Inoc_Froid+decalage_temp_hiver)
                        EcrireRegistre(38,pc_Inoc_Chaud+decalage_temp_hiver)
                        EcrireRegistre(40,pc_horsgel+decalage_temp_hiver)
                        Blocage_fonctionnement=1
                        EcrireRegistre(33,7)
                co_init=co

while 1:

        First_Reg=LireRegistres(0,85)
        Second_Reg=LireRegistres(140,84)
        pc_hiver=First_Reg[81]
        pc_ete=First_Reg[82]
        dec_hiver=First_Reg[83]
        dec_ete=First_Reg[84]
        ouv_vanne=First_Reg[21]
        co=First_Reg[12]
        pc_horsgel= First_Reg[69]
        pc_Inoc_Chaud=First_Reg[71]*100
        pc_Inoc_Froid=First_Reg[72]*100
        if First_Reg[71]==720 or First_Reg[71]==0 :
                EcrireRegistre(72,29)
                EcrireRegistre(69,1600)
                EcrireRegistre(71,16)
        tempZ1=Second_Reg[146-140]
        print tempZ1
        pcZ1=Second_Reg[147-140]
        tempZ2=Second_Reg[170-140]
        pcZ2=Second_Reg[171-140]
        tempZ3=Second_Reg[194-140]
        pcZ3=Second_Reg[195-140]
        tempZ4=Second_Reg[218-140]
        pcZ4=Second_Reg[219-140]
        Assemblage=First_Reg[33]
        Mode=First_Reg[70]
        Priorite=First_Reg[34]
        Bloquer=First_Reg[32]
        comZ1=Second_Reg[157-140]
        comZ2=Second_Reg[181-140]
        comZ3=Second_Reg[205-140]
        comZ4=LireRegistre(229)
        presZ1=Second_Reg[140-140]
        print comZ1
        print comZ2
        presZ2=Second_Reg[164-140]
        Bloquer= First_Reg[32]
        print Bloquer
        presZ3=Second_Reg[188-140]
        presZ4=Second_Reg[212-140]
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
        if Second_Reg[220-140]<32768:
                dec_z4=Second_Reg[220-140]
        else:
                dec_z4=Second_Reg[220-140]-65536
        mode_z1=Second_Reg[150-140]
        mode_z2=Second_Reg[174-140]
        mode_z3=Second_Reg[198-140]
        mode_z4=Second_Reg[222-140]
        fen_z1 = Second_Reg[154-140]
        fen_z2=Second_Reg[178-140]
        fen_z3=Second_Reg[202-140]
        fen_z4=LireRegistre(226)
        if LireRegistre(77)==0:
                EcrireRegistre(285,2)
                EcrireRegistre(77,1)
        time.sleep(0.5)
        ts=time.time()
        vanne()
        consigne()
