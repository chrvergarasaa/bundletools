# -*- coding: utf-8 -*-

import os;
import numpy as np;
import subprocess as sp;
from time import time;

def read_intersection( infile ):
    
    f = open(infile, 'rb');

    total_triangles = np.frombuffer( f.read( 4 ), np.uint32 )[ 0 ];
    
    InTri = np.frombuffer( f.read( 4 * total_triangles), np.uint32 );
    FnTri = np.frombuffer( f.read( 4 * total_triangles), np.uint32 );
    
    InPoints = np.frombuffer( f.read( 4 * 3 * total_triangles), np.float32 ).reshape(-1,3);
    FnPoints = np.frombuffer( f.read( 4 * 3 * total_triangles), np.float32 ).reshape(-1,3);
    
    fib_index = np.frombuffer( f.read( 4 * total_triangles), np.uint32 );
    
    f.close();
    return InTri, FnTri, InPoints, FnPoints, fib_index;
    
#========================== Cálculo de intersección ==========================================    

for i in range(1,80):

    t1 = time();
    
    if i < 10:
        sub = '00' + str(i);
            
    else:
        sub = '0' + str(i);
            
    print(sub);
    
    Lhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/lh.obj'; # left hemisphere path
    Rhemi_path = os.getcwd() + '/../../../../../ARCHI/' + sub + '/Meshes/rh.obj'; # left hemisphere path
    
    #Lbundles_path = os.getcwd() + '/../../../../MT/Narciso_Andrea/subs/001/tractography-streamline-regularized-deterministic_resampled_filtered_trm_ffclust/aligned_individual_clusters/';
    Rbundles_path = os.getcwd() + '/../isaias_clustering/Brain_fiber_clustering/data/79subjects/inter-clustered_QB_202/' + sub + '/individual_aligned_clusters/T1/'; # bundles path
    Lbundles_path = os.getcwd() + '/../isaias_clustering/Brain_fiber_clustering/data/79subjects/inter-clustered_QB_202/' + sub + '/individual_aligned_clusters/T1/'; # bundles path
    #Rbundles_path = os.getcwd() + '/ARCHI database/short fibers/001/right-hemi/'; # right bundles path
    
    Lintersection_path = os.getcwd() + '/intersection/' + sub + '_left-hemi/'; # left intersection path
    Rintersection_path = os.getcwd() + '/intersection/' + sub + '_right-hemi/'; # right intersection path
    
    if not os.path.exists(os.getcwd() + '/intersection/'):
        os.mkdir(os.getcwd() + '/intersection/');
    
    sp.call(['make']);
    sp.call(['./interx', Lhemi_path, Rhemi_path, Lbundles_path, Rbundles_path, Lintersection_path, Rintersection_path]);
    
    print('Tiempo de ejecución Ldirect: ' + str(time()-t1) + '[s]');
    
    del Lbundles_path, Rbundles_path;

#%%

# #================= Se lee la intersección de cada fascículo en una carpeta ====================

# LintersectionDir = os.listdir( Lintersection_path );
# LintersectionDir.sort();

# RintersectionDir = os.listdir( Rintersection_path );
# RintersectionDir.sort();

# #================= Hemisferio Izquierdo ============================        
# LlistInInd, LlistFnInd, LlistInPoints, LlistFnPoints, LlistFibInd = [], [], [], [], [];

# for intDir in LintersectionDir:
    
#     infile = Lintersection_path + intDir;
#     InTri, FnTri, InPoints, FnPoints, fib_index = read_intersection(infile);
    
#     LlistInInd.append(InTri); # índice del triángulo que intersecta con el extremo inicial de la fibra
#     LlistFnInd.append(FnTri); # índice del triángulo que intersecta con el extremo final de la fibra
#     LlistInPoints.append(InPoints); # punto exacto de intersección con el extremo inicial
#     LlistFnPoints.append(FnPoints); # punto exacto de intersección con el extremo final
#     LlistFibInd.append(fib_index); # índice de la fibra que intersecta
        
# #================= Hemisferio Derecho ===============================   
# RlistInInd, RlistFnInd, RlistInPoints, RlistFnPoints, RlistFibInd = [], [], [], [], [];

# for intDir in RintersectionDir:
    
#     infile = Rintersection_path + intDir;
#     InTri, FnTri, InPoints, FnPoints, fib_index = read_intersection(infile);
    
#     RlistInInd.append(InTri);
#     RlistFnInd.append(FnTri);
#     RlistInPoints.append(InPoints);
#     RlistFnPoints.append(FnPoints);
#     RlistFibInd.append(fib_index);
    
# del LintersectionDir, RintersectionDir, Lintersection_path, Rintersection_path;
# del Lhemi_path, Rhemi_path, intDir, infile, InTri, FnTri, InPoints, FnPoints, fib_index;

