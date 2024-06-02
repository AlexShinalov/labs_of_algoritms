from Helpers.Images import Images
from Algorithm.algo2DCCA.algo2DCCA_classic import Algo2DCCA as Algo2DCCA
from Algorithm.algo2DPLS.algo2DPLS_classic import Algo2DPLS as Algo2DPLS
from Helpers.Correlation import Correlatin
import time
import matplotlib.pyplot as plt
import json
import numpy as np

if __name__ == "__main__":
    distantion = Correlatin.distantion
    isMax = False
    D = 200
    
    links_x, links_y = Images.get_links(num_test=1)
    algo = Algo2DCCA(distantion=distantion, isMax=isMax, d=D)
    X = Images.get_pictures(links_x)
    Y = Images.get_pictures(links_y)
    algo.fit(X, Y, withRRPP=True)
    print(f"2DCCA:{np.round(Correlatin.cov_set(algo.U, algo.V), 5)}")
    
    links_x, links_y = Images.get_links(num_test=1)
    algo = Algo2DPLS(distantion=distantion, isMax=isMax, d=D)
    X = Images.get_pictures(links_x)
    Y = Images.get_pictures(links_y)
    
    algo.fit(X, Y, withRRPP=True)
    print(f"2DPLS:{np.round(Correlatin.cov_set(algo.U, algo.V), 5)}")
    
    
    
    
                
                
                
        