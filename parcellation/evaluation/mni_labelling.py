#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:20:38 2020

@author: fondecyt-1190701
"""

import nibabel as nib
import os
import bundleTools as bt
import numpy as np
import pickle
from statistics import mode
from collections import defaultdict

#%% Lectura de atlas Brainnetome en formato NIFTI (vóxeles etiquetados).
atlas_nib = nib.load('BN_Atlas_246_1mm.nii.gz')
atlas_img = np.asanyarray(atlas_nib.dataobj)

#%% Transforma matrices en formato trm (3x3) a formato estándar (coordenadas, homogéneas, 4x4).
def trm_to_std(trm):
    T0 = trm[0,0];
    T1 = trm[0,1];
    T2 = trm[0,2];
    A0 = trm[1,0];
    A1 = trm[1,1];
    A2 = trm[1,2];
    B0 = trm[2,0];
    B1 = trm[2,1];
    B2 = trm[2,2];
    C0 = trm[3,0];
    C1 = trm[3,1];
    C2 = trm[3,2];
    
    std = np.array(([A0,A1,A2,T0],
                    [B0,B1,B2,T1],
                    [C0,C1,C2,T2],
                    [0,0,0,1]))    
    return std

#%% 
#Lectura de mallado cortical izquierdo y derecho (en Talairach).
    #Nota: El atlas de Brainnetome está en espacio MNI, que está "cerca" de Talairach. No se transformó el mallado a espacio MNI por falta de tiempo.
sub = '001';
Lhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/lh_tal.obj'; 
Rhemi_path = os.getcwd() + '/../../../../../ARCHI/Meshes_OBJ/' + sub + '/rh_tal.obj'; 

Lvertex, Lpolygons = bt.read_transformed_mesh_obj(Lhemi_path)
Rvertex, Rpolygons = bt.read_transformed_mesh_obj(Rhemi_path)

# Triángulos vecinos de cada triángulo del mallado.
Lneighbors = bt.mesh_neighbors(Lpolygons)
Rneighbors = bt.mesh_neighbors(Rpolygons)

#%% LEFRANC ATLAS

#Lectura de atlas en formato GIFTI (vértices etiquetados).
lefranc_atlas = nib.load('constellation_clusters.gii')
lefranc_data = [x.data for x in lefranc_atlas.darrays]

#Separación de etiquetas en hemisferio izquierdo y derecho.
lh_vertex_labels = list(lefranc_data[0][0:40962])
rh_vertex_labels = list(lefranc_data[0][40962:])
        
#Lista para guardar etiquetas de polígonos (triángulos).
#De manera arbitraria, se elige asignar a cada triángulo la etiqueta que más se repite entre las de los vértices que lo tocan.
lh_poly_labels = []

#Se itera sobre cada triángulo...
for i, vertices in enumerate(Lpolygons):
    p_labels = []
    
    #Se obtienen las etiquetas de todos los vértices que tocan al triángulo...
    for vertex in vertices:
        p_labels.append(lh_vertex_labels[vertex])
    
    #...y se obtiene la moda. 
    try:
        lh_poly_labels.append(mode(p_labels))
        
    #De no existir moda, se asigna arbitrariamente la etiqueta del primer vértice.
    except:
        lh_poly_labels.append(p_labels[0])
            
#Se repite lo mismo para el hemisferio derecho.
rh_poly_labels = []

for i, vertices in enumerate(Rpolygons):
    p_labels = []
    for vertex in vertices:
        p_labels.append(rh_vertex_labels[vertex])
                
    try:
        rh_poly_labels.append(mode(p_labels))
        
    except:
        rh_poly_labels.append(p_labels[0])

#Se crea también un diccionario que asocia a cada etiqueta la lista de triángulos en los que aparece.
lh_labels_dict = defaultdict(list)

#Ignoramos las que tengan un valor de -1 (honestamente no recuerdo por qué existe el valor -1, pero no está en la descripción de parcelas anatómicas). 
for i, label in enumerate(lh_poly_labels):
    if label != -1:
        lh_labels_dict[label].append(i)

#Ídem para el hemisferio derecho.
rh_labels_dict = defaultdict(list)

for i, label in enumerate(rh_poly_labels):
    if label != -1:
        rh_labels_dict[label].append(i)
     
#Las etiquetas 11 y 407 representan zonas que no pertenecen a la corteza => no pueden existir parcelas en estos triángulos.
Lnope = lh_labels_dict[11]
Rnope = rh_labels_dict[407]

#Guardamos los triángulos restringidos para su uso en otro código.
with open('Lnope.pkl', 'wb') as f:
    pickle.dump(Lnope, f)
    
with open('Rnope.pkl', 'wb') as f:
    pickle.dump(Rnope, f)

del lh_labels_dict[11]
del rh_labels_dict[407]

#Guardamos las etiquetas válidas.
with open('Lefranc_Lparcels.pkl', 'wb') as f:
    pickle.dump(dict(lh_labels_dict), f)

with open('Lefranc_Rparcels.pkl', 'wb') as f:
    pickle.dump(dict(rh_labels_dict), f)

#%% BRAINNETOME ATLAS

#Matriz de coordenadas en mm a coordenadas en vóxeles.
mm_to_vox_trm = np.zeros((4,3))

#Lectura desde archivo .trm (matriz en formato de Anatomist).
#DISCLAIMER: La verdad tampoco recuerdo bien de donde saqué la transformación mm->vox para Brainnetome.
i = 0
with open('brainnetome_mm_to_vox_2.trm', 'r') as f:
    for line in f:
        j = 0
        for num in line.split():
            mm_to_vox_trm[i][j] = num
            j += 1
        i += 1
    
#Transformación de matriz a coordenadas homogéneas (4x4).
mm_to_vox = trm_to_std(mm_to_vox_trm)

#Lista para almacenar etiquetas de vértices. 
#En el caso de este atlas, debemos proyectar la etiqueta de cada vóxel al vértice más cercano.
#Para esto, hacemos el proceso inverso: tomamos la coordenada en mm de cada vértice, la transformamos a vóxel, y redondeamos al entero más cercano.
#Finalmente, le asignamos a ese vértice la etiqueta correspondiente.
lh_vertex_labels = []

#Para cada vértice...
for v in Lvertex:
    #...obtenemos las coordenadas en mm...
    x = v[0]
    y = v[1]
    z = v[2]
    
    #...las transformamos a vóxeles
    vox = nib.affines.apply_affine(mm_to_vox,[x,y,z])
    
    #...las redondeamos al entero más cercano...
    vox_x = int(round(vox[0]))
    vox_y = int(round(vox[1]))
    vox_z = int(round(vox[2]))
    
    #...y obtenemos la etiqueta correspondiente al vóxel.
    #Los términos 217 y 181 son para invertir los ejes Y y Z, ya que el mallado está en coordenadas LPI, mientras que el atlas está en LAS.
    lh_vertex_labels.append(atlas_img[vox_x,217-vox_y,181-vox_z])
    
#Lo mismo para el hemisferio derecho.
rh_vertex_labels = []

for v in Rvertex:
    x = v[0]
    y = v[1]
    z = v[2]
    
    vox = nib.affines.apply_affine(mm_to_vox,[x,y,z])
    
    vox_x = int(round(vox[0]))
    vox_y = int(round(vox[1]))
    vox_z = int(round(vox[2]))
    
    rh_vertex_labels.append(atlas_img[vox_x,217-vox_y,181-vox_z])
 
#Al igual que con Lefranc, se pasan las etiquetas de vértices a etiquetas de triángulos utilizando la moda de los vértices adyacentes.
lh_poly_labels = []

for i, vertices in enumerate(Lpolygons):
    p_labels = []
    
    for vertex in vertices:
        p_labels.append(lh_vertex_labels[vertex])
                
    try:
        lh_poly_labels.append(mode(p_labels))
        
    except:
        lh_poly_labels.append(0)
            
#Lo mismo para el hemisferio derecho.
rh_poly_labels = []

for i, vertices in enumerate(Rpolygons):
    p_labels = []
    for vertex in vertices:
        p_labels.append(rh_vertex_labels[vertex])
                
    try:
        rh_poly_labels.append(mode(p_labels))
        
    except:
        rh_poly_labels.append(0)

#%% Debido a que el mapeo de mallado a vértice no es uno a uno, muchos de los vértices quedan sin etiqueta.
#Luego, a aquellos vértices con etiqueta 0 (sin etiqueta) les asignamos la moda de las etiquetas de sus triángulos vecinos.
#Al repetir esto, eventualmente todos los triángulos tendrán una etiqueta asignada.

flag = 0

while(flag == 0):
    flag = 1
    for i, label in enumerate(lh_poly_labels):
        if label == 0:
            flag = 0
            neighbors = Lneighbors[i]        
            neighbors_labels = []
    
            for nbor in neighbors:
                nbor_label = lh_poly_labels[nbor]
                
                if nbor_label != 0:
                    neighbors_labels.append(nbor_label)
                        
            if len(neighbors_labels) == 0:
                continue
            
            else:
                try:
                    lh_poly_labels[i] = mode(neighbors_labels)
                    
                except:
                    lh_poly_labels[i] = neighbors_labels[0]

flag = 0
while(flag == 0):
    flag = 1        
    for i, label in enumerate(rh_poly_labels):
        if label == 0:
            flag = 0
            neighbors = Rneighbors[i]        
            neighbors_labels = []
    
            for nbor in neighbors:
                nbor_label = rh_poly_labels[nbor]
                
                if nbor_label != 0:
                    neighbors_labels.append(nbor_label)
                
            if len(neighbors_labels) == 0:
                continue
            
            else:
                try:
                    rh_poly_labels[i] = mode(neighbors_labels)
                    
                except:
                    rh_poly_labels[i] = neighbors_labels[0]

#%% Se llena un diccionario etiquetas:triángulos para ambos hemisferios, al igual que con Lefranc.
# Se descartan las iguales a -1, o aquellas de triángulos que están en zonas no-válidas (Lnope y Rnope).
                    
lh_labels_dict = defaultdict(list)

for i, label in enumerate(lh_poly_labels):
    if i in Lnope:
        continue
    
    if label != -1:
        lh_labels_dict[label].append(i)

rh_labels_dict = defaultdict(list)

for i, label in enumerate(rh_poly_labels):
    if i in Rnope:
        continue
    
    if label != -1:
        rh_labels_dict[label].append(i)
       
#%% Se guardan las etiquetas en el disco.
        
with open('Brainnetome_Lparcels.pkl', 'wb') as f:
    pickle.dump(dict(lh_labels_dict), f)

with open('Brainnetome_Rparcels.pkl', 'wb') as f:
    pickle.dump(dict(rh_labels_dict), f)

#%% Se selecciona una paleta de colores cualquiera para las etiquetas.
paleta = []  
with open('rainbow2-fusion.ima', 'r') as f:
    for line in f:
        paleta.append(eval(line.rstrip('\n')))

#%% Lectura de parcelas desde disco.
with open('Brainnetome_Lparcels.pkl', 'rb') as f:
    lh_labels_dict = pickle.load(f)

with open('Brainnetome_Rparcels.pkl', 'rb') as f:
    rh_labels_dict = pickle.load(f)

#%% Visualización.
import visualizationTools as vt

#Mallados corticales.
Lhemi = vt.Polygon(Lvertex, Lpolygons);
Rhemi = vt.Polygon(Rvertex, Rpolygons);

#Opacidad de mallados.
Lhemi.setOpacity(1);
Rhemi.setOpacity(1);

#Creación de render.
render = vt.Render();

#Dibujado de mallado.
render.AddActor(Lhemi);
render.AddActor(Rhemi);

for label, tris in lh_labels_dict.items():
    
    real_label = int((246.0/217.0)*label)
    
    if real_label > 255:
        real_label = 255
        
    color = paleta[real_label]
        
    tri = vt.Polygon(Lvertex, Lpolygons[tris])
    tri.setColor((color[0]/255.0,color[1]/255.0,color[2]/255.0))
    
#    color = (np.random.random(),np.random.random(),np.random.random())
#    tri.setColor(color)
    
    render.AddActor(tri)

for label, tris in rh_labels_dict.items():

    real_label = int((246.0/217.0)*label)
    
    if real_label > 255:
        real_label = 255
    
    color = paleta[real_label]

    tri = vt.Polygon(Rvertex, Rpolygons[tris])
    tri.setColor((color[0]/255.0,color[1]/255.0,color[2]/255.0))
    
#    color = (np.random.random(),np.random.random(),np.random.random())
#    tri.setColor(color)

    render.AddActor(tri)
    
render.Start()
del render
