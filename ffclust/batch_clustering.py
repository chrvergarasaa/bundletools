# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os;
import glob;
from time import time;

for i in range(2,80):

    if i <= 9:
        sub = '00' + str(i);
    else:
        sub = '0' + str(i);
    
    bundles_path = '../../../../../../../HDD/Ubuntu/ARCHI/' + sub + '/OverSampledFibers/';

    print(i);

    if not os.path.exists('../../../../../../../HDD/Ubuntu/Chris/MT/inter-bundle-master/codes/isaias_clustering/Brain_fiber_clustering/data/79subjects/clustered_2/' + sub + '/'):
        os.makedirs('../../../../../../../HDD/Ubuntu/Chris/MT/inter-bundle-master/codes/isaias_clustering/Brain_fiber_clustering/data/79subjects/clustered_2/' + sub + '/')

    t1 = time();
    os.system('python main.py' + ' ' + '--infile' + ' ' + bundles_path + 'tractography_resampled_filtered.bundles' + ' ' + '--outdir' + ' ' + '../../../../../../../HDD/Ubuntu/Chris/MT/inter-bundle-master/codes/isaias_clustering/Brain_fiber_clustering/data/79subjects/clustered_2/' + sub + '/');
    print('Tiempo: ' + str(time() - t1) + '[s]');
