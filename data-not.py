import pandas as pd
import hvplot.pandas
import holoviews as hv

prices = {'Too Cheap': [100,120,200,200,300,100,100,300,100,350,340,450,100,257,109,109,280,400,250,200],
          'Cheap': [150,200,250,300,340,190,200,350,120,360,360,460,110,388,299,129,350,410,260,240],
          'Expensive': [400,400,450,350,400,200,300,370,180,370,490,490,130,433,399,149,400,420,270,280],
          'Too Expensive': [500,480,500,400,490,300,500,380,200,380,500,500,140,499,422,199,410,430,280,300],
        }

df = pd.DataFrame(prices)