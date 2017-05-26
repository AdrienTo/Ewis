import numpy as np
import openturns as ot
from   openturns.viewer import View

#[Nb_PSU, Delta_V*V0],(np.array(Dist_SPDB))[:,0],Catalog_Gauge

class CalcMassFunc(ot.OpenTURNSPythonFunction):

        def __init__(self, x1, x2, x3):
            super(CalcMassFunc,self).__init__(len(x2)*x1[0],1)
            self.x1 = x1             # x1[0]: Total nb of equipment power requests, x1[1]: Constant deltaV*V0
            self.x2 = x2             # Vector of distances b/t EPDC & element of the EWIS architecture
            self.x3 = np.array(x3)   # Catalog of available gauges

        def _exec(self, X):
            # Reshaping the sample of Power request vector
            R = np.array(X).reshape(len(self.x2), self.x1[0])    
            # Summing power request by sub system
            Sum = R.sum(axis=1)
            # Reshaping the distance vector
            D = self.x2.reshape(len(self.x2))
            # Compute the gauge sizing criteria expressed as a lineic resistance 
            # argmax {r \in Catalog s.t. r <= (deltaV*V0/(Distance*SumPower))}
            out = self.x1[1]/(D*Sum)
            # Get the indexes corresponding to adequate gauge            
            indexes = [(self.x3[:,0] * (self.x3[:,0] <= t)).argmax() for t in out]
            # Compute the sum of mass computed by multiplying distances with lineic mass corresponding to chosen gauge
            return [np.sum(np.array(self.x2).ravel() * self.x3[indexes, 1])]
        
class DistanceFunc(ot.OpenTURNSPythonFunction):

    def __init__(self,X0):
        super(DistanceFunc, self).__init__(len(X0),1)
        self.X0 = ot.NumericalPoint(X0)

    def _exec(self,x):
        d = ot.NumericalPoint(x) - self.X0
        return [d.norm1()]

