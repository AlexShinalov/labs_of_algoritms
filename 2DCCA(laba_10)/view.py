from GUI.GUI import GUI
from Algorithm.algo2DCCA.algo2DCCA_classic import Algo2DCCA
from Algorithm.algo2DPLS.algo2DPLS_classic import Algo2DPLS

if __name__ == "__main__":
    app = GUI("2DCCA", Algo2DPLS)
    app.mainloop()