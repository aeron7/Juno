 import requests
from bs4 import BeautifulSoup
Underlying_Stock = ['NIFTY','BANKNIFTY','ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','AUROPHARMA','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BALKRISIND','BANKBARODA','BATAINDIA','BERGEPAINT','BEL','BHARATFORG','BPCL','BHARTIARTL','INFRATEL','BHEL','BIOCON','BOSCHLTD','BRITANNIA','CADILAHC','CANBK','CENTURYTEX','CESC','CHOLAFIN','CIPLA','COALINDIA','COLPAL','CONCOR','CUMMINSIND','DABUR','DIVISLAB','DLF','DRREDDY','EICHERMOT','EQUITAS','ESCORTS','EXIDEIND','FEDERALBNK','GAIL','GLENMARK','GMRINFRA','GODREJCP','GRASIM','HAVELLS','HCLTECH','HDFCBANK','HDFC','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','ICICIBANK','ICICIPRULI','IDEA','IDFCFIRSTB','IBULHSGFIN','IOC','IGL','INDUSINDBK','INFY','INDIGO','ITC','JINDALSTEL','JSWSTEEL','JUBLFOOD','JUSTDIAL','KOTAKBANK','L%26TFH','LT','LICHSGFIN','LUPIN','M%26MFIN','MGL','M%26M','MANAPPURAM','MARICO','MARUTI','MFSL','MINDTREE','MOTHERSUMI','MRF','MUTHOOTFIN','NATIONALUM','NCC','NESTLEIND','NIITTECH','NMDC','NTPC','ONGC','OIL','PAGEIND','PETRONET','PIDILITIND','PEL','PFC','POWERGRID','PNB','PVR','RBLBANK','RELIANCE','RECLTD','SHREECEM','SRTRANSFIN','SIEMENS','SRF','SBIN','SAIL','SUNPHARMA','SUNTV','TATACHEM','TCS','TATAGLOBAL','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','TVSMOTOR','UJJIVAN','ULTRACEMCO','UBL','MCDOWELL-N','UPL','VEDL','VOLTAS','WIPRO','YESBANK','ZEEL']
symbolCode = '0'
header = {
 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
   "X-Requested-With": "XMLHttpRequest"
}
a = 0
while a < len(Underlying_Stock):
    Underlying_Stock[a] = Underlying_Stock[a].replace('&','%26')
    if a < 2:
        my_url_nse = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=' + Underlying_Stock[a] + '&date=27FEB2020'
        if a == 0:
            my_url_yahoo = 'https://in.finance.yahoo.com/quote/^NSEI?p=^NSEI&.tsrc=fin-srch'
        else:
            my_url_yahoo = 'https://in.finance.yahoo.com/quote/^NSEBANK?p=^NSEBANK&.tsrc=fin-srch'
    else :
        my_url_nse = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode='+ symbolCode + '&symbol=' + Underlying_Stock[a] + '&symbol='+ Underlying_Stock[a] + '&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17'
        my_url_yahoo = 'https://in.finance.yahoo.com/quote/' + Underlying_Stock[a] + '.NS?p='+ Underlying_Stock[a] +'.NS&.tsrc=fin-srch'
    page_nse = requests.get(my_url_nse,headers=header)
    soup_nse = BeautifulSoup(page_nse.content,'html.parser')
    locate_yellow = soup_nse.findAll("td",{"class","ylwbg"})
    locate_white  = soup_nse.findAll("td",{"class","nobg"})
    #Scraping Yahoo
    page_yahoo = requests.get(my_url_yahoo)
    soup_yahoo = BeautifulSoup(page_yahoo.content,'html.parser')
    locate_yahoo = soup_yahoo.find('span',{'class',"Trsdu(0.3s)"})
    stock_price  = locate_yahoo.text
    stock_price  = stock_price.replace(',','')
    stock_price  = float(stock_price)
    #print(stock_price)
    Strike_Price = []
    m = 0
    difference = []
    while m < (len(locate_yellow)/10):
        locate_strike = soup_nse.findAll("td",{"class","grybg"})[m]
        Strike_Price.append(locate_strike.text)
        Strike_Price[m] = float(Strike_Price[m])
        difference.append(Strike_Price[m] - stock_price)
        m += 1
    if len(difference) != 0:
        l = 0
        neg_list = []
        while l < len(difference):
            if difference[l] < 0:
                neg_list.append(difference[l])
                l += 1
            else:
                l += 1
        ki = difference.index(max(neg_list)) * 10
        ATM_Strike = Strike_Price[difference.index(max(neg_list))]
        #print("ATM STRIKE:")
        #print(ATM_Strike)
    else :
        pass

#Defining Function for Scraping and Converting Data
    def Repeat(i,j,x,y,z):
        while i < (len(Strike_Price) * 10):
            if i <= (ki+j):
                x.append(y[i].text)
            else :
                x.append(z[i].text)
            i += 10
    def floater(x):
        i = 0
        while i < len(x):
            x[i] = x[i].replace(',','')
            if '-' in x[i] and len(x[i]) == 1:
                x[i] = x[i].replace('-','0')
                x[i] = float(x[i])
            elif '-' in x[i] and len(x[i]) > 1:
                x[i] = x[i].replace('-','')
                x[i] = float(x[i])
                x[i] = x[i] * -1
            else :
                x[i] = float(x[i])
            i += 1
#Scraping and Converting data for PCR/Juno
    call_oi = []
    put_oi  = []
    Repeat(0,0,call_oi,locate_yellow,locate_white)
    Repeat(9,9,put_oi,locate_white,locate_yellow)
    floater(call_oi)
    floater(put_oi)
#Scraping Prices and Converting to Float
    call_bp = []
    put_bp  = []
    call_ap = []
    put_ap  = []
    Repeat(7,7,call_bp,locate_yellow,locate_white)
    Repeat(1,1,put_bp,locate_white,locate_yellow)
    Repeat(8,8,call_ap,locate_yellow,locate_white)
    Repeat(2,2,put_ap,locate_white,locate_yellow)
    floater(call_ap)
    floater(call_bp)
    floater(put_ap)
    floater(put_bp)
#Scraping Quantity
    call_bq = []
    Repeat(6,6,call_bq,locate_yellow,locate_white)
    floater(call_bq)
    call_bq.sort()
    if min(call_bq) == 0:
        lot_size = call_bq[call_bq.count(min(call_bq))]
    elif min(call_bq) > 0:
        lot_size = min(call_bq)
    else:
        pass
#Scanning Juno
    def Juno_Scanner(x):
        if max(x) > 1500000:
            print('\n')
            print("Companies Name:")
            print(Underlying_Stock[a])
            print("Stock Price:")
            print(stock_price)
            print("ATM STRIKE:")
            print(ATM_Strike)
            if x == call_oi:
                print("Trade Found at:")
                print(Strike_Price[x.index(x[x.index(max(x))])],"CE")
                print("Open Interest")
                print(max(x))
                print("Premium:")
                print(call_ap[x.index(x[x.index(max(x))])])
            elif x == put_oi:
                print("Trade Found at:")
                print(Strike_Price[x.index(x[x.index(max(x))])],"PE")
                print("Open Interest")
                print(max(x))
                print("Premium:")
                print(put_ap[x.index(x[x.index(max(x))])])
            else:
                pass
            print("Lot Size:")
            print(lot_size)
            #PCR > 1.1 Bullish
            #PCR < 0.9 Bearish
            print("PCR:")
            print((sum(put_oi)/sum(call_oi)))
            print('\n')
        else:
            pass
    Juno_Scanner(call_oi)
    Juno_Scanner(put_oi)
    a += 1
