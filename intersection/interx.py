# -*- coding: utf-8 -*-

import os;
import subprocess as sp;
from time import time;
    
#========================== Cálculo de intersección ==========================================    

Ns = 79 #Número de sujetos. El código asume que los datos de los sujetos se encuentran en carpetas desde "001" hasta "Ns".

for i in range(1,Ns-1):     #Iteración sobre todos los sujetos   
    
    #---------- Sujeto a evaluar ----------# 
    if i < 10:
        sub = '00' + str(i);    #Los primeros 9 sujetos tienen prefijo "00" (001-009)...
        
    else:
        sub = '0' + str(i);     #...y el resto tiene prefijo "0" (por ejemplo, 010-079).
            
    print('\nProcesando sujeto ' + sub)
    
#%% #---------- Setup (mallado y creación de carpetas) ----------#
    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; # Ruta en donde se encuentra el mallado del hemisferio izquierdo (en formato .obj)
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; # Ruta en donde se encuentra el mallado del hemisferio derecho (en formato .obj)
    
    if not os.path.exists(os.getcwd() + '/membership/' + sub + '/'):
        os.makedirs(os.getcwd() + '/membership/' + sub + '/');          #Creación de carpeta para guardar las tuplas de conectividad (In,Fn) de cada cluster, en formato .membershipdata.
    
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/');        #Creación de carpeta para guardar la información de intersección de cada cluster, en formato .intersectiondata.
    
#%% 
    # ---------- Selección de fascículos a procesar ----------#
    bundles_path = os.getcwd() + '/../isaias_clustering/Brain_fiber_clustering/data/79subjects/inter-clustered_QB_202/' + sub + '/individual_aligned_clusters/T1/'; # Ruta en donde se encuentran los clusters del sujeto (en formato .bundles)
       
#%% 
    #---------- Intersección clusters con hemisferio izquierdo (Lhemi) ----------#
    t1 = time();    #Cálculo de tiempo de ejecución
    intersection_path = os.getcwd() + '/intersection/' + sub + '/L-L_direct/'; # intersection path
    membership_path = os.getcwd() + '/membership/' + sub + '/L-L_direct/'; # membership path
    
    #---------- Flags de escritura ----------#
    intersection_flag = '1';   #Escribir o no los datos de intersección (triángulos, fibras que intersectan, puntos de intersección)
    membership_flag = '1';     #Escribir o no datos de pertenencia (flags binarios: (1,1), (1,0), (0,0)).
    reverse_flag = '0';
    
    #---------- Llamada a código C++ ----------#
    print('\nLhemi direct')
    sp.call(['make']);  #Compilación del código C
    sp.call(['./interx', Lhemi_path, '', bundles_path, '', intersection_path, '', membership_path, '', intersection_flag, membership_flag, reverse_flag]); #Llamada al código C
    
    #Nota: Al llamar al código C en la línea anterior, los argumentos vacíos ('') se deben a que el código original se diseñó para trabajar con ambos hemisferios al mismo tiempo...
    #...sin embargo, esta implementación trabaja los hemisferios por separado, razón por la cual la mitad de los argumentos son vacíos.
    
    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');
    
#%% 
    #---------- Intersección clusters con hemisferio derecho (Rhemi) ----------#
    t1 = time();    #Cálculo de tiempo de ejecución
    intersection_path = os.getcwd() + '/intersection/' + sub + '/R-R_direct/'; # intersection path
    membership_path = os.getcwd() + '/membership/' + sub + '/R-R_direct/'; # membership path
    
    #---------- Flags de escritura ----------#
    intersection_flag = '1';   #Escribir o no los datos de intersección (triángulos, fibras que intersectan, puntos de intersección)
    membership_flag = '1';     #Escribir o no datos de pertenencia (flags binarios: (1,1), (1,0), (0,0)).
    reverse_flag = '0';
    
    #---------- Llamada a código C++ ----------#
    print('\nRhemi direct')
    sp.call(['./ejemplo', Lhemi_path, '', bundles_path, '', intersection_path, '', membership_path, '', intersection_flag, membership_flag, reverse_flag]);
    
    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');
    
#%% 
    #---------- Intersección clusters SENTIDO INVERSO con hemisferio izquierdo (Lhemi) ----------#    
    t1 = time();    #Cálculo de tiempo de ejecución
    intersection_path = os.getcwd() + '/intersection/' + sub + '/L-L_inverse/'; # intersection path
    membership_path = os.getcwd() + '/membership/' + sub + '/L-L_inverse/'; # membership path
    
    #---------- Flags de escritura ----------#
    intersection_flag = '1';   #Escribir o no archivo .intersectiondata con datos de intersección (triángulos intersectados, fibras que intersectan, puntos de intersección).
    membership_flag = '1';     #Escribir o no datos archivo .membershipdata con datos de pertenencia (flags binarios: (1,1), (1,0), (0,0)).
    reverse_flag = '1';        #Invertir o no las fibras que entran al cálculo de intersección (0: sentido original; 1: sentido inverso).
    
    #---------- Llamada a código C++ ----------#
    print('\nLhemi inverse')
    sp.call(['./ejemplo', Lhemi_path, '', bundles_path, '', intersection_path, '', membership_path, '', intersection_flag, membership_flag, reverse_flag]);

    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');

#%% 
    #---------- Intersección clusters SENTIDO INVERSO con hemisferio derecho (Rhemi) ----------#
    
    t1 = time();    #Cálculo de tiempo de ejecución
    intersection_path = os.getcwd() + '/intersection/' + sub + '/R-R_inverse/'; # intersection path
    membership_path = os.getcwd() + '/membership/' + sub + '/R-R_inverse/'; # membership path
    
    #---------- Flags de escritura ----------#
    intersection_flag = '1';   #Escribir o no los datos de intersección (triángulos, fibras que intersectan, puntos de intersección)
    membership_flag = '1';     #Escribir o no datos de pertenencia (flags binarios: (1,1), (1,0), (0,0)).
    reverse_flag = '1';
    
    #---------- Llamada a código C++ ----------#
    print('\nRhemi inverse')
    sp.call(['./ejemplo', Lhemi_path, '', bundles_path, '', intersection_path, '', membership_path, '', intersection_flag, membership_flag, reverse_flag]);
    
    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');