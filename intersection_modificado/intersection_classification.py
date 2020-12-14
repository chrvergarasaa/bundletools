#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os;
import numpy as np;
from shutil import move;
import glob;
import utils.bundleTools as bt;
from time import time;

#Este código es para realizar un post-procesamiento a las intersecciones cluster-corteza obtenidas con el algoritmo de intersección.
#Se basa en los perfiles de conectividad, y la clasificación de clusters realizada previamente con bundle_classification.
#Sin embargo, vale mencionar que al igual que bundle_classification, este código es altamente heurístico, y por lo tanto su lógica es...
#...en el mejor de los casos, funcional, y en el peor de los casos, confusa y deficiente.

#Sumado a lo anterior, la naturaleza volátil y variable de las intersecciones evaluadas en ambos sentido (principalmente debido al error de proyección...
#...del algoritmo de intersección) hacen que este algoritmo sea aún más propenso a errores.


Ns = 79 #Número de sujetos. El código asume que los datos de los sujetos se encuentran en carpetas desde "001" hasta "Ns".

for i in range(1,Ns+1):     #Iteración sobre todos los sujetos   

    #---------- Sujeto a evaluar ----------# 
    if i < 10:    
        sub = '00' + str(i);    #Los primeros 9 sujetos tienen prefijo "00" (001-009)...
        
    else:
        sub = '0' + str(i);     #...y el resto tiene prefijo "0" (por ejemplo, 010-079).
    
    print('\nProcesando sujeto ' + sub);
    
    t1 = time();
    
    #---------- Perfiles de conectividad ----------#    
    Ldirect_path = os.getcwd() + '/intersection/' + sub + '/L-L_direct/';
    Linverse_path = os.getcwd() + '/intersection/' + sub + '/L-L_inverse/';
    Rdirect_path = os.getcwd() + '/intersection/' + sub + '/R-R_direct/';
    Rinverse_path = os.getcwd() + '/intersection/' + sub + '/R-R_inverse/';
    
    #---------- Creación de directorios para intersecciones finales ----------#
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/Final/L-L/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/Final/L-L/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/Final/L-R/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/Final/L-R/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/Final/R-L/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/Final/R-L/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/Final/R-R/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/Final/R-R/');    
        
    if not os.path.exists(os.getcwd() + '/intersection/' + sub + '/Final/Inter/'):
        os.makedirs(os.getcwd() + '/intersection/' + sub + '/Final/Inter/');
    
    #---------- Clasificaciones iniciales de clusters (obtenidas con bundle_classification) ----------#
    LL_path = os.getcwd() + '/bundle_classification/' + sub + '/L-L/';
    LR_path = os.getcwd() + '/bundle_classification/' + sub + '/L-R/';
    RL_path = os.getcwd() + '/bundle_classification/' + sub + '/R-L/';
    RR_path = os.getcwd() + '/bundle_classification/' + sub + '/R-R/';
    
    #---------- Lectura de bundles en cada categoría ----------#
    LL_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(LL_path + '*.bundles')]; #Todos los clusters que son intra L hemi.
    LR_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(LR_path + '*.bundles')]; #Todos los clusters que son inter L to R hemi.
    RL_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(RL_path + '*.bundles')]; #Todos los clusters que son inter R to L hemi.
    RR_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(RR_path + '*.bundles')]; #Todos los clusters que son intra R hemi.
    
    #---------- Clusters con resultados extraños (contradictorios o ambiguos) ----------#
    LL_weird = [];
    LR_weird = [];
    RL_weird = [];
    RR_weird = [];
    
    #---------- Clasificación de los clusters intra L hemi ----------#
    #La idea aquí es filtrar las fibras que sólo intersectan en su extremo inicial, y mantener las fibras intra-hemisferio.
    for cluster in LL_list:
        Ld_infile = Ldirect_path + cluster + '.intersectiondata';   #Intersección en sentido directo.
        Li_infile = Linverse_path + cluster + '.intersectiondata';  #Intersección en sentido inverso.
        
        # En primera instancia trabajamos con intersección en sentido directo
        if os.path.exists(Ld_infile): 
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Ld_infile);
            intra_idx = np.where(FnTri != 1000000);   #Índices de fibras intra-hemisferio (las fibras que sólo conectan en un extremo tienen asignado FnTri = 1000000).
            InTri = InTri[intra_idx];                 #Triángulos del extremo inicial correspondientes sólo a fibras intra-hemisferio.
            n_tri = np.uint32(len(InTri));            #Cantidad de triángulos intra.
            
            #En caso de que no hayan triángulos intra, intentamos lo mismo con el sentido inverso.
            if n_tri == 0:
                InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Li_infile);
                intra_idx = np.where(FnTri != 1000000);
                InTri = InTri[intra_idx];
                n_tri = np.uint32(len(InTri));
                
            #En caso de que sí hayan triángulos intra...
            else:
                FnTri = FnTri[intra_idx];           #Triángulos del extremo inicial correspondientes sólo a fibras intra-hemisferio.
                InPoints = InPoints[intra_idx];     #Puntos del extremo inicial correspondientes sólo a fibras intra-hemisferio.
                FnPoints = FnPoints[intra_idx];     #Puntos del extremo final correspondientes sólo a fibras intra-hemisferio.
                fib_index = fib_index[intra_idx];   #Índices de las fibras intra-hemisferio (relativas al total de fibras del cluster).
                
                f = open(Ldirect_path + '../Final/L-L/' + cluster + '.intersectiondata', 'wb+');    #Archivo de intersección final a escribir.
                
                #El archivo .intersectiondata guarda lo siguiente:
                f.write(n_tri);     #Número de triángulos intersectados.
                
                f.write(InTri);     #Triángulos del extremo inicial.
                f.write(FnTri);     #Triángulos del extremo final.
                
                f.write(InPoints);  #Puntos del extremo inicial.
                f.write(FnPoints);  #Puntos del extremo final.
                
                f.write(fib_index); #Índices de fibras intra-hemisferio.
                
                f.close();    
            
        #Si no hay intersección en sentido directo, utilizamos la encontrada en sentido inverso.
        elif os.path.exists(Li_infile):
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Li_infile);
            intra_idx = np.where(FnTri != 1000000);
            InTri = InTri[intra_idx];
            n_tri = np.uint32(len(InTri));
            
            #Si no hay triángulos, entonces descartamos el cluster (aunque esta situación no debiese ocurrir).
            if n_tri == 0:
                move(os.getcwd() + '/bundle_classification/' + sub + '/L-L/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundles');
                move(os.getcwd() + '/bundle_classification/' + sub + '/L-L/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundlesdata');
                continue;     
                
            else:
                FnTri = FnTri[intra_idx];
                InPoints = InPoints[intra_idx];
                FnPoints = FnPoints[intra_idx];
                fib_index = fib_index[intra_idx];
                
                f = open(Ldirect_path + '../Final/L-L/' + cluster + '.intersectiondata', 'wb+');
                
                f.write(n_tri);
                
                f.write(FnTri);
                f.write(InTri);
                
                f.write(FnPoints);
                f.write(InPoints);
                
                f.write(fib_index);
                
                f.close();    

    #---------- Clasificación de los clusters inter L to R hemi ----------#
    #La idea aquí es filtrar las fibras que intersectan en ambos extremos (intra), y mantener las fibras inter-hemisferio.
    for cluster in LR_list:
        
        #Tomamos el sentido directo, es decir, de L a R.
        infile = Ldirect_path + cluster + '.intersectiondata';    
        
        #El sentido directo debiese existir, por lo que si no existe lo agregamos a la lista de clusters extraños para inspección.
        if not os.path.exists(infile):
            LR_weird.append(cluster);
            continue;
        
        #Lectura de intersección en sentido directo.
        InTri_direct, FnTri_direct, InPoints_direct, FnPoints_direct, fib_index_direct = bt.read_intersection(infile);
    
        #Tomamos el sentido inverso, es decir, de R a L.
        infile = Rinverse_path + cluster + '.intersectiondata';
        
        #Si no existe lo agregamos a la lista de extraños.
        if not os.path.exists(infile):
            LR_weird.append(cluster);
            continue;
            
        #Lectura de intersección en sentido inverso.
        InTri_reverse, FnTri_reverse, InPoints_reverse, FnPoints_reverse, fib_index_reverse = bt.read_intersection(infile);
    
        #Obtenemos los índices de las fibras que están tanto en sentido directo como en sentido inverso (que aparecen en ambos archivos .intersectiondata).
        fib_index_direct = fib_index_direct[np.in1d(fib_index_direct, fib_index_reverse)];
        fib_index_reverse = fib_index_reverse[np.in1d(fib_index_reverse, fib_index_direct)];
        
        #Obtenemos los triángulos del extremo inicial en ambos sentidos (donde los triángulos del extremo inicial en sentido inverso, serán los triángulos finales al considerar las fibras como ínter-hemisferio).
        InTri_direct = InTri_direct[fib_index_direct.argsort()];
        InTri_reverse = InTri_reverse[fib_index_reverse.argsort()];

        #Reordenamos los índices.
        fib_index_direct = np.sort(fib_index_direct);

        #Cantidad de triángulos obtenidos.
        n_tri = np.uint32(len(InTri_direct));
    
        #Si no quedan triángulos, descartamos el cluster.
        if n_tri == 0:
            move(os.getcwd() + '/bundle_classification/' + sub + '/L-R/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundles');
            move(os.getcwd() + '/bundle_classification/' + sub + '/L-R/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundlesdata');
            continue;
    
        #Guardado de archivo .intersectiondata final.
        f = open(Ldirect_path + '../Final/Inter/' + cluster + '.intersectiondata', 'wb+');
    
        f.write(n_tri);

        f.write(InTri_direct);
        f.write(InTri_reverse);
        
        f.write(InPoints_direct);
        f.write(InPoints_reverse);
    
        fib_index_direct = np.sort(fib_index_direct);
        f.write(fib_index_direct);
    
        f.close();
    
    #---------- Clasificación de los clusters inter R to L hemi ----------#    
    #Se realiza el mismo procedimiento que para L to R, pero a la inversa.
    for cluster in RL_list:
        infile = Rdirect_path + cluster + '.intersectiondata';    
        
        if not os.path.exists(infile):
            RL_weird.append(cluster);
            continue;
        
        InTri_direct, FnTri_direct, InPoints_direct, FnPoints_direct, fib_index_direct = bt.read_intersection(infile);
    
        infile = Linverse_path + cluster + '.intersectiondata';
        
        if not os.path.exists(infile):
            RL_weird.append(cluster);
            continue;
    
        InTri_reverse, FnTri_reverse, InPoints_reverse, FnPoints_reverse, fib_index_reverse = bt.read_intersection(infile);
            
        fib_index_direct = fib_index_direct[np.in1d(fib_index_direct, fib_index_reverse)];
        fib_index_reverse = fib_index_reverse[np.in1d(fib_index_reverse, fib_index_direct)];
        
        InTri_direct = InTri_direct[fib_index_direct.argsort()];
        InTri_reverse = InTri_reverse[fib_index_reverse.argsort()];

        fib_index_direct = np.sort(fib_index_direct);

        n_tri = np.uint32(len(InTri_direct));
    
        if n_tri == 0:
            move(os.getcwd() + '/bundle_classification/' + sub + '/R-L/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundles');
            move(os.getcwd() + '/bundle_classification/' + sub + '/R-L/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundlesdata');
            continue;
    
        f = open(Ldirect_path + '../Final/Inter/' + cluster + '.intersectiondata', 'wb+');
    
        f.write(n_tri);

        f.write(InTri_reverse);
        f.write(InTri_direct);    
        
        f.write(InPoints_reverse);
        f.write(InPoints_direct);
    
        fib_index_direct = np.sort(fib_index_direct);
        f.write(fib_index_direct);
    
        f.close();
    
    #---------- Clasificación de los clusters intra R hemi ----------#
    #Se realiza el mismo procedimiento que para intra L hemi.
    for cluster in RR_list:
        Rd_infile = Rdirect_path + cluster + '.intersectiondata';
        Ri_infile = Rinverse_path + cluster + '.intersectiondata';
        
        if os.path.exists(Rd_infile): 
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Rd_infile);
            intra_idx = np.where(FnTri != 1000000);
            InTri = InTri[intra_idx];
            n_tri = np.uint32(len(InTri));
            
            if n_tri == 0:
                print(cluster);
                InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Ri_infile);
                intra_idx = np.where(FnTri != 1000000);
                InTri = InTri[intra_idx];
                n_tri = np.uint32(len(InTri));
                
            else:
                FnTri = FnTri[intra_idx];
                InPoints = InPoints[intra_idx];
                FnPoints = FnPoints[intra_idx];
                fib_index = fib_index[intra_idx];
                
                f = open(Ldirect_path + '../Final/R-R/' + cluster + '.intersectiondata', 'wb+');        
                
                f.write(n_tri);
        
                f.write(InTri);
                f.write(FnTri);
        
                f.write(InPoints);
                f.write(FnPoints);
        
                f.write(fib_index);
        
                f.close();

        elif os.path.exists(Ri_infile):
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Ri_infile);
            intra_idx = np.where(FnTri != 1000000);
            InTri = InTri[intra_idx];
            n_tri = np.uint32(len(InTri));
            
            if n_tri == 0:
                move(os.getcwd() + '/bundle_classification/' + sub + '/R-R/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundles');
                move(os.getcwd() + '/bundle_classification/' + sub + '/R-R/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + sub + '/Discarded/' + cluster + '.bundlesdata');
                continue;       
                
            else:
                FnTri = FnTri[intra_idx];
                InPoints = InPoints[intra_idx];
                FnPoints = FnPoints[intra_idx];
                fib_index = fib_index[intra_idx];
        
                f = open(Ldirect_path + '../Final/R-R/' + cluster + '.intersectiondata', 'wb+');
            
                f.write(n_tri);
            
                f.write(FnTri);
                f.write(InTri);
            
                f.write(FnPoints);
                f.write(InPoints);
                
                f.write(fib_index);
            
                f.close();
                
    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');
    
