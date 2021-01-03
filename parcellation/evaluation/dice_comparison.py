#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:03:50 2020

@author: fondecyt-1190701
"""

import os
import bundleTools as bt
from statistics import mode
from collections import defaultdict
import pickle
import numpy as np
import visualizationTools as vt

#%%

#Cálculo de Dice Score entre dos conjuntos A y B.
def DSC(A,B):
    set_A = set(A)
    set_B = set(B)
    
    interx = set_A.intersection(set_B)
    
    return (2*len(interx))/((len(set_A)+len(set_B)))

#Visualización de parcelación (similar a la encontrada en el script Parcellation).
def visualize_parcellation(L_sp, R_sp, sub, seed = False):
    if seed != False:
        np.random.seed(seed)
    
    n_parcels = len(L_sp.keys()) + len(R_sp.keys())
    
    paleta = [(np.random.random(), np.random.random(), np.random.random()) for i in range(n_parcels)]

    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; # left hemisphere path
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; # right hemisphere path

    Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
    Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)
    
    Lhemi = vt.Polygon(Lvertex, Lpolygons);
    Rhemi = vt.Polygon(Rvertex, Rpolygons);
    
    Lhemi.setOpacity(1);
    Rhemi.setOpacity(1);
    
    render = vt.Render();
    
#    render.AddActor(Lhemi);
    render.AddActor(Rhemi);
    
    for k, v in L_sp.items():
        color = paleta[lh_index[k]]
#        color = paleta[fp.index(k)]
    
        if len(v) == 0:
            continue
    
        sp_tri = vt.Polygon(Lvertex, Lpolygons[v]);
        sp_tri.setColor((color[0], color[1], color[2]));
#        render.AddActor(sp_tri);

    for k, v in R_sp.items():
        color = paleta[rh_index[k]]
#        color = paleta[fp.index(k)]
    
        if len(v) == 0:
            continue
    
        sp_tri = vt.Polygon(Rvertex, Rpolygons[v]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);
    
    render.Start();
    del render
    
#%%    

#Sujeto a graficar.
sub = '001'

#Lectura de etiquetas del atlas de Narciso López (creado también sobre mallado ARCHI).
atlas = 'narciso'
lh_atlas_path = 'atlas/' + atlas + '/' + atlas + '_lh_labels_13.txt'
rh_atlas_path = 'atlas/' + atlas + '/' + atlas + '_rh_labels_13.txt'

#Al igual que Lefranc, este atlas tiene vértices etiquetados, por lo que el proceso es similar.
lh_atlas_dict = defaultdict(list)
rh_atlas_dict = defaultdict(list)

lh_vertex_labels = []
rh_vertex_labels = []

#Se leen los archivos de texto que contienen las etiquetas de cada vértice.
with open(lh_atlas_path, 'r') as f:
    for line in f:
        lh_vertex_labels.append(int(line.rstrip('\n')))
        lh_atlas_dict[int(line.rstrip('\n'))] = []

#Lo mismo para el hemisferio derecho.
with open(rh_atlas_path, 'r') as f:
    for line in f:
        rh_vertex_labels.append(int(line.rstrip('\n')))
        rh_atlas_dict[int(line.rstrip('\n'))] = []
        
#Y luego se vuelve a repetir el proceso de asignar a cada triángulo la moda de las etiquetas de los vértices adyacentes.
Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh.obj'; 
Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh.obj'; 

Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)

lh_poly_labels = []
rh_poly_labels = []

for i, vertices in enumerate(Lpolygons):
    p_labels = []
    for vertex in vertices:
        p_labels.append(lh_vertex_labels[vertex])
                
    try:
        lh_poly_labels.append(mode(p_labels))
        lh_atlas_dict[mode(p_labels)].append(i)
        
    except:
#        lh_poly_labels.append(-1)
        lh_poly_labels.append(p_labels[0])
            
for i, vertices in enumerate(Rpolygons):
    p_labels = []
    for vertex in vertices:
        p_labels.append(rh_vertex_labels[vertex])
        
    try:
        rh_poly_labels.append(mode(p_labels))
        rh_atlas_dict[mode(p_labels)].append(i)
        
    except:
#        rh_poly_labels.append(-1)
        rh_poly_labels.append(p_labels[0])
        

#%% Se cargan desde disco los triángulos con restricción, obtenidos desde el atlas de Lefranc.

with open('Lnope.pkl', 'rb') as f:
    Lnope = pickle.load(f)
    
with open('Rnope.pkl', 'rb') as f:
    Rnope = pickle.load(f)

#%% Se eliminan los triángulos con restricción.

lh_labels_dict = defaultdict(list)

for i, label in enumerate(lh_poly_labels):
    if i in Lnope:
        continue
    
    lh_labels_dict[label].append(i)

rh_labels_dict = defaultdict(list)

for i, label in enumerate(rh_poly_labels):
    if i in Rnope:
        continue
    
    rh_labels_dict[label].append(i)


#%% Se guardan las parcelas obtenidas por Narciso.

with open('Narciso_Lparcels.pkl', 'wb') as f:
    pickle.dump(dict(lh_labels_dict), f)
    
with open('Narciso_Rparcels.pkl', 'wb') as f:
    pickle.dump(dict(rh_labels_dict), f)

#%% Lectura de parcelas propias.

#Las parcelas obtenidas están en formato binario .parcelsdata, que contiene los triángulos correspondientes a cada parcela.
lh_mine_path = os.getcwd() + '/final_parcels/left/'
rh_mine_path = os.getcwd() + '/final_parcels/right/'

#Se crea un diccionario parcela:triángulos.
lh_mine_dict = dict()
rh_mine_dict = dict()

#Se utiliza la función read_parcels.
for Dir in os.listdir(lh_mine_path):
    lh_mine_dict[Dir.split('.')[0]] = bt.read_parcels(lh_mine_path + Dir)
    
for Dir in os.listdir(rh_mine_path):
    rh_mine_dict[Dir.split('.')[0]] = bt.read_parcels(rh_mine_path + Dir)
    
#%% Selección de atlas a comparar.

atlases = ['Lefranc','Brainnetome','Narciso']

# Índice del atlas a escoger.
selection = 0

# Cargar parcelación del atlas seleccionado.
with open(atlases[selection] + '_Lparcels.pkl', 'rb') as f:   
    lh_atlas_dict = pickle.load(f)

with open(atlases[selection] + '_Rparcels.pkl', 'rb') as f:   
    rh_atlas_dict = pickle.load(f)    
    
#%% Cálculo de DSC entre parcelas.

# Diccionario parcela_propia:parcela_atlas, para aquellos casos que superan el umbral de DSC.
lh_dice_dict = defaultdict(int)
rh_dice_dict = defaultdict(int)

lh_index = defaultdict(int)
rh_index = defaultdict(int)

# Lista que almacena las parcelas ya utilizadas.
used = []

# Umbral de DSC a utilizar (% de similitud).
dice_thr = 0.6

# Iteración sobre todas las parcelas propias obtenidas.
for parcel, tris in lh_mine_dict.items():
    #Se registra el mayor DSC obtenido entre todas las comparaciones, y el nombre de la parcela asociada.
    dice_max = 0
    winner = ''
  
    #Se itera sobre las parcelas del atlas.
    for ref, rtris in lh_atlas_dict.items():
        
        #Si la parcela ya fue utilizada, ignorar.
        if ref in used:
            continue
        
        #Cálculo de DSC entre parcela propia y parcela del atlas.
        dice = DSC(tris,rtris)
        
        #Si es mayor al máximo obtenido, actualizar.
        if dice > dice_max:
            dice_max = dice
            winner = ref
    
    #Si el mayor valor obtenido supera el umbral de similitud, se agrega al diccionario de parcelas similares, y a la lista de parcelas ya utilizadas.
    if dice_max >= dice_thr:
        lh_dice_dict[parcel] = winner
#        lh_dice_dict[parcel] = (winner,dice_max)
        used.append(winner)
        
        lh_index[parcel] = i
        lh_index[winner] = i
        
        i += 1
        
    # Si no supera el umbral, continuar con la siguiente parcela.
    else:
        continue

#Se repite lo mismo para el hemisferio derecho.
used = []

for parcel, tris in rh_mine_dict.items():
    dice_max = 0
    winner = ''
  
    for ref, rtris in rh_atlas_dict.items():
        if ref in used:
            continue
        dice = DSC(tris,rtris)
        if dice > dice_max:
            dice_max = dice
            winner = ref
        
    if dice_max >= dice_thr:
        rh_dice_dict[parcel] = winner
#        rh_dice_dict[parcel] = (winner,dice_max)
        used.append(winner)
        
        rh_index[parcel] = i
        rh_index[winner] = i
        
        i += 1

    else:
        continue  


#Diccionario de parcelas similares, considerando los triángulos asociados en el caso de la parcelación propia.
lh_mine_common = {k:lh_mine_dict[k] for k in list(lh_dice_dict.keys()) if k in lh_mine_dict}
rh_mine_common = {k:rh_mine_dict[k] for k in list(rh_dice_dict.keys()) if k in rh_mine_dict}

#Diccionario de parcelas similares, considerando los triángulos asociados en el caso de la parcelación del atlas.
lh_atlas_common = {k:lh_atlas_dict[k] for k in list(lh_dice_dict.values()) if k in lh_atlas_dict}
rh_atlas_common = {k:rh_atlas_dict[k] for k in list(rh_dice_dict.values()) if k in rh_atlas_dict}

#%% Visualización de parcelas con DSC superior al umbral.

visualize_parcellation(lh_mine_common, rh_mine_common, '001', seed = 47)

#visualize_parcellation(lh_atlas_common, rh_atlas_common, '001', seed = 47)
#
#visualize_parcellation(lh_atlas_dict, rh_atlas_dict, '001', seed = 67)
    
