from pandas.io.data import DataReader
from datetime import datetime

stl = DataReader('REC.OL',  'yahoo', datetime(2012, 1, 1), datetime(2016, 11, 1))
print(stl['Adj Close'])
print type(stl)

OSEBX = [
    'ASC','AFG','AKER','AKERBP','ATEA','AVANCE','AXA','BAKKA','BIOTEC','BWLPG','DNB','DNO','EKO','ENTRA','EPR','FRO','GIG','GJF','GOGL','HEX','IDEX','KOA','KOG','MHG','MULTI','NEXT','NANO','NOD','NHY','NAS','NPRO','OLT','ORK','PGS','PHO','QFR','REC','SALM','SAS NOK','SSO','SCHA','SCHB','SDRL','STL','SNI','STB','SUBC','TEL','TGS','THIN','TOM','TRE','VEI','WEIFA','WWASA','WWI','WWIB','XXL','YAR']

osebxList = DataReader(OSEBX,  'yahoo', datetime(2016, 1, 1), datetime(2016, 11, 1))
print(osebxList['Adj Close'])

