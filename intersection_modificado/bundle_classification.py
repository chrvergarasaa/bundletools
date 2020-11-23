#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:25:51 2020

@author: christopher
"""

import os;
import numpy as np;
import subprocess as sp;
from shutil import copyfile, move;
import glob;
import utils.bundleTools as bt;
from time import time;
import sys;

clustering_method = 'QB_202'

for i in range(1,80):
    
    if i < 10:
        sub = '00' + str(i);
        
    else:
        sub = '0' + str(i);
    
    print(sub);
    
    t1 = time();
    
    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/lh.obj'; # left hemisphere path
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/rh.obj'; # right hemisphere path
    
#    Lvertex, Lpolygons = bt.read_mesh(Lhemi_path);
#    Rvertex, Rpolygons = bt.read_mesh(Rhemi_path);
    
    bundles_path = os.getcwd() + '/../isaias_clustering/Brain_fiber_clustering/data/79subjects/inter-clustered_' + clustering_method + '/' + sub + '/individual_aligned_clusters/T1/'; # bundles path
    # centroid_path = os.getcwd() + '/../../subs/' + sub + '/tractography-streamline-regularized-deterministic_resampled_filtered_trm_ffclust/individual_centroids/'; # centroids path
    classification_path = os.getcwd() + '/bundle_classification/' + clustering_method + '/'  + sub + '/';
    
    cluster_names = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(bundles_path + '*.bundles')];
    
    Ldirect_path = os.getcwd() + '/membership/' + clustering_method + '/' + sub + '/L-L_direct/'; # membership path
    Linverse_path = os.getcwd() + '/membership/' + clustering_method + '/' + sub + '/L-L_inverse/'; # membership path
    Rdirect_path = os.getcwd() + '/membership/' + clustering_method + '/' + sub + '/R-R_direct/'; # membership path
    Rinverse_path = os.getcwd() + '/membership/' + clustering_method + '/' + sub + '/R-R_inverse/'; # membership path
    
    ###---------- Creación de diccionario ----------###
    memb_dict = {};
    
    for name in cluster_names:
        Ldirect = Ldirect_path + name + '.membershipdata';
        Linverse = Linverse_path + name + '.membershipdata';
        Rdirect = Rdirect_path + name + '.membershipdata';
        Rinverse = Rinverse_path + name + '.membershipdata';
        
        with open(Ldirect, 'rb') as f1, open(Linverse, 'rb') as f2, open(Rdirect, 'rb') as f3, open(Rinverse, 'rb') as f4:
            Ldirect_flags = tuple(f1.read( 2 ));
            Linverse_flags = tuple(f2.read( 2 ));
            Rdirect_flags = tuple(f3.read( 2 ));
            Rinverse_flags = tuple(f4.read( 2 ));
        
        memb_dict[name] = {'Ldirect': Ldirect_flags, 'Linverse': Linverse_flags, 'Rdirect': Rdirect_flags, 'Rinverse': Rinverse_flags};

    
    ###---------- Creación de directorios de clasificación ----------###
    if not os.path.exists(classification_path + 'L-L/'):
        os.makedirs(classification_path + 'L-L/');
        
    if not os.path.exists(classification_path + 'R-R/'):
        os.makedirs(classification_path + 'R-R/');
        
    if not os.path.exists(classification_path + 'L-R/'):
        os.makedirs(classification_path + 'L-R/');
        
    if not os.path.exists(classification_path + 'R-L/'):
        os.makedirs(classification_path + 'R-L/');
        
    if not os.path.exists(classification_path + 'Discarded/'):
        os.makedirs(classification_path + 'Discarded/');
        
    if not os.path.exists(classification_path + 'Ambiguous/'):
        os.makedirs(classification_path + 'Ambiguous/');
        
    LR_midline_cluster_names = [];
    RL_midline_cluster_names = [];
    
    ambiguous = [];
    
    for cluster in memb_dict:
        Ldirect_flags = memb_dict[cluster]['Ldirect'];
        Linverse_flags = memb_dict[cluster]['Linverse'];
        Rdirect_flags = memb_dict[cluster]['Rdirect'];
        Rinverse_flags = memb_dict[cluster]['Rinverse'];
            
        count = sum(Ldirect_flags) + sum(Linverse_flags) + sum(Rdirect_flags) + sum(Rinverse_flags);
            
        if (Ldirect_flags == (1,1) or Linverse_flags == (1,1)) and (Rdirect_flags == (0,0) and Rinverse_flags == (0,0)): 
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
    
        elif (Rdirect_flags == (1,1) or Rinverse_flags == (1,1)) and (Ldirect_flags == (0,0) and Linverse_flags == (0,0)):
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
    
        elif Ldirect_flags == (1,0) and Rinverse_flags == (1,0):
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'L-R/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'L-R/' + cluster + '.bundlesdata');
            
        elif Rdirect_flags == (1,0) and Linverse_flags == (1,0):
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'R-L/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'R-L/' + cluster + '.bundlesdata');
        
        elif count <= 1:
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'Discarded/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'Discarded/' + cluster + '.bundlesdata');    
    
        else:
            copyfile(bundles_path + cluster + '.bundles', classification_path + 'Ambiguous/' + cluster + '.bundles');
            copyfile(bundles_path + cluster + '.bundlesdata', classification_path + 'Ambiguous/' + cluster + '.bundlesdata');
            ambiguous.append(cluster);
                       
    for cluster in ambiguous:
            
        Ld = memb_dict[cluster]['Ldirect'];
        Li = memb_dict[cluster]['Linverse'];
        Rd = memb_dict[cluster]['Rdirect'];
        Ri = memb_dict[cluster]['Rinverse'];
        
        Ld_int = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/L-L_direct/' + cluster + '.intersectiondata';
        Li_int = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/L-L_inverse/' + cluster + '.intersectiondata';
        Rd_int = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/R-R_direct/' + cluster + '.intersectiondata';
        Ri_int = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/R-R_inverse/' + cluster + '.intersectiondata';
        
        intra_Ld = 0;
        intra_Li = 0;
        intra_Rd = 0;
        intra_Ri = 0;
        inter_LR = 0;
        inter_RL = 0;
    
        if Ld == (1,1):
            Ld_FnTri = bt.read_intersection(Ld_int)[1];
            intra_idx = np.where(Ld_FnTri != 1000000);
            intra_Ld = len(Ld_FnTri[intra_idx]);
            
        if Li == (1,1):
            Li_FnTri = bt.read_intersection(Li_int)[1];
            intra_idx = np.where(Li_FnTri != 1000000);
            intra_Li = len(Li_FnTri[intra_idx]);    
        
        if Rd == (1,1):
            Rd_FnTri = bt.read_intersection(Rd_int)[1];
            intra_idx = np.where(Rd_FnTri != 1000000);
            intra_Rd = len(Rd_FnTri[intra_idx]);
            
        if Ri == (1,1):
            Ri_FnTri = bt.read_intersection(Ri_int)[1];
            intra_idx = np.where(Ri_FnTri != 1000000);
            intra_Ri = len(Ri_FnTri[intra_idx]);    
            
        if (Ld == (1,1) or Ld == (1,0)) and (Ri == (1,1) or Ri == (1,0)):
            Ld_FnTri = bt.read_intersection(Ld_int)[1];
            
            fib_direct = bt.read_intersection(Ld_int)[-1];
            fib_inverse = bt.read_intersection(Ri_int)[-1];
            
            fib_direct_inter = fib_direct[np.where(Ld_FnTri == 1000000)]
            
            inter_LR = sum(np.isin(fib_inverse, fib_direct_inter))
                                                            
        if (Rd == (1,1) or Rd == (1,0)) and (Li == (1,1) or Li == (1,0)):
            Rd_FnTri = bt.read_intersection(Rd_int)[1];
            
            fib_direct = bt.read_intersection(Rd_int)[-1];
            fib_inverse = bt.read_intersection(Li_int)[-1];
            
            fib_direct_inter = fib_direct[np.where(Rd_FnTri == 1000000)]
            
            inter_RL = sum(np.isin(fib_inverse, fib_direct_inter))        
                        
        dom = max(intra_Ld,intra_Li,intra_Rd,intra_Ri,inter_LR,inter_RL);
        dom_idx = np.argmax([intra_Ld,intra_Li,intra_Rd,intra_Ri,inter_LR,inter_RL]);
        
        #No intersection
        if dom == 0:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'Discarded/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'Discarded/' + cluster + '.bundlesdata');
        
        #L_direct
        elif dom_idx == 0:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
            os.remove(Li_int)            
            
        #L_inverse    
        elif dom_idx == 1:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-L/' + cluster + '.bundlesdata');
            os.remove(Ld_int)
            
        #R_direct
        elif dom_idx == 2:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
            os.remove(Ri_int)

        #R_inverse            
        elif dom_idx == 3:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-R/' + cluster + '.bundlesdata');
            os.remove(Rd_int)
            
        #L-R
        elif dom_idx == 4: 
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'L-R/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'L-R/' + cluster + '.bundlesdata');
    
        #R-L
        elif dom_idx == 5:
            move(classification_path + 'Ambiguous/' + cluster + '.bundles', classification_path + 'R-L/' + cluster + '.bundles');
            move(classification_path + 'Ambiguous/' + cluster + '.bundlesdata', classification_path + 'R-L/' + cluster + '.bundlesdata');
    

    print('Tiempo de ejecución: ' + str(time()-t1) + '[s]');