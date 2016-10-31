
import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib.pyplot as plt
from matplotlib import style
import re
style.use("dark_background")
path = "C:/Users/acer/Desktop"
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE_Ratio','Stock_P_Change','S&P_500','S&P500_P_Change','Difference','Status'])
    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    ticker_list = []
   # print(sp500_df)
    #print (stock_list)
    for each_dir in stock_list[1:25]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)
        starting_stock_value = False
        starting_sp500_value = False
#        print(each_file)
#        time.sleep(15)
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file,'%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp,unix_time)
                full_file_path = each_dir+'/'+file
                source = open(full_file_path,'r').read()
                #print (source)
                try:
                    try:
                        value = float(source.split (gather+':</td><td class="yfnc_tabledata1">')[1].split('</td')[0])
                    except Exception as e:
                        value = float(source.split (gather+':</td>\n<td class="yfnc_tabledata1">')[1].split('</td')[0])

                        #print (str(e),ticker,file)
                    try:
                        
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%d-%m-%Y')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time=259200).strftime('%d-%m-%Y')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        #print(str(e), ticker, file)
                        try:
                            stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price = float(stock_price.group(1))
                            #print (stock_price)
                        except Exception as e:
                            stock_price = source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0]
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price = float(stock_price.group(1))
                            
                            
                            print ("Latest Stock Price:",stock_price)

                        
                    #print ("Stock_Price:",stock_price,"Ticker:",ticker)
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value
                    
                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100
                    

                    difference = stock_p_change - sp500_p_change
                    if difference > 0:
                        status = "Outperform"
                    else:
                        status = "Underperfrom"
                        

                    df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE_Ratio':value,'Price':stock_price,'Stock_P_Change':stock_p_change,'S&P_500':sp500_value,'S&P500_P_Change':sp500_p_change,'Difference':difference,'Status':status}, ignore_index = True )
                except:
                    pass
        for each_ticker in ticker_list:
            try:
                plot_df = df[(df["Ticker"] == each_ticker)]
                plot_df = plot_df.set_index(['Date'])
                if plot_df['Status'][-1] == "Underperfrom":
                    color = "r"
                else:
                    color = "g"
                plot_df['Difference'].plot(label=each_ticker,color=color)
                
                plt.legend()
            except:
                pass
        plt.show()        
        save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
        print(save)
        df.to_csv(save)
                
            
                
                
Key_Stats()