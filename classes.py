import matplotlib.pyplot as plt
import json
from pyjstat import pyjstat
import pandas as pd


class Drzava:
    name : str
    years : list
    gdp : list[int, float]
    inflation : list[int, float]

    def __init__(self, name, years, gdp, inflation):
        if not isinstance(name, str) or any({not isinstance(x, list) for x in [years, gdp, inflation]}):
            raise ValueError
        elif len({len(x) for x in [years, gdp, inflation]}) > 1:
            raise ValueError(f'Lenghts of lists are not equal! : {[len(x) for x in [years, gdp, inflation]]}')
        #y to y gdp and inflation
        self.name = name
        self.years = years
        self.gdp = gdp
        self.inflation = list(map(lambda x: x/100, inflation))
    
    def __repr__(self):
        return f'Država: {self.name}; Leta: {self.years[0]}-{self.years[-1]}|'

    #growth (total, relative + inflation adjusted)
    @staticmethod
    def total_growth(l):
        """Returns y to y total growth for a list of values"""
        if not isinstance(l, list):
            raise ValueError
        g = list()
        for i in range(1, len(l)):
            g.append(l[i]-l[i-1])
        return g
    
    @staticmethod
    def relative_growth(l):
        """Returns y to y relative growth for a list of values"""
        if not isinstance(l, list):
            raise ValueError
        g = list()
        for i in range(1, len(l)):
            g.append((l[i]-l[i-1])/l[i-1])
        return g
    
    @staticmethod
    def depreciated_total_growth(l, d):
        """returns y to y growth of values in l, using y to y 
        depreciation weights from d"""
        if not isinstance(l, list) or not isinstance(d, list):
            raise ValueError
        g = list()
        for i in range(1, len(l)):
            adj_gr = (l[i] - l[i-1]*(1 + d[i])) #letosnja - lanska krat 1+inflacija
            g.append(adj_gr)
        return g
    
    @staticmethod
    def depreciated_relative_growth(l, d):
        """returns y to y relative growth of values in l, using y to y 
        depreciation weights from d"""
        if not isinstance(l, list) or not isinstance(d, list):
            raise ValueError
        g = list()
        for i in range(1, len(l)):
            adj_gr = (l[i] - l[i-1]*(1 + d[i])) 
            g.append(adj_gr/l[i-1])
        return g
    
    @staticmethod
    def depreciated_relative_real_growth_fischer(l, d):
        """Returns exact y to y relative real growth (inflation adjusted) using the Fisher equation"""
        if not isinstance(l, list) or not isinstance(d, list):
            raise ValueError
        g = list()
        for i in range(1, len(l)):
            inflation_decimal = d[i] / 100
            # Exact formula for real relative growth
            real_growth = (l[i] / (l[i-1] * (1 + inflation_decimal))) - 1
            g.append(real_growth)
        return g

    #graphs
    @staticmethod
    def graph(x_ticks, y_data, x_label='x', y_label='y', title='graf', ax=None):
        """Generalized graph plot; highlights top 5 highest y values"""
        x_ticks: list
        y_data: list[int, float]
        x_label: str
        y_label: str
        title: str

        top_5 = sorted(list(enumerate(y_data)), key=lambda x: x[1])[-5:]
        top_5_i = [x[0] for x in top_5]
        top_5_y = [x[1] for x in top_5]
        x_data = list(range(len(y_data)))
        
        # If no axis is provided, create a standalone window
        is_standalone = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
            is_standalone = True

        ax.plot(x_data, y_data, color="#1fb487", linewidth=1.5)
        ax.scatter(top_5_i, top_5_y, color='red', zorder=100, s=20) 
        
        # FIXED: Exponent notation (** instead of ^) and checked the absolute data span 
        data_span = max(y_data) - min(y_data)
        if data_span > 10**4 or (0 < data_span < 10**-2):
            pass
            # ax.set_yscale('log')
            
        ax.set_xticks(x_data)
        ax.set_xticklabels(x_ticks, fontsize=8, rotation=45, ha='right')
        ax.set_title(title, fontsize = 10)
        ax.grid(True, which="both", linestyle="-", alpha=0.5)
        ax.set_xlabel(x_label, fontsize=10, fontweight='bold', labelpad=15)
        ax.set_ylabel(y_label, fontsize=10, fontweight='bold', labelpad=10)


    @staticmethod
    def graph_single(x_ticks, y_data, x_label = 'x', y_label = 'y', title = 'graf'):
        """Generalized graph plot; highlights top 5 highest y values"""
        x_ticks : list
        y_data : list[int, float]
        x_label : str
        y_label : str
        title : str

        top_5 = sorted(list(enumerate(y_data)), key = lambda x: x[1])[-5:]
        top_5_i = [x[0] for x in top_5]
        top_5_y = [x[1] for x in top_5]
        x_data = list(range(len(y_data)))
        #top_5_x = [x_ticks[i] for i in top_5_i]
        
        fig = plt.figure(figsize = (10, 6))
        plt.plot(list(range(len(y_data))), y_data, color = "#1fb487", linewidth = 1.5)
        plt.scatter(top_5_i, top_5_y, color = 'red', zorder = 100, s=20) #pikice na ta vecjih 5-ih
        if (min(y_data) - top_5_y[-1]) > 10^4 or (min(y_data) - top_5_y[-1]) < 10^(-1):
            plt.yscale('log')
        #plt.xticks(top_5_i, top_5_x, fontsize = 8, rotation = 45, ha = 'right')
        plt.xticks(x_data, x_ticks, fontsize = 8, rotation = 45, ha = 'right')
        plt.title(title, fontsize = 10)
        plt.grid(True, which="both", linestyle = "-", alpha=0.5)
        plt.xlabel(x_label, fontsize = 10, fontweight = 'bold' , labelpad = 15)
        plt.ylabel(y_label, fontsize = 10, fontweight = 'bold', labelpad = 10)

        plt.tight_layout()
        plt.show(block = False)
        #plt.close()
        return


    #get methods
    def get_gdp_growth(self):
        """list of total year to year gdp growth"""
        return Drzava.total_growth(self.gdp)
    
    def get_relative_gdp_growth(self):
        """List of year to year relative gdp growth"""
        return Drzava.relative_growth(self.gdp)
    
    def get_adjusted_gdp(self):
        """List of inflation adjusted total year to year growth"""
        return Drzava.depreciated_total_growth(self.gdp, self.inflation)
    
    def get_adjusted_relative_gdp_growth(self):
        """List of inflation adjusted relative year to year growth"""
        return Drzava.depreciated_relative_growth(self.gdp, self.inflation)
    
    def get_adjusted_relative_real_gdp_growth(self):
        return Drzava.depreciated_relative_real_growth_fischer(self.gdp, self.inflation)
    
    #graph
    # Graphs
    def total_gdp_graph(self, ax=None):
        Drzava.graph(self.years, self.gdp, 'Year', 'GDP', f'{self.name} total GDP from {self.years[0]} to {self.years[-1]}', ax=ax)

    def total_adjusted_gdp_graph(self, ax=None):  # Fixed spelling from _raph to _graph
        Drzava.graph(self.years[1:], self.get_adjusted_gdp(), 'Year', 'GDP', f'{self.name} infl. adjusted total GDP growth from {self.years[0]} to {self.years[-1]}', ax=ax)

    def inflation_graph(self, ax=None):
        Drzava.graph(self.years, self.inflation, 'Year', 'Inflation(HICP)', f'{self.name} total inflation from {self.years[0]} to {self.years[-1]}', ax=ax)
    
    def relative_growth_gdp_graph(self, ax=None):
        Drzava.graph(self.years[1:], self.get_relative_gdp_growth(), 'Year', 'Relative GDP growth', f'{self.name} relative GDP growth from {self.years[0]} to {self.years[-1]}', ax=ax)
    
    def adjusted_relative_gdp_growth_graph(self, ax=None):
        Drzava.graph(self.years[1:], self.get_adjusted_relative_gdp_growth(), 'Year', 'Inflation adjusted relative GDP growth', f'{self.name} inflation adjusted relative GDP growth from {self.years[0]} to {self.years[-1]}', ax=ax)
    
    def adjusted_relative_real_gdp_growth_graph(self, ax=None):
        Drzava.graph(self.years[1:], self.get_adjusted_relative_real_gdp_growth(), 'Year', 'Inflation adjusted relative real GDP growth', f'{self.name} inflation adjusted relative real GDP growth from {self.years[0]} to {self.years[-1]}', ax=ax)


    #data
    @staticmethod
    def acquire_data(json_path):
        """Meant for local json file -> convert it into a pandas dataset"""
        with open(json_path, 'r') as file:
            dataset = pyjstat.Dataset.read(file.read())
        # Convert it directly to a Pandas DataFrame
        df = dataset.write('dataframe')
        return df

    @staticmethod    
    def split_gdp_data_by_country(data):
        """Splits a pandas dataframe of expected eu gdp values json format 
        into a dict shaped like {country : {Time : [], value : []}}"""
        # Filter the dataset for the specific unit of measure
        filtered_data = data[data['Unit of measure'] == 'Current prices, million euro']

        dict_country_data = {}

        # Group the filtered data by country
        for country, group in filtered_data.groupby('Geopolitical entity (reporting)'):
            dict_country_data[country] = {
                'Time': group['Time'].tolist(),
                'value': group['value'].tolist()
            }

        return dict_country_data
    
    @staticmethod
    def split_inflation_data_by_country(data):
        """A faster alternative using Pandas groupby."""
        # Filter the dataset for the correct unit of measure
        filtered_data = data[data['Unit of measure'] == 'Annual average rate of change']

        dict_country_data = {}

        # Group by the country and convert 'Time' and 'value' columns directly to lists
        for country, group in filtered_data.groupby('Geopolitical entity (reporting)'):
            dict_country_data[country] = {
                'Time': group['Time'].tolist(),
                'value': group['value'].tolist()
            }
        
        return dict_country_data
    
    @staticmethod
    def split_chain_linked_volumes_data_by_country(data):
        """Splits a pandas dataframe of expected eu chain linked volumes values in million euros json format 
        into a dict shaped like {country : {Time : [], value : []}}"""
        # Filter the dataset for the specific unit of measure
        filtered_data = data[data['Unit of measure'] == 'Chain linked volumes (2010), million euro']

        dict_country_data = {}

        # Group the filtered data by country
        for country, group in filtered_data.groupby('Geopolitical entity (reporting)'):
            dict_country_data[country] = {
                'Time': group['Time'].tolist(),
                'value': group['value'].tolist()
            }

        return dict_country_data
    
    @staticmethod
    def find_country(name, list_of_countries):
        """Finds the country with a given name in a list of countries, returns None if country is not in the list"""
        name : str
        list_of_countries : list

        chosen_country = None 
        for country in list_of_countries:
            if not isinstance(country, Drzava):
                raise ValueError('List contains a non Drzava object')
            elif country.name == name:
                chosen_country = country
                break
        return chosen_country

