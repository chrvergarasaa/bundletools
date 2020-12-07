#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os;
import numpy as np;
from shutil import copyfile, move;
import glob;
import utils.bundleTools as bt;
from time import time;

Ns = 79 #Número de sujetos. El código asume que los datos de los sujetos se encuentran en carpetas desde "001" hasta "Ns".

for i in range(1,Ns+1):     #Iteración sobre todos los sujetos   
    
    #---------- Sujeto a evaluar ----------# 
    if i < 10:
        sub = '00' + str(i);    #Los primeros 9 sujetos tienen prefijo "00" (001-009)...
        
    else:
        sub = '0' + str(i);     #...y el resto tiene prefijo "0" (por ejemplo, 010-079).
    
    print('\nProcesando sujeto ' + sub)
    
    #%% #---------- Setup (mallado y creación de carpetas) ----------#
    
    t1 = time();    #Cálculo de tiempo de ejecución
    
    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/lh.obj'; # Ruta en donde se encuentra el mallado del hemisferio izquierdo (en formato .obj)
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/rh.obj'; # Ruta en donde se encuentra el mallado del hemisferio derecho (en formato .obj)
    
    
    bundles_path = os.getcwd() + '/../isaias_clustering/Brain_fiber_clustering/data/79subjects/inter-clustered/' + sub + '/individual_aligned_clusters/T1/'; # Ruta en donde se encuentran los clusters del sujeto (en formato .bundles)

    classification_path = os.getcwd() + '/bundle_classification/'  + sub + '/'; # Ruta en donde se guardarán los bundles clasificados según su tipo de intersección.
    
    cluster_names = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(bundles_path + '*.bundles')]; # Lista con nombres de los clusters a evaluar
    
    Ldirect_path = os.getcwd() + '/membership/' + sub + '/L-L_direct/'; # Ruta de tupla de conectividad en el caso Ldirect.
    Linverse_path = os.getcwd() + '/membership/' + sub + '/L-L_inverse/'; # Ruta de tupla de conectividad en el caso Linverse.
    Rdirect_path = os.getcwd() + '/membership/' + sub + '/R-R_direct/'; # Ruta de tupla de conectividad en el caso Rdirect.
    Rinverse_path = os.getcwd() + '/membership/' + sub + '/R-R_inverse/'; # Ruta de tupla de conectividad en el caso Rinverse.
    
    ###---------- Creación de diccionario ----------###
    memb_dict = {}; # Diccionario que contiene la tupla de conectividad de cada cluster.
    
    for name in cluster_names:  # Iteración sobre cada cluster.
        Ldirect = Ldirect_path + name + '.membershipdata';
        Linverse = Linverse_path + name + '.membershipdata';
        Rdirect = Rdirect_path + name + '.membershipdata';
        Rinverse = Rinverse_path + name + '.membershipdata';
        
        with open(Ldirect, 'rb') as f1, open(Linverse, 'rb') as f2, open(Rdirect, 'rb') as f3, open(Rinverse, 'rb') as f4:  # Lectura de tupla de conectividad para los 4 casos posibles.
            Ldirect_flags = tuple(f1.read( 2 ));
            Linverse_flags = tuple(f2.read( 2 ));
            Rdirect_flags = tuple(f3.read( 2 ));
            Rinverse_flags = tuple(f4.read( 2 ));
        
        memb_dict[name] = {'Ldirect': Ldirect_flags, 'Linverse': Linverse_flags, 'Rdirect': Rdirect_flags, 'Rinverse': Rinverse_flags}; # Se añaden las tuplas al diccionario.
    
    ###---------- Creación de directorios de clasificación ----------###
    if not os.path.exists(classification_path + 'L-L/'):    # Clusters intra-hemisferio izquierdo.
        os.makedirs(classification_path + 'L-L/');
        
    if not os.path.exists(classification_path + 'R-R/'):    # Clusters intra-hemisferio derecho.
        os.makedirs(classification_path + 'R-R/');
        
    if not os.path.exists(classification_path + 'L-R/'):    # Cluster ínter-hemisferio de izquierda a derecha.
        os.makedirs(classification_path + 'L-R/');
        
    if not os.path.exists(classification_path + 'R-L/'):    # Cluster ínter-hemisferio de derecha a izquierda.
        os.makedirs(classification_path + 'R-L/');
        
    if not os.path.exists(classification_path + 'Discarded/'):  # Clusters que no intersectan en ambos extremos.
        os.makedirs(classification_path + 'Discarded/');
        
    if not os.path.exists(classification_path + 'Ambiguous/'):  # Clusters ambiguos o contradictorios.
        os.makedirs(classification_path + 'Ambiguous/');
    
    ambiguous = []; # Lista de clusters ambiguos.
    
    for cluster in memb_dict:   # Iteración sobre cada cluster.
        Ldirect_flags = memb_dict[cluster]['Ldirect'];  # Tupla de conectividad Ldirect.
        Linverse_flags = memb_dict[cluster]['Linverse'];  # Tupla de conectividad Linverse.
        Rdirect_flags = memb_dict[cluster]['Rdirect'];  # Tupla de conectividad Rdirect.
        Rinverse_flags = memb_dict[cluster]['Rinverse'];  # Tupla de conectividad Rinverse.
            
        count = sum(Ldirect_flags) + sum(Linverse_flags) + sum(Rdirect_flags) + sum(Rinverse_flags);    # Cantidad de flags iguales a 1 (se utiliza en el quinto caso).
        
        #--- Clasificación de clusters ---#
        
        if (Ldirect_flags == (1,1) or Linverse_flags == (1,1)) and (Rdirect_flags == (0,0) and Rinverse_flags == (0,0)):    # Clusters que sólo conectan con el hemisferio izquierdo, en cualquier sentido.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
    
        elif (Rdirect_flags == (1,1) or Rinverse_flags == (1,1)) and (Ldirect_flags == (0,0) and Linverse_flags == (0,0)):    # Clusters que sólo conectan con el hemisferio izquierdo, en cualquier sentido.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
    
        elif Ldirect_flags == (1,0) and Rinverse_flags == (1,0):    # Clusters que comienzan en el hemisferio izquierdo y terminan en el derecho.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'L-R/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'L-R/' + cluster + '.bundlesdata');
            
        elif Rdirect_flags == (1,0) and Linverse_flags == (1,0):    # Clusters que comienzan en el hemisferio derecho y terminan en el izquierdo.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'R-L/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'R-L/' + cluster + '.bundlesdata');
        
        elif count <= 1:    # Si el perfil tiene un flag igual a 1 o menos, es porque no conecta, o probablemente sólo conecte en un extremo.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'Discarded/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'Discarded/' + cluster + '.bundlesdata');    
    
        else:   # Si no cumple cualquiera de los casos anteriores, se considera ambiguo y se necesita más procesamiento.
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'Ambiguous/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'Ambiguous/' + cluster + '.bundlesdata');
            ambiguous.append(cluster);
                       
    for cluster in ambiguous:
        Ld = memb_dict[cluster]['Ldirect']; #Perfil de conectividad en caso Ldirect.
        Li = memb_dict[cluster]['Linverse']; #Perfil de conectividad en caso Linverse.
        Rd = memb_dict[cluster]['Rdirect']; #Perfil de conectividad en caso Rdirect.
        Ri = memb_dict[cluster]['Rinverse']; #Perfil de conectividad en caso Rinverse.
        
        # Lectura de datos de intersección en los cuatro casos posibles (triángulos intersectados, fibras que intersectan).
        Ld_int = os.getcwd() + '/intersection/' + sub + '/L-L_direct/' + cluster + '.intersectiondata';
        Li_int = os.getcwd() + '/intersection/' + sub + '/L-L_inverse/' + cluster + '.intersectiondata';
        Rd_int = os.getcwd() + '/intersection/' + sub + '/R-R_direct/' + cluster + '.intersectiondata';
        Ri_int = os.getcwd() + '/intersection/' + sub + '/R-R_inverse/' + cluster + '.intersectiondata';
        
        # Variables de conteo para cada caso (intra o inter, y L o R).
        intra_Ld = 0;
        intra_Li = 0;
        intra_Rd = 0;
        intra_Ri = 0;
        inter_LR = 0;
        inter_RL = 0;
        
        # Dependiendo del perfil de conectividad, obtenemos los datos de intersección de cada uno.
        if Ld == (1,1): # Caso: posiblemente intra hemisferio izquierdo.
            Ld_FnTri = bt.read_intersection(Ld_int)[1];
            intra_idx = np.where(Ld_FnTri != 1000000);  # No consideramos las fibras ínter-hemisferio en un cluster intra-hemisferio.   
            intra_Ld = len(Ld_FnTri[intra_idx]);    #Cantidad de fibras intra-hemisferio.
            
        if Li == (1,1): # Caso: posiblemente intra hemisferio izquierdo.
            Li_FnTri = bt.read_intersection(Li_int)[1];
            intra_idx = np.where(Li_FnTri != 1000000);  # No consideramos las fibras ínter-hemisferio en un cluster intra-hemisferio.   
            intra_Li = len(Li_FnTri[intra_idx]);    #Cantidad de fibras intra-hemisferio.
        
        if Rd == (1,1): # Caso: posiblemente intra hemisferio derecho.
            Rd_FnTri = bt.read_intersection(Rd_int)[1];
            intra_idx = np.where(Rd_FnTri != 1000000);  # No consideramos las fibras ínter-hemisferio en un cluster intra-hemisferio.   
            intra_Rd = len(Rd_FnTri[intra_idx]);    #Cantidad de fibras intra-hemisferio.
            
        if Ri == (1,1): # Caso: posiblemente intra hemisferio derecho.
            Ri_FnTri = bt.read_intersection(Ri_int)[1];
            intra_idx = np.where(Ri_FnTri != 1000000);  # No consideramos las fibras ínter-hemisferio en un cluster intra-hemisferio.   
            intra_Ri = len(Ri_FnTri[intra_idx]);    #Cantidad de fibras intra-hemisferio.
            
        if (Ld == (1,1) or Ld == (1,0)) and (Ri == (1,1) or Ri == (1,0)): # Caso: posiblemente ínter hemisferio de izquierda a derecha.
            Ld_FnTri = bt.read_intersection(Ld_int)[1]; #Índices de triángulos en el extremo final.
            
            fib_direct = bt.read_intersection(Ld_int)[-1];  # Índices de fibras que intersectaron en el sentido directo (provenientes del hemisferio izquierdo).
            fib_inverse = bt.read_intersection(Ri_int)[-1];  # Índices de fibras que intersectaron en el sentido inverso (que llegan al hemisferio derecho).
            
            fib_direct_inter = fib_direct[np.where(Ld_FnTri == 1000000)]    # Índices de fibras que sólo intersectaron en su extremo inicial en sentido directo (potencialmente ínter-hemisferio).
            
            inter_LR = sum(np.isin(fib_inverse, fib_direct_inter))  # Cantidad de fibras en sentido inverso que coinciden con las intersectadas en sentido directo (es decir, fibras potencialmente inter izquierda a derecha).
                                                            
        if (Rd == (1,1) or Rd == (1,0)) and (Li == (1,1) or Li == (1,0)): # Caso: posiblemente ínter hemisferio de derecha a izquierda.
            Rd_FnTri = bt.read_intersection(Rd_int)[1]; #Índices de triángulos en el extremo final.
            
            fib_direct = bt.read_intersection(Rd_int)[-1];  # Índices de fibras que intersectaron en el sentido directo (provenientes del hemisferio derecho).
            fib_inverse = bt.read_intersection(Li_int)[-1];  # Índices de fibras que intersectaron en el sentido inverso (que llegan al hemisferio izquierdo).
            
            fib_direct_inter = fib_direct[np.where(Rd_FnTri == 1000000)]    # Índices de fibras que sólo intersectaron en su extremo inicial en sentido directo (potencialmente ínter-hemisferio).
            
            inter_RL = sum(np.isin(fib_inverse, fib_direct_inter))  # Cantidad de fibras en sentido inverso que coinciden con las intersectadas en sentido directo (es decir, fibras potencialmente inter derecha a izquierda).
                        
        dom = max(intra_Ld,intra_Li,intra_Rd,intra_Ri,inter_LR,inter_RL);   # Máximo de cantidad de fibras en todos los casos considerados.
        dom_idx = np.argmax([intra_Ld,intra_Li,intra_Rd,intra_Ri,inter_LR,inter_RL]);   # Índice del máximo (argmax).
        
        #No intersection
        if dom == 0:    # Si no hay máximo, ninguno es mayor, y por tanto no es claro el tipo de intersección => se descarta.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'Discarded/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'Discarded/' + cluster + '.bundlesdata');
        
        #L_direct
        elif dom_idx == 0:  # Si argmax es el caso intra Ldirect, se clasifica como intra hemisferio izquierdo.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
            os.remove(Li_int)            
            
        #L_inverse    
        elif dom_idx == 1:  # Si argmax es el caso intra Linverse, se clasifica como intra hemisferio izquierdo.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
            os.remove(Ld_int)
            
        #R_direct
        elif dom_idx == 2:  # Si argmax es el caso intra Rdirect, se clasifica como intra hemisferio derecho.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
            os.remove(Ri_int)

        #R_inverse            
        elif dom_idx == 3:  # Si argmax es el caso intra Rinverse, se clasifica como intra hemisferio derecho.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
            os.remove(Rd_int)
            
        #L-R
        elif dom_idx == 4:  # Si argmax es el caso inter LR, se clasifica como inter hemisferio izquierdo a derecho.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-R/' + cluster + '.bundlesdata');
    
        #R-L
        elif dom_idx == 5:  # Si argmax es el caso inter RL, se clasifica como inter hemisferio derecho a izquierdo.
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-L/' + cluster + '.bundlesdata');
    

    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');