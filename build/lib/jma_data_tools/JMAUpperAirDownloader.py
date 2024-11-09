import time, sys, glob
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os


class JMAUpperAirDownloader:
    def __init__(self, amedas_file='Amedas_list.csv', output_path='upperair_download'):
        self.amedas_file = amedas_file
        self.output_path = output_path
        self.url = {}
        self.data_at_defined_press = None
        self.wind_data = None
        self.temphum_data = None
        self.output_files = {}
        

    def get_info(self, h, att):
        if h.has_attr(att):
            nu = int(h.get(att))
        else:
            nu = 1
        return nu
    

    def conv_text_sonde(self, text):
        change = {'日':'Day', 
                  '気圧(hPa)':'Pres(hPa)',
                  'ジオポテンシャル':'GeoPot',
                  '高度(m)':'Height(m)',
                  '気温(℃)':'Temp(C)',
                  '相対湿度(%)':'RH(%)',
                  '風速(m/s)':'WindSpd(m/s)',
                  '風向(°)':'WindDir(deg)',
                  '識別符':'Mark'
                  }
        for k, v in change.items(): 
            text = text.replace(k,v)
        return text

    def rep_text(self, text):
        return text.replace('///', '').replace('特異点', 'SingularPoint')
    
    
    def download_sounding_data(self, point, date):
        """
        Downloads sounding data for a specified station (point) and date from JMA.
        
        Parameters:
            point (str): The station ID for the location.
            date (pd.Timestamp): The date and time for the sounding data.
        
        Returns:
            dict: A dictionary containing DataFrames of interpolated data, temperature and humidity, and wind data.
        """
        
        opath = self.output_path
        print(date)
        year, mon, day, hour = str(date.year), '%.2d' % date.month, '%.2d' % date.day,'%.2d' % date.hour
        hour = str(date.hour)
        
        
        try:
            
            hp1 = 'https://www.data.jma.go.jp/obd/stats/etrn/upper/view/'
            url = hp1 + 'hourly_usp.php?year='+year+'&month='+mon+'&day='+day+'&hour='+hour+'&atm=&point='+point+'&view='
            print('***' , '指定気圧面の観測データ', '****')
            print('trying to access:  ', url)
            self.url['data_at_defined_press'] = url
            
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table1 = soup.find('table', id='tablefix1') # Get table
            table2 = soup.find('table', id='tablefix2') # Get table
                      
            
            url = hp1 + 'daily_uth.php?year='+year+'&month='+mon+'&day='+day+'&hour='+hour+'&atm=&point='+point+'&view='
            
            print('***' , '気温・湿度の観測データ', '****')
            print('trying to access:  ', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table3 = soup.find('table', id='tablefix1') # Get table
            self.url['temphum'] = url
            
            url = hp1 + 'daily_uwd.php?year='+year+'&month='+mon+'&day='+day+'&hour='+hour+'&atm=&point='+point+'&view='
            print('***' , '風の観測データ', '****')
            print('trying to access:  ', url)        
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table4 = soup.find('table', id='tablefix1') # Get table
            self.url['wind'] = url
        
            dd = []
            for table in [table1, table2,table3,table4]:
                rows = table.findAll('tr')  # split to rows
                #-----Get header information---------
                header = [ [{ 'scol':self.get_info(c,'colspan'), 'srow':self.get_info(c,'rowspan'), 'text':self.conv_text_sonde(c.text) } for c in tr] for tr in rows]
                    
                header = [x for x in header if x ]
                
                # number of header columns
                nu_col = max([ sum([c['scol'] for c in header[irow]]) for irow in range(2)])
                
                hd = ['']*len(header)*nu_col # there are two rows and 2 cols
                # split row and column of header
                for irow in range(len(header)):
                    for h1 in header[irow]:
                        idb = hd.index('')
                        for ir in range(h1['srow']):
                            for ic in range(h1['scol']): 
                                #print h1['text'], idb+ic+ir*nu_col 
                                hd[idb + ic + ir*nu_col] = h1['text']
                
                # merge rows of header
                hder = [] 
                nu_headrow = header[0][0]['srow']
                for i in range(nu_col): 
                    #if hd[i] != hd[i+nu_col]: hder.append(hd[i + nu_col]+hd[i])
                    #else: 
                    hder.append( '_'.join(list(np.unique(np.array([ hd[i+ii*nu_col] for ii in range( nu_headrow ) ])))))
                                
                
                # Get data            
                data = [ [ self.rep_text(c.text) for c in tr] for tr in rows]
                data = [x for x in data if x ][header[0][0]['srow']:]
                
                do = pd.DataFrame(data, columns = hder)
                dd.append(do)

            path = opath + '/'+point+'/' 
            if not os.path.isdir(path): os.makedirs(path)
            print(path)
            if (table1 != None) and (table2 != None):
            
                dout = pd.concat(dd[:2])
                dout.set_index('Pres(hPa)',inplace=True)
                for c in dout.columns: dout.loc[:,c] = pd.to_numeric(dout.loc[:,c], errors='coerce')
                dip = dout
                ofile1 = path+'Interp_'+year+'-'+mon+'-'+day+'_'+hour+".csv"
                dip.to_csv(ofile1, header=True, index=False, encoding='utf-8')
            
            if (table3 != None):          
                dout = dd[2]
                dout.set_index('Pres(hPa)',inplace=True)
                for c in dout.columns[:-1]: dout.loc[:,c] = pd.to_numeric(dout.loc[:,c], errors='coerce')
                dth = dout
                ofile2 = path+'TempHum_'+year+'-'+mon+'-'+day+'_'+hour+".csv"
                dth.to_csv(ofile2, header=True, index=False, encoding='utf-8')

            if (table4 != None):               
                dout = dd[3]
                dout.set_index('Pres(hPa)',inplace=True)
                for c in dout.columns[:-1]: dout.loc[:,c] = pd.to_numeric(dout.loc[:,c], errors='coerce')
                dwd = dout
                ofile3 = path+'Wind_'+year+'-'+mon+'-'+day+'_'+hour+".csv"
                dwd.to_csv(ofile3, header=True, index=False, encoding='utf-8')
            
            
            self.data_at_defined_press = dip
            self.wind_data = dwd
            self.temphum_data = dth
            self.output_files = { 'file1': ofile1, 'file2': ofile2, 'file3': ofile3 }
        
            return dip
        
        except:
            print(date, '\n **** \n File not exist \n **** \n') 
            return {}
            
            
            
            
#==============================================================================
#==============================================================================
if __name__ == "__main__":
    
    # Initialize the downloader
    downloader = JMAUpperAirDownloader(output_path='upperair_test_download')
    
    from JMADataPlotter import JMADataPlotter
    
    #plotter = PlotJMA()
    #amedas_file = 'Amedas_list.csv'
    #alist = pd.read_csv(amedas_file, index_col=0).set_index('station_id')
    
    #==========GET ALL AMEDAS INFORMATION==========================================
    #https://www.jma.go.jp/jma/en/Activities/upper/upper.html
    kansho = [47401, 47412, 47418, 47582, 47600, 47646,
              47678, 47741, 47778, 47807, 47827, 47909,
              47918, 47945, 47971, 47991, 
              89532] # last one is Showwa Kichi
    
    point =  '47646' # Tsukuba station
    
    #opath = 'data_download/' 

    test_point = '47646'  # Example station code for Tsukuba
    test_date = pd.Timestamp('2022-06-01 09:00')
    
    data = downloader.download_sounding_data(test_point, test_date)
    plotter = JMADataPlotter()
    plotter.plot_sounding(data)
    
    
    
    
    
    
    
    
    
    