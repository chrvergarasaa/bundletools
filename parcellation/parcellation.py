#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 20:09:15 2020

@author: fondecyt-1190701
"""
import numpy as np
import os
import operator
import subprocess as sproc
import networkx as nx
from collections import defaultdict
from time import time
from itertools import combinations
from random import random
from copy import deepcopy

import bundleTools as bt
import bundleTools3 as bt3
import visualizationTools as vt

#%%

#Obtiene los triángulos por cada subparcela
def triangles_per_subparcel(hemi_dict, sp_dict):
    #Para cada triángulo...
    for tri in hemi_dict.keys():
        for k, v in hemi_dict[tri].items():
            
            #Si es el contador general del triángulo, no hacer nada.
            if k == 'n':
                continue
            
            #Si es el contador de una subparcela, agregarlo al diccionario de subparcelas
            else:
                sp_dict[k][tri] = v

#Elimina subparcelas pequeñas (tamaño medido en cantidad de triángulos)
def filter_small_parcels(hemi_dict, sp_dict, thr):
    #Para cada subparcela...
    for sp in list(sp_dict.keys()):
        #Si tiene menos triángulos que el umbral, eliminar la subparcela del diccionario de subparcelas...
        if len(sp_dict[sp]) < thr:
            small = sp_dict.pop(sp)
            
            #...y también del diccionario de triángulos. Además, reducir el contador "n".
            for tri in list(small.keys()):
                hemi_dict[tri]['n'] -= small[tri]
                del hemi_dict[tri][sp]

#Cálculo del centro de densidad de cada parcela
def calculate_density_center(hemi_dict, dc_dict, thr):
    #Para cada triángulo...
    for tri in hemi_dict.keys():
        for k, v in hemi_dict[tri].items():
            
            #Si es el contador general del triángulo, no hacer nada.
            if k == 'n':
                continue
            
            #De lo contrario, calcular la probabilidad de la subparcela como "contador_subparcela/contador_general".
            else:
                p = v/hemi_dict[tri]['n']
                 
                #Si la probabilidad es mayor que el umbral, guardar en diccionario de centros de densidad.
                if p >= thr:
                    dc_dict[k][tri] = p

#Traslape entre sub-parcelas
def subparcel_overlap(dc, dc_dict, thr):
    #Se crea un grafo no dirigido
    dc_graph = nx.Graph()
    
    #Y una matriz cuadrada que almacena el traslape (idc) para cada par de centros de densidad
    n_dc = len(dc)
    overlaps = np.zeros((n_dc,n_dc))
    
    #Todos contra todos...
    for sp1 in dc_dict.keys():
        for sp2 in dc_dict.keys():
            if sp1 != sp2:
                sp1_tri = set(dc_dict[sp1].keys())
                sp2_tri = set(dc_dict[sp2].keys())
                
                #Calcular la intersección entre ambos centros de densidad
                inter = sp1_tri.intersection(sp2_tri)
                sp_min = np.min((len(sp1_tri),len(sp2_tri)))
                
                #Calcular el idc = interseccion(dc)/min(dc)
                idc = len(inter)/sp_min
                
                #Si es mayor al umbral definido, agregar al grafo. Además, agregar su idc a la matriz.
                if idc >= idc_thr:
                    dc_graph.add_edge(sp1,sp2)
                    overlaps[dc.index(sp1),dc.index(sp2)] = idc
                    overlaps[dc.index(sp2),dc.index(sp1)] = idc
        
    return dc_graph, overlaps

#Fusiona subparcelas con traslape significativo
def fuse_subparcels(dc, dc_graph, overlaps, hemi_dict, sp_dict):
    #Obtiene una lista con los cliques maximales del grafo
    cliques = sorted(nx.find_cliques(dc_graph), key = len, reverse = True)
    
    #Ordena los cliques maximales... primero por largo, y luego por porcentaje de intersección promedio
    cliques_avg_idc = []
    
    #Para cada clique...
    for clique in cliques:
        total_idc = []

        #Se obtienen todas las combinaciones posibles del clique, y para cada par...
        for pair in combinations(clique, 2):
            #...se obtienen el traslape
            total_idc.append(overlaps[dc.index(pair[0]),dc.index(pair[1])])
        
        #Y luego se obtiene el promedio de los traslapes para ese clique.
        cliques_avg_idc.append(np.mean(total_idc))
    
    #Se ordenan los cliques maximales según el traslape promedio
    cliques_temp = sorted(zip(cliques, cliques_avg_idc), key = lambda x: (len(x[0]), x[1]), reverse = True)
    cliques_sorted, avg_idc_sorted = map(list, zip(*cliques_temp))

    #Se fusionan los cliques en orden descendente, descartando aquellos que ya fueron utilizados
    used = set()
    
    for clique in cliques_sorted:
        for sp in clique:
            if sp in used:
                continue
            else:
                ref = sp
                used.add(sp)
                break
            
        for sp in clique:
            if sp == ref or sp in used:
                continue
            
            else:
                for tri in list(sp_dict[sp].keys()):
                    hemi_dict[tri][ref] += sp_dict[sp][tri]
                    del hemi_dict[tri][sp]            
                used.add(sp)
                
#Obtiene parcelación dura (determinista, asignando a cada triángulo la subparcela con mayor probabilidad)
def hard_parcellation(hemi_dict, sp_hard):
    #Para cada triángulo...
    for tri in list(hemi_dict.keys()):
        #Eliminar el contador general. Además, si el triángulo queda sin parcelas, eliminar su entrada.
        del hemi_dict[tri]['n']
        if len(hemi_dict[tri]) == 0:
            del hemi_dict[tri]
    
    #Para cada triángulo, obtener la subparcela con mayor probabilidad,
    for tri in list(hemi_dict.keys()):        
        m = max(hemi_dict[tri].items(), key=operator.itemgetter(1))[0]    
        hemi_dict[tri] = m
        
    #Agregar la parcela más probable al diccionario de parcelación dura, junto con sus triángulos.
    for tri, sp in hemi_dict.items():
        sp_hard[sp].append(tri)
        
#Componentes Conectadas Principales
def PCC(Tri, polygons): #Autor: Felipe Silva
    if len(Tri) == 0: return Tri;
    edgesPolys = [];

    for ind in Tri:
        edgesPolys.append([polygons[ind,0], polygons[ind,1]]);
        edgesPolys.append([polygons[ind,0], polygons[ind,2]]);
        edgesPolys.append([polygons[ind,1], polygons[ind,2]]);
    
    edgesPolys = np.unique(edgesPolys, axis=0);
    
    G = nx.Graph();
    G.add_edges_from(edgesPolys);
    
    cc = list(nx.connected_components(G));
    len_cc = [len(comp) for comp in cc];
    regions_cc = list(cc[np.argmax(len_cc)]);
    
    ind = [np.where(polygons[Tri]==region_cc)[0] for region_cc in regions_cc];
    ind = np.unique(np.concatenate(ind));
    return (cc, len_cc, Tri[ind]);
    
#%%
import pickle

#Existen ciertos triángulos que, por definición, no pueden representar parcelas. Estos corresponden a regiones posterior-inferior de la línea media...
#...donde ambos hemisferios se unen, ya que en estricto rigor no corresponden a corteza, si no que a materia blanca/gris interna.

#La parcelación obtenida por Lefranc indica cuales triángulos están "restringidos", los cuales están guardados en el archivo .pkl:
#Lrestricted.pkl para el hemisferio izquierdo.
#Rrestricted.pkl para el hemisferio derecho.

with open('Lnope.pkl', 'rb') as f:
    Lrestricted = set(pickle.load(f))

with open('Rnope.pkl', 'rb') as f:
    Rrestricted = set(pickle.load(f))

#%%
#Proyecta la parcelación obtenida sobre un mallado cortical ARCHI
def visualize_parcellation(L_sp, R_sp, sub, seed = False):
    
    #Semilla para colores aleatorios
    if seed != False:
        np.random.seed(seed)
    
    #Parcelas finales a graficar
    final_parcels = set()

    for k in L_sp.keys():
        final_parcels.add(k)
        
    for k in R_sp.keys():
        final_parcels.add(k)

    fp = list(final_parcels)    

    #Paleta de colores según cantidad de parcelas
    paleta = [(np.random.random(), np.random.random(), np.random.random()) for i in range(len(fp))]

    #Directorios de los mallados corticales
    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; # left hemisphere path
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; # right hemisphere path

    #Lectura de mallados
    Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
    Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)
    
    Lhemi = vt.Polygon(Lvertex, Lpolygons);
    Rhemi = vt.Polygon(Rvertex, Rpolygons);
    
    Lhemi.setOpacity(1);
    Rhemi.setOpacity(1);
    
    #Creación del render a visualizar
    render = vt.Render();
    
    #Se renderizan los mallados
    render.AddActor(Lhemi);
    render.AddActor(Rhemi);
    
    #Para cada parcela del hemisferio izquierdo...
    for k, v in L_sp.items():
        #Se selecciona un color de la paleta
        color = paleta[fp.index(k)]
        
        if len(v) == 0:
            continue
    
        #De todos los triángulos con parcelas, se eliminan aquellos que pertenecen al conjunto de triángulos restringidos.
        v_restricted = list(set(v).difference(Lrestricted))
    
        #Se renderizan los triángulos y polígonos.
        sp_tri = vt.Polygon(Lvertex, Lpolygons[v_restricted]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);

    #Ídem para el derecho
    for k, v in R_sp.items():
        color = paleta[fp.index(k)]
    
        if len(v) == 0:
            continue
    
        v_restricted = list(set(v).difference(Rrestricted))
    
        sp_tri = vt.Polygon(Rvertex, Rpolygons[v_restricted]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);
    
    render.Start();
    del render
    
#%%---------- Setup (mallado y creación de carpetas) ----------#

#Sujeto base. Puede ser cualquiera, ya que todos los mallados tienen triángulos correspondientes.
sub = '001';

#Lectura de polígonos del mallado izquierdo y derecho.
Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; 
Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; 

Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)

#Cálculo de vecindad para cada triángulo del mallado (triángulos que comparten una arista o un vértice).
Lneighbors = bt.mesh_neighbors(Lpolygons)
Rneighbors = bt.mesh_neighbors(Rpolygons)

#%%----------Creación de diccionarios ----------#

# Key: Value => Subparcela: [triángulos en los que aparece la subparcela]
L_sp_dict = defaultdict(lambda: defaultdict(float))
R_sp_dict = defaultdict(lambda: defaultdict(float))

# Key: Value => Subparcela: [triángulos correspondientes al centro de densidad de la subparcela]
L_dc_dict = defaultdict(lambda: defaultdict(float))
R_dc_dict = defaultdict(lambda: defaultdict(float))

# Key: Value => Triángulo: [subparcelas que llegan a ese triángulo, y cuántas veces lo hace cada una]
Lhemi_dict = defaultdict(lambda: defaultdict(int))
Rhemi_dict = defaultdict(lambda: defaultdict(int))

#%% Subparcelas preliminares por cada triángulo (i.e. cuál subparcela aparece en cada triángulo, y cuántas veces)
for i in range(1,80):
    
    t0 = time()
    
    #Nombre del sujeto
    if i < 10:
        sub = '00' + str(i)
        
    else:
        sub = '0' + str(i)
    
    print(sub)
    
    #Tipo de intersección
    int_type = ['L-L','R-R','Inter']
    
    #Se itera sobre todas las intersecciones
    for tipo in int_type:
        int_path = '../intersection_int32/intersection/' + sub + '/Final/' + tipo + '/'
        int_list = os.listdir(int_path)
        
        #Conteo de subparcelas preliminares por triángulo.
            #Por definición, cada clúster define dos subparcelas:
                #En su extremo inicial, la subparcela clúster_A
                #En su extremo final, la subparcela clúster_B
                
        for file in int_list:
            cluster_name = file.split('.')[0].split('_')[1]
            
            #Dependiendo del tipo de intersección (intra o inter), se define el nombre la subparcela:
                #Para Intra-Left: Tanto el extremo A como el extremo B están en el diccionario de subparcelas izquierdas.
                #Para Intra-Right: Tanto el extremo A como el extremo B están en el diccionario de subparcelas derechas.
                #Para Ìnter: El extremo A està en el lado izquierdo, y el B en el derecho.
                
            if tipo == 'L-L':
                if cluster_name + 'A' not in L_sp_dict:
                    L_sp_dict[cluster_name + 'A'] = {}
            
                if cluster_name + 'B' not in L_sp_dict:
                    L_sp_dict[cluster_name + 'B'] = {}
                    
            elif tipo == 'Inter':
                if cluster_name + 'A' not in L_sp_dict:
                    L_sp_dict[cluster_name + 'A'] = {}
            
                if cluster_name + 'B' not in R_sp_dict:
                    R_sp_dict[cluster_name + 'B'] = {}
                    
            elif tipo == 'R-R':
                if cluster_name + 'A' not in R_sp_dict:
                    R_sp_dict[cluster_name + 'A'] = {}
            
                if cluster_name + 'B' not in R_sp_dict:
                    R_sp_dict[cluster_name + 'B'] = {}
            
            #Lectura de intersección y obtención de triángulos iniciales y finales
            ix = bt.read_intersection(int_path + file)
            in_tri = ix[0]
            fn_tri = ix[1]
            
            #Por cada triángulo, aumentar contador para la subparcela correspondiente.
            #Además, aumentar el contador general "n" del triángulo.
            for tri in in_tri:            
                if tipo == 'L-L' or tipo == 'Inter':
                    Lhemi_dict[tri]['n'] += 1 
                    Lhemi_dict[tri][cluster_name + 'A'] += 1
                    
                    nbors = Lneighbors[tri]
                    
                    for nbor in nbors:
                        if nbor in in_tri:
                            Lhemi_dict[tri]['n'] += 1 
                            Lhemi_dict[tri][cluster_name + 'A'] += 1
                    
                elif tipo == 'R-R':
                    Rhemi_dict[tri]['n'] += 1 
                    Rhemi_dict[tri][cluster_name + 'A'] += 1
                    
                    nbors = Rneighbors[tri]
                    
                    for nbor in nbors:
                        if nbor in in_tri:
                            Rhemi_dict[tri]['n'] += 1
                            Rhemi_dict[tri][cluster_name + 'A'] += 1
                
            for tri in fn_tri:
                if tipo == 'L-L':
                    Lhemi_dict[tri]['n'] += 1 
                    Lhemi_dict[tri][cluster_name + 'B'] += 1
                    
                    nbors = Lneighbors[tri]
                    
                    for nbor in nbors:
                        if nbor in in_tri:
                            Lhemi_dict[tri]['n'] += 1 
                            Lhemi_dict[tri][cluster_name + 'B'] += 1
                    
                elif tipo == 'Inter' or tipo == 'R-R':
                    Rhemi_dict[tri]['n'] += 1 
                    Rhemi_dict[tri][cluster_name + 'B'] += 1
                    
                    nbors = Rneighbors[tri]
                    
                    for nbor in nbors:
                        if nbor in in_tri:
                            Rhemi_dict[tri]['n'] += 1
                            Rhemi_dict[tri][cluster_name + 'B'] += 1
                            

    print(str(time() - t0) + '[s]')    
                
#%% Conteo de triángulos para cada subparcela (i.e. en cuáles triángulos aparece X subparcela, y cuántas veces llega ahí)
            
triangles_per_subparcel(Lhemi_dict, L_sp_dict)            
triangles_per_subparcel(Rhemi_dict, R_sp_dict)
   
#%% Filtrado de subparcelas pequeñas (por cantidad de triángulos insuficientes). Incluye actualización de conteo en primer diccionario.

size_thr = len(Lpolygons)/1000.0
                
filter_small_parcels(Lhemi_dict, L_sp_dict, size_thr)
filter_small_parcels(Rhemi_dict, R_sp_dict, size_thr)

#%% Cálculo de probabilidades y centros de densidad de cada subparcela.

dc_thr = 0.2

calculate_density_center(Lhemi_dict, L_dc_dict, dc_thr)
calculate_density_center(Rhemi_dict, R_dc_dict, dc_thr)

#%% Modelación del traslape entre subparcelas.

idc_thr = 0.1

L_dc = list(L_dc_dict.keys())
R_dc = list(R_dc_dict.keys())

L_dc_graph, L_overlaps = subparcel_overlap(L_dc, L_dc_dict, idc_thr)
R_dc_graph, R_overlaps = subparcel_overlap(R_dc, R_dc_dict, idc_thr)

#%% Fusión de subparcelas cuyo centro de densidad tenga intersección significativa.

fuse_subparcels(L_dc, L_dc_graph, L_overlaps, Lhemi_dict, L_sp_dict)
fuse_subparcels(R_dc, R_dc_graph, R_overlaps, Rhemi_dict, R_sp_dict)

#%% Obtención de parcelación dura (según probabilidades).

#Se utilizan copias para mantener las probabilidades originales.
Lhemi_hard = deepcopy(Lhemi_dict)
Rhemi_hard = deepcopy(Rhemi_dict)

Lparcels_hard = defaultdict(list)
Rparcels_hard = defaultdict(list)

hard_parcellation(Lhemi_hard, Lparcels_hard)
hard_parcellation(Rhemi_hard, Rparcels_hard)

#%% Creación de directorios para almacenar...

#Parcelación dura
Lhard_path = os.getcwd() + '/hard_parcels/left/'
Rhard_path = os.getcwd() + '/hard_parcels/right/'

if not os.path.exists(Lhard_path):
    os.makedirs(Lhard_path)

if not os.path.exists(Rhard_path):
    os.makedirs(Rhard_path)    

#Parcelación CC
Lparcelcc_path = os.getcwd() + '/cc_parcels/left/'
Rparcelcc_path = os.getcwd() + '/cc_parcels/right/'

if not os.path.exists(Lparcelcc_path):
    os.makedirs(Lparcelcc_path)

if not os.path.exists(Rparcelcc_path):
    os.makedirs(Rparcelcc_path)    

#Parcelación final (post-procesada)
Lfinal_path = os.getcwd() + '/final_parcels/left/'
Rfinal_path = os.getcwd() + '/final_parcels/right/'

if not os.path.exists(Lfinal_path):
    os.makedirs(Lfinal_path)

if not os.path.exists(Rfinal_path):
    os.makedirs(Rfinal_path)
    
#%% Escritura de hard parcels

for sp, tris in Lparcels_hard.items():
    bt.write_parcels(Lhard_path + sp + '.parcelsdata', tris)

for sp, tris in Rparcels_hard.items():
    bt.write_parcels(Rhard_path + sp + '.parcelsdata', tris)

#%% Lectura de hard parcels

Lparcels_hard = dict()
Rparcels_hard = dict()

for Dir in os.listdir(Lhard_path):
    Lparcels_hard[Dir.split('.')[0]] = bt.read_parcels(Lhard_path + Dir)
    
for Dir in os.listdir(Rhard_path):
    Rparcels_hard[Dir.split('.')[0]] = bt.read_parcels(Rhard_path + Dir)

#%% Cálculo de componente conexa más grande de cada parcela

Lparcel_cc = {}
Rparcel_cc = {}

for k,v in Lparcels_hard.items():
    Lparcel_cc[k] = PCC(np.array(v), Lpolygons)
    
for k,v in Rparcels_hard.items():
    Rparcel_cc[k] = PCC(np.array(v), Lpolygons)
    
#%% Escritura de parcelas CC

for sp, tris in Lparcel_cc.items():
    bt.write_parcels(Lparcelcc_path + sp + '.parcelsdata', tris)

for sp, tris in Rparcel_cc.items():
    bt.write_parcels(Rparcelcc_path + sp + '.parcelsdata', tris)

#%% Lectura de parcelas CC

Lparcel_cc = dict()
Rparcel_cc = dict()

for Dir in os.listdir(Lparcelcc_path):
    Lparcel_cc[Dir.split('.')[0]] = bt.read_parcels(Lparcelcc_path + Dir)
    
for Dir in os.listdir(Rparcelcc_path):
    Rparcel_cc[Dir.split('.')[0]] = bt.read_parcels(Rparcelcc_path + Dir)
    
#%% Opening morfológico (erosión + dilatación)

ero = 1
dil = 6

sproc.call(['make']);
sproc.call(['./felipe', Lhemi_path, Rhemi_path, str(ero), str(dil),  Lparcelcc_path, Rparcelcc_path, Lfinal_path, Rfinal_path]);

#%% Lectura de parcelas finales

Lparcels_final = dict()
Rparcels_final = dict()

for Dir in os.listdir(Lfinal_path):
    Lparcels_final[Dir.split('.')[0]] = bt.read_parcels(Lfinal_path + Dir)
    
for Dir in os.listdir(Rfinal_path):
    Rparcels_final[Dir.split('.')[0]] = bt.read_parcels(Rfinal_path + Dir)    

#%% Visualización

semilla = 48

#visualize_parcellation(Lparcels_hard, Rparcels_hard, '001', seed = semilla)
#visualize_parcellation(Lparcel_cc, Rparcel_cc, '001', seed = semilla)
visualize_parcellation(Lparcels_final, Rparcels_final, '003', seed = semilla)
   
#%% Lectura de parcelaciones guardadas como respaldo

#import pickle
#
#with open('backups/L_sp_cc.pkl', 'rb') as f:
#    Lparcel_cc = pickle.load(f)
#
#with open('backups/R_sp_cc.pkl', 'rb') as f:
#    Rparcel_cc = pickle.load(f)
#
##%%
#
#with open('L_hemi_hard.pkl', 'wb') as f:
#    pickle.dump(dict(Lhemi_hard), f)
#
#with open('R_hemi_hard.pkl', 'wb') as f:
#    pickle.dump(dict(Rhemi_hard), f)

#%% Plot density maps (this is not necessary)

parcel_idx = 42

parcel = list(L_sp_dict)[parcel_idx]
parcel_p = defaultdict(float)

for tri, v in L_sp_dict[parcel].items():
    p = v/Lhemi_dict[tri]['n']
    parcel_p[tri] = p

render = vt.Render()
    
Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; # left hemisphere path
Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; # right hemisphere path

Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)

Lhemi = vt.Polygon(Lvertex, Lpolygons);
Rhemi = vt.Polygon(Rvertex, Rpolygons);

Lhemi.setOpacity(1);
Rhemi.setOpacity(1);

render = vt.Render();

render.AddActor(Lhemi);
#render.AddActor(Rhemi);

option = 3

#Regular parcel
if option == 0:
    tris = list(parcel_p.keys())
    
    tri = vt.Polygon(Lvertex, Lpolygons[tris])
    tri.setColor((1.0,0.0,0.0))
    render.AddActor(tri)
    
    render.Start()
    del render

#Density map
elif option == 1:
    for k, v in parcel_p.items():
        tri = vt.Polygon(Lvertex, Lpolygons[[k]])
        if v < 0.2:
            continue
#            color = (0.3,0.0,0.0)
        else:
            color = (1.0,0.0,0.0)
        tri.setColor(color)
        render.AddActor(tri)
        
    render.Start()
    del render
    
#Hard parcel
elif option == 2:
    parcel_idx = 25
    parcel = list(Lparcels_hard.keys())[parcel_idx]
    tris = Lparcels_hard[parcel]    
    tri = vt.Polygon(Lvertex, Lpolygons[tris])
    tri.setColor((1.0,0.0,0.0))
    render.AddActor(tri)
    
    render.Start()
    del render

#CC's    
elif option == 3:
    parcel_idx = 25
    parcel = list(Lparcels_hard.keys())[parcel_idx]
    v = Lparcels_hard[parcel]
    (La,Lb,Lc) = PCC(np.array(v), Lpolygons)
    
    for cc in La:
        cc_tris = list(cc)
        
        ind = [np.where(Lpolygons[np.array(v)]==cc)[0] for cc in cc_tris];
        ind = np.unique(np.concatenate(ind));
        
        cc_tri = vt.Polygon(Lvertex,Lpolygons[np.array(v)[ind]])
        cc_tri.setColor((1.0,0.0,0.0))
#        cc_tri.setColor((np.random.random(),np.random.random(),np.random.random()))
        render.AddActor(cc_tri)
   
    main_tri = vt.Polygon(Lvertex,Lpolygons[Lc])
    main_tri.setColor((1.0,0.0,0.0))
    render.AddActor(main_tri)
    
    render.Start()
    del render