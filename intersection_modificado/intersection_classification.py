#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:37:53 2020

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

clustering_method = 'HDB_1_652'

for i in range(1,80):

    if i < 10:    
        sub = '00' + str(i);
        
    else:
        sub = '0' + str(i);
    
    print(sub);
    
    t1 = time();
    
    # Lhemi_path = os.getcwd() + '/meshes/' + sub + '/' + sub + '_Lhemi.mesh';
    # Rhemi_path = os.getcwd() + '/meshes/' + sub + '/' + sub + '_Rhemi.mesh';
    
    # Lvertex, Lpolygons = bt.read_mesh(Lhemi_path);
    # Rvertex, Rpolygons = bt.read_mesh(Rhemi_path);
    
    
    # bundles_path = os.getcwd() + '/../../subs/' + sub + '/tractography-streamline-regularized-deterministic_resampled_filtered_trm_ffclust/aligned_individual_clusters/'; # bundles path
    # centroid_path = os.getcwd() + '/../../subs/' + sub + '/tractography-streamline-regularized-deterministic_resampled_filtered_trm_ffclust/individual_centroids/'; # centroids path
    # classification_path = os.getcwd() + '/bundle_classification/' + sub + '/';
    
    # cluster_dirs = glob.glob(bundles_path + '*.bundles');
    # cluster_names = [];
    
    # for Dir in cluster_dirs:
    #     cluster_names.append(Dir[187:-8]);
    
    Ldirect_path = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/L-L_direct/'; # membership path
    Linverse_path = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/L-L_inverse/'; # membership path
    Rdirect_path = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/R-R_direct/'; # membership path
    Rinverse_path = os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/R-R_inverse/'; # membership path
    
    if not os.path.exists(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/L-L/'):
        os.makedirs(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/L-L/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/L-R/'):
        os.makedirs(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/L-R/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/R-L/'):
        os.makedirs(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/R-L/');
    
    if not os.path.exists(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/R-R/'):
        os.makedirs(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/R-R/');    
        
    if not os.path.exists(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/Inter/'):
        os.makedirs(os.getcwd() + '/intersection/' + clustering_method + '/' + sub + '/Final/Inter/');
    
    LL_path = os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-L/';
    LR_path = os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-R/';
    RL_path = os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-L/';
    RR_path = os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-R/';
    
    LL_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(LL_path + '*.bundles')];
    LR_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(LR_path + '*.bundles')];
    RL_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(RL_path + '*.bundles')];
    RR_list = [os.path.basename(os.path.splitext(x)[0]) for x in glob.glob(RR_path + '*.bundles')];
    
    #LL_list contiene la lista de todos los clusters que son intra L-hemi.
    #Ldirect_path 
    
    LL_weird = [];
    LR_weird = [];
    RL_weird = [];
    RR_weird = [];
    
    for cluster in LL_list:
        Ld_infile = Ldirect_path + cluster + '.intersectiondata';
        Li_infile = Linverse_path + cluster + '.intersectiondata';
        
        if os.path.exists(Ld_infile): 
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Ld_infile);
            intra_idx = np.where(FnTri != 1000000);
            InTri = InTri[intra_idx];
            n_tri = np.uint32(len(InTri));
            
            if n_tri == 0:
                InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Li_infile);
                intra_idx = np.where(FnTri != 1000000);
                InTri = InTri[intra_idx];
                n_tri = np.uint32(len(InTri));
                
            else:
                FnTri = FnTri[intra_idx];
                InPoints = InPoints[intra_idx];
                FnPoints = FnPoints[intra_idx];
                fib_index = fib_index[intra_idx];
                
                f = open(Ldirect_path + '../Final/L-L/' + cluster + '.intersectiondata', 'wb+');
                
                f.write(n_tri);
                
                f.write(InTri);
                f.write(FnTri);
                
                f.write(InPoints);
                f.write(FnPoints);
                
                f.write(fib_index);
                
                f.close();    
            
        elif os.path.exists(Li_infile):
            InTri, FnTri, InPoints, FnPoints, fib_index = bt.read_intersection(Li_infile);
            intra_idx = np.where(FnTri != 1000000);
            InTri = InTri[intra_idx];
            n_tri = np.uint32(len(InTri));
            
            if n_tri == 0:
                move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-L/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundles');
                move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-L/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundlesdata');
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


    for cluster in LR_list:
        
        infile = Ldirect_path + cluster + '.intersectiondata';    
        
        if not os.path.exists(infile):
            LR_weird.append(cluster);
            continue;
        
        InTri_direct, FnTri_direct, InPoints_direct, FnPoints_direct, fib_index_direct = bt.read_intersection(infile);
    
        infile = Rinverse_path + cluster + '.intersectiondata';
        
        if not os.path.exists(infile):
            LR_weird.append(cluster);
            continue;
    
        InTri_reverse, FnTri_reverse, InPoints_reverse, FnPoints_reverse, fib_index_reverse = bt.read_intersection(infile);
    
        fib_index_direct = fib_index_direct[np.in1d(fib_index_direct, fib_index_reverse)];
        fib_index_reverse = fib_index_reverse[np.in1d(fib_index_reverse, fib_index_direct)];
        
        InTri_direct = InTri_direct[fib_index_direct.argsort()];
        InTri_reverse = InTri_reverse[fib_index_reverse.argsort()];

        fib_index_direct = np.sort(fib_index_direct);

        n_tri = np.uint32(len(InTri_direct));
    
        if n_tri == 0:
            move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-R/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundles');
            move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/L-R/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundlesdata');
            continue;
    
        f = open(Ldirect_path + '../Final/Inter/' + cluster + '.intersectiondata', 'wb+');
    
        f.write(n_tri);

        f.write(InTri_direct);
        f.write(InTri_reverse);
        
        f.write(InPoints_direct);
        f.write(InPoints_reverse);
    
        fib_index_direct = np.sort(fib_index_direct);
        f.write(fib_index_direct);
    
        f.close();
        
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
            move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-L/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundles');
            move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-L/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundlesdata');
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
                move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-R/' + cluster + '.bundles', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundles');
                move(os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/R-R/' + cluster + '.bundlesdata', os.getcwd() + '/bundle_classification/' + clustering_method + '/' + sub + '/Discarded/' + cluster + '.bundlesdata');
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
    
