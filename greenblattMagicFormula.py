from exceptions import ValueError
import json
import requests
import pandas as pd

requests.packages.urllib3.disable_warnings()

OSEBX = ['AFG.OL', 'AKER.OL', 'AKERBP.OL', 'AKSO.OL', 'ASETEK.OL', 'ATEA.OL', 'AXA.OL','B2H.OL', 'BAKKA.OL', 'DNB.OL', 
         'DNO.OL', 'EKO.OL', 'ENTRA.OL', 'EPR.OL', 'FRO.OL', 'GIG.OL', 'GJF.OL', 'GOGL.OL', 'GSF.OL', 'HNB.OL',
         'HEX.OL', 'IDEX.OL', 'KIT.OL', 'KOA.OL', 'KOG.OL', 'LSG.OL', 'LINK.OL', 'MHG.OL', 'NEXT.OL', 'NANO.OL',
         'NOD.OL', 'NHY.OL', 'NAS.OL', 'NPRO.OL', 'OLT.OL', 'OPERA.OL', 'ORK.OL', 'PGS.OL', 'REC.OL', 'SALM.OL',
         'SSO.OL', 'SCHA.OL', 'SCHB.OL', 'SDRL.OL', 'SRBANK.OL', 'STL.OL', 'SNI.OL', 'STB.OL', 'SUBC.OL', 'TEL.OL',
         'TGS.OL', 'THIN.OL', 'TOM.OL', 'TRE.OL', 'VEI.OL', 'WWL.OL', 'WEIFA.OL', 'WWI.OL', 'WWIB.OL', 'XXL.OL', 'YAR.OL']

magic_lst = []
maxPE = 1000000
for i, ticker in enumerate(OSEBX):

    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)
    json_loaded_summary =  json.loads(summary_json_response.text)

    eps = 0.0001
    print(ticker)
    if json_loaded_summary["quoteSummary"]["result"]:
        if "defaultKeyStatistics" in json_loaded_summary["quoteSummary"]["result"][0]:
            if json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]:
                if "raw" in json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]:
                    if json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']:
                        eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
    
        curr_price = 999999
    
        if json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']:
            curr_price = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']
        else:
            print(json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["currentPrice"])
    
        PE_ratio = curr_price / eps
        if PE_ratio < 0 : 
            PE_ratio = maxPE + (PE_ratio * (-1))
        elif PE_ratio < 5 : 
            PE_ratio = maxPE + PE_ratio
        normal_PE = 1 / PE_ratio
    
        ROIC = -999999
        if json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["returnOnEquity"]:
            ROIC = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["returnOnEquity"]['raw']
            
        if ROIC < 0.25:
            ROIC = 0.01
        normalROIC = 1 / ROIC
        
        sum_normal = normal_PE + ROIC
        print ( ROIC ) 
        #magic_lst.append([ticker, eps, curr_price, PE_ratio, ROIC, normal_PE, sum_normal, i])
        magic_lst.append([ticker, ROIC, normal_PE, sum_normal])
    else :
        print('No data')

#magic_formula = pd.DataFrame(magic_lst, columns=['OSEBX', 'eps', 'curr_price', 'PE', 'ReturnOnCapital', 'normalPE', 'sum_normal', 'magicFormula'])
magic_formula = pd.DataFrame(magic_lst, columns=['OSEBX', 'ReturnOnCapital', 'normalPE', 'magicFormula'])

print(magic_formula.sort_values(['magicFormula'], ascending=[False]).to_string(index=False))

                        


