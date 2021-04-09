from pykeops.common.ivf import GenericIVF
import numpy as np


class IVF(GenericIVF):
    def __init__(self, k=5, metric="euclidean", normalise=False):
        from pykeops.numpy import LazyTensor

        self.__get_tools()
        super().__init__(k=k, metric=metric, normalise=normalise, LazyTensor=LazyTensor)

    def __get_tools(self):
        from pykeops.numpy.utils import numpytools

        self.tools = numpytools

    def fit(self, x, clusters=50, a=5, Niter=15, backend="CPU", approx=False):
        if approx:
            raise ValueError("Approximation not supported for numpy")
        if type(x) != np.ndarray:
            raise ValueError("Input dataset must be np array")
        return self._fit(x, clusters=clusters, a=a, Niter=Niter, backend=backend)

    def kneighbors(self, y):
        if type(y) != np.ndarray:
            raise ValueError("Query dataset must be a np array")
        return self._kneighbors(y)
