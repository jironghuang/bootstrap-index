#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:57:07 2020

@author: jirong
"""
import pandas as pd
import numpy as np
import random
import io
import requests

class bootstrapindex(object):
    		  		 			     			  	   		   	  			  	
    def __init__(self, data, window, num_samples_per_period, min_sample_size, prop_block_bootstrap, 
                 days_block, starting_index=None):
        
        """ Constructor for bootstrap_index class
        
        Attributes:
            data (pandas data frame or series) Data-frame
            window (string) expanding or sliding
            num_samples_per_period (int) Number of blocks of samples to be extracted 
            min_sample_size (int) To define minimum data points to be extracted for each sample 
            prop_block_bootstrap (float) number of trials
            days_block (int) Used as parameter in expanding or sliding window block.
            starting_index (int) Starting index to create window of training and testing indexes
            expanding_windows_w_bootstrap_info (dict) Dictionary of indexes used for boostrapping
                
        """                             
        if not(type(data) is pd.core.frame.DataFrame or type(data) is pd.Series):
            raise ValueError('data input must be of type pd.core.frame.DataFrame or pd.Series')          
        self.data = data
        
        if not(type(window) is str):
            raise ValueError('window input must be of type int')           
        self.window = window #sliding or expanding
        
        if not(type(num_samples_per_period) is int):
            raise ValueError('num_samples_per_period input must be of type int')          
        self.num_samples_per_period = num_samples_per_period      
        
        if not(type(min_sample_size) is int):
            raise ValueError('min_sample_size input must be of type int')    
            
        #Minimum sample size must be smaller than number of rows in data
        if min_sample_size > data.shape[0]:
            raise ValueError('min_sample_size must be smaller than number of rows in data') 
              
        self.min_sample_size = min_sample_size

        if not(type(prop_block_bootstrap) is float):
            raise ValueError('prop_block_bootstrap input must be of type float')                          
        self.prop_block_bootstrap = prop_block_bootstrap
        
        if not(type(days_block) is int):
            raise ValueError('days_block input must be of type int')

        #days_block must be smaller than number of rows in data
        if days_block > data.shape[0]:
            raise ValueError('days_block must be smaller than number of rows in data')             
                          
        self.days_block = days_block
        
        if not(type(starting_index) is int):
            raise ValueError('starting_index input must be of type int')                          
        self.starting_index = starting_index
        
        if starting_index is None:
            self.starting_index = 0
        else:
            self.starting_index = starting_index

        self.expanding_windows_w_bootstrap_info = None  #Dictionary of indexes
        
        pass
         
    def create_window_index(self, days_block = None):
        
        """ Method for creating window index  
        
		Args:        
            days_block: testing block size which is also used to create multiple of training block size
        
        Returns: 
            list: list of training and testing indexes
                            
        Examples
        --------
        url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
        s=requests.get(url).content
        data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
        data.set_index('Date', inplace=True)           
        bootstrap = bootstrapindex(data, window='sliding', 
                                    num_samples_per_period=10, 
                                    min_sample_size=300, 
                                    prop_block_bootstrap=0.25, 
                                    days_block=252, 
                                    starting_index = 5
                                    )        
        bootstrap = bootstrap_index(data)
        bootstrap.create_window_index()
        Out[93]: 
        [[[0, 251], [252, 503]],
         [[0, 503], [504, 755]],     
        ...
        """      

        if not(days_block is None):
            if not(type(days_block) is int):
                raise ValueError('days_block input must be of type int') 
            
        if days_block is None:
            days_block = self.days_block

        #Starting index assigned to s
        s = self.starting_index
        
        num_blocks = int((self.data.shape[0] - s) / days_block)        
        
        if self.window == 'expanding':
            windows_index = [[[s,(s + days_block * (n+1) - 1)], [s + days_block * (n+1), s + days_block * (n+1) + days_block - 1]] \
                             if n<(num_blocks-2) else\
                                 [[s,(s + days_block * (n+1) - 1)], [s + days_block * (n+1), (s + self.data.shape[0]-1)]] \
                                     for n in range(num_blocks-1)]               
                                
        if self.window == 'sliding':
            windows_index = [[[(s + days_block * n),(s + days_block * (n+1) - 1)], [s + days_block * (n+1), s + days_block * (n+1) + days_block - 1]] \
                             if n<(num_blocks-2) else\
                                 [[(s + days_block * n),(s + days_block * (n+1) - 1)], [s + days_block * (n+1), (s + self.data.shape[0]-1)]] \
                                     for n in range(num_blocks-1)]                
        
        return windows_index
    
    def extract_block_bootstrap_periods(self, sample_size, start_sample_index = 0, end_sample_index = None):

        """ Function for selecting period
        
        Args:       
            start_sample_index: Start of sample index        
            end_sample_index: End of sample index       
                
        Returns:            
            dictionary of start and end indexes
            
        Examples
        --------            
        url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
        s=requests.get(url).content
        data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
        data.set_index('Date', inplace=True)       
        bootstrap = bootstrapindex(data, window='sliding', 
                                    num_samples_per_period=10, 
                                    min_sample_size=300, 
                                    prop_block_bootstrap=0.25, 
                                    days_block=252, 
                                    starting_index = 5
                                    )        
        bootstrap.extract_block_bootstrap_periods(sample_size = 100, start_sample_index = 50, end_sample_index = 500)
        Out[143]: 
        {'start_index': array([247, 118,  78, 171, 170, 368, 343, 215, 166, 287]),
         'end_index': array([372, 243, 203, 296, 295, 493, 468, 340, 291, 412])}            
        """    
           
        if not(type(sample_size) is int):
            raise ValueError('sample_size input must be of type int')           

        if not(type(start_sample_index) is int):
            raise ValueError('start_sample_index input must be of type int')           

        if not(type(end_sample_index) is int):
            raise ValueError('end_sample_index input must be of type int')           
        
        #Select proportion size if larger
        sample_size_prop = round(end_sample_index * self.prop_block_bootstrap)
        
        #if sample_size_prop > self.min_sample_size:
        if sample_size_prop > sample_size:            
            sample_size = sample_size_prop
                                
        if end_sample_index is None:
            end_sample_index = self.data.shape[0] - sample_size - 1
        else:
            end_sample_index = end_sample_index - sample_size - 1              
    
        def rand_int(seed_num):   
            random.seed(seed_num)        
            return random.randrange(start_sample_index, end_sample_index)
        
        start_index = np.array([rand_int(n) for n in range(self.num_samples_per_period)])
        end_index = start_index + sample_size        
        
        return {'start_index': start_index, 'end_index': end_index}      
    
    
    def create_dictionary_window_n_bootstrap_index(self):
                           
        """ Method for creating dictionary of window and block bootstrap indexes. 
                
        Returns: 
            dict: Dictionary of in_sample index, out_sample index, bootstrap_index extracted from in_sample_index range
                            
        Examples
        --------
            url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
            s=requests.get(url).content
            data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
            data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
            data.set_index('Date', inplace=True)    
            
            bootstrap = bootstrapindex(data, window='sliding', 
                                        num_samples_per_period=10, 
                                        min_sample_size=300, 
                                        prop_block_bootstrap=0.25, 
                                        days_block=252, 
                                        starting_index = 5
                                        )
            bootstrap.create_dictionary_window_n_bootstrap_index()
            bootstrap.expanding_windows_w_bootstrap_info
            Out[132]: 
            {1: {'in_sample_index': [5, 256],
              'out_sample_index': [257, 508],
              'bootstrap_index': {'start_index': array([3, 1, 0, 1, 1, 4, 4, 2, 1, 3]),
               'end_index': array([252, 250, 249, 250, 250, 253, 253, 251, 250, 252])}},
             2: {'in_sample_index': [257, 508],
              'out_sample_index': [509, 760],
              'bootstrap_index': {'start_index': array([ 98,  34,  14,  60,  60, 159, 203,  82,  58, 118]),    
        ...
        """           
        
        window_index = self.create_window_index()
        
        self.expanding_windows_w_bootstrap_info = {}
        length = 0
        
        for n in window_index:
            length += 1
            #print(length)
            self.expanding_windows_w_bootstrap_info[length] = {}
            self.expanding_windows_w_bootstrap_info[length]['in_sample_index'] = n[0]    
            self.expanding_windows_w_bootstrap_info[length]['out_sample_index'] = n[1]       
            
            if (self.days_block * length) < self.min_sample_size:                         
                min_sample_size_adj = self.days_block - 3  #3 is included to make minimum sample smaller than block of data considered
            else:
                min_sample_size_adj = self.min_sample_size  
            
            bootstrap_index = self.extract_block_bootstrap_periods(sample_size=min_sample_size_adj, start_sample_index = 0, end_sample_index = n[0][1])   
            
            
            self.expanding_windows_w_bootstrap_info[length]['bootstrap_index'] = bootstrap_index        
        pass    

#Code example
if __name__ == "__main__": 
    
    url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
    s=requests.get(url).content
    data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data.set_index('Date', inplace=True)    
    
    bootstrap = bootstrapindex(data, window='sliding', 
                                num_samples_per_period=10, 
                                min_sample_size=300, 
                                prop_block_bootstrap=0.25, 
                                days_block=252, 
                                starting_index = 5
                                )
    bootstrap.create_dictionary_window_n_bootstrap_index()
    bootstrap.expanding_windows_w_bootstrap_info    
    bootstrap.extract_block_bootstrap_periods(sample_size = 100, start_sample_index = 50, end_sample_index = 500)

    