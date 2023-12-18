import pandas as pd
import numpy as np




class SeriesW(pd.Series):
    """
    A SeriesW object is a pandas.Series that has an attribute composed 
    by weights. In addition to the standard Series constructor arguments,
    SeriesW also accepts the following keyword arguments:

    Parameters
    ----------
    weights : array or Series or list (optional)
        Weights associated to each observation of the DataFrame
        the weights should have a shape with the same number of values as the
        number of rows in the data.
    
    """   
    def __init__(self, data=None, index=None,weights = None, **kwargs):
        if weights is None:
            weights = np.ones(self.data.shape[0])
        else:
            weights = np.asarray(weights).astype(float)
        object.__setattr__(self,"weights", weights)
        name = kwargs.pop("name", None)
        super().__init__(data, index=index, name=name, **kwargs)
        
        
    @property
    def _constructor(self):
        def _seriesw_constructor(*args, **kwargs):
            """
            A specialized SeriesW constructor
            """
            srs = SeriesW(*args,weights=self.weights, **kwargs)
            return srs
        return _seriesw_constructor
    
    @property
    def _constructor_expanddim(self):
        def _dataframew_constructor_expand(*args, **kwargs):
            """
            A specialized DataFrameW constructor
            """
            srs = DataFrameW(*args,weights=self.weights, **kwargs)
            return srs
        return _dataframew_constructor_expand
    
    def mean(self):
        return np.average(super(),weights=self.weights)
    
    def sum(self):
        return np.sum(super().values*self.weights)
    
    def nobs(self):
        """
        A nobs method to implement sum of weighted on a DataFrameW
        """
        return self.weights.sum(0)
    
    def sumsquares(self):
        """weighted sum of squares of demeaned data"""
        return np.dot(((super().values-self.mean()) ** 2).T, self.weights)

    def var(self):
        """variance with default degrees of freedom correction
        """
        return self.sumsquares() / (self.nobs())

    def std(self):
        """standard deviation with default degrees of freedom correction
        """
        return np.sqrt(self.var())
        
    
class DataFrameW(pd.DataFrame):
    """
    A DataFrameW object is a pandas.DataFrame that has an attribute composed 
    by weights. In addition to the standard DataFrame constructor arguments,
    DataFrameW also accepts the following keyword arguments:

    Parameters
    ----------
    weights : array or Series or list (optional)
        Weights associated to each observation of the DataFrame
        the weights should have a shape with the same number of values as the
        number of rows in the data.
    """        
    def __init__(self, data=None, *args, weights = None, **kwargs):
        if weights is None:
            weights = np.ones(self.data.shape[0])
        else:
            weights = np.asarray(weights).astype(float)
        object.__setattr__(self,"weights", weights)
        super().__init__(data, *args, **kwargs)
        
        
    @property
    def _constructor(self):
        def _dataframew_constructor(*args, **kwargs):
            """
            A specialized DataFrameW constructor
            """
            srs = DataFrameW(*args,weights=self.weights, **kwargs)
            return srs
        return _dataframew_constructor

    @property
    def _constructor_sliced(self):
        def _dataframew_constructor_sliced(*args, **kwargs):
            """
            A specialized SeriesW constructor from DataFrameW
            """
            print(self.weights)
            srs = SeriesW(*args,weights=self.weights, **kwargs)
            return srs
        return _dataframew_constructor_sliced
    
    def mean(self):
        """ 
        A mean method to implement weighted mean on a DataFrameW
        """
        return pd.Series(np.average(super(),weights=self.weights,axis=0),index=self.columns)
    
    def sum(self):
        """
        A sum method to implement a weighted sum on a DataFrameW
        """
        return pd.Series(np.dot(super().values.T,self.weights),index=self.columns)
    
    def nobs(self):
        """
        A nobs method to implement sum of weighted on a DataFrameW
        """
        return self.weights.sum(0)

    def sumsquares(self):
        """weighted sum of squares of demeaned data"""
        return pd.Series(np.dot(((super().values-self.mean()) ** 2).T, self.weights), 
                         index=self.columns)

    def var(self):
        """variance with default degrees of freedom correction
        """
        return self.sumsquares() / (self.nobs())

    def std(self):
        """standard deviation with default degrees of freedom correction
        """
        return np.sqrt(self.var())    

    
