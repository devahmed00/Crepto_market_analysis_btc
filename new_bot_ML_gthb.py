import requests as rq
import pandas as pd
import numpy as np
import time 
import joblib
import os 


TELEGRAM_TOKEN =""

CHAT_ID = ""

crypto_symbol = input("Enter the cryptocurrency symbol (e.g., BTC, ETH) : \n").upper() 


sec=["1m","3m" , "5m" ,"15m"  , "30m" , "1h" , "2h","4h","6h","8h","12h"]

def qes():
	t=input("Select timeframe : (1m , 3m , 5m ,15m , 30m , 1h , 2h , 4h , 6h , 8h , 12h ) : \n")
	if t in sec :
		return t
	else :
		print("invalide choice please repet :")
		
		return qes()
t=qes()

def t_f():
	global t
	t_frim=""
	h_m=""
	for i in t:
		if i.isdigit():
			t_frim+=i
		else:
			h_m+=i
	tfrm=int(t_frim)
	if  "m" in h_m[-1]:
		return (tfrm*60) +10
	elif "h" in h_m[-1] :
		return (tfrm*3600) +10
	
def send_to_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        dt=rq.post(url, data=data, timeout=10)
        print(dt.text)
    except:
        pass


def clean():
	os.system("cls"if os.name=="nt"else "clear")

dt100=[]
price=[]
close_price=[]
open_price=[]

def detailes():
	urlp = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={crypto_symbol}_USDT"
	
	url=f"https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair={crypto_symbol}_USDT&interval={t}"
	headers={
"User-Agent":"Mozilla/5.0"
	}
	try:
		p=rq.get(url,headers=headers).json()
		
		close_price.append(float(p[-2][5]))
		open_price.append(float(p[-2][2]))
		
		for i in (p):
			if i[7]=="true":
				dt100.append(i)
			
		pp=rq.get(urlp,headers=headers).json()
		price.append(pp[0]["last"])
		
		
		
	except Exception as e :
		print("Error while loading data")
		time.sleep(10)
		print("please . wait .... ")
		detailes()
		
#quntty
def qntt():
	return sum([float(dt100[i][6])for i in range(20)])/20
	
			
	
#rsi

avg_g=None
avg_l=None
def rsi():
	global avg_g,avg_l
	gain=0
	los=0
	last=dt100[-16:]
	for d in range(len(last)-1):
		diff=float(last[d+1][5]) -float(last[d][5])
		if diff>0:
			gain+=diff
		elif diff<0:
			los+=(abs(diff))
	if avg_g is None:
		avg_g=gain/14
		avg_l=los/14
		
	elif avg_g is  not None:
		dif=float(dt100[-1][5]) - float(dt100[-2][5])
		gain=dif if dif >0 else 0
		los=abs(dif) if dif <0 else 0 
		avg_g=(avg_g*13+gain)/14
		avg_l=(avg_l*13+los)/14
	if avg_g==0:
		return 0
	elif avg_l==0:
		return 100
	rs=avg_g/avg_l
	rsi =100 - ( 100 / (1+rs))
	return rsi
	
			
#ema12
prv_ema12=None
def ema12():
	global  prv_ema12
	k=2/(12+1)
	last=dt100[-12:]
	tt=0
	if prv_ema12 is None:
		for e in last:
			e=float(e[5])
			tt+=e
		prv_ema12=tt/12
	else:
		prv_ema12=float(dt100[-1][5])*k+prv_ema12*(1-k)
	return prv_ema12 
	
#ema14
prv_ema14=None		
def ema14():
	global prv_ema14
	k=2/(14+1)
	last=dt100[-14:]
	if prv_ema14 is None:
		prv_ema14=sum(float(e[5]) for e in last)/14
	else:
		prv_ema14=float(dt100[-1][5])*k+prv_ema14*(1-k)
	return prv_ema14
		
#ema26
prv_ema26=None
def ema26():
	global prv_ema26
	k=2/(26+1)
	last=dt100[-26:]
	if prv_ema26 is None :
		prv_ema26=sum(float(e[5]) for e in last)/26
	else:
		prv_ema26=float(dt100[-1][5])*k+prv_ema26*(1-k)
	return prv_ema26

#macd line 
macd_list=[]
def macd_line():
	ema26_value = ema26()
	ema12_value = ema12()
	macd=ema12_value - ema26_value
	macd_list.append(macd)
	return macd

#signal line 

prv_signal=None
def signal_line(macd_value):
	global prv_signal
	k=2/(9+1)
	if len(macd_list)==0:
		return None
	if prv_signal is None:
		if  len(macd_list)<9:
			prv_signal=sum(macd_list)/len(macd_list)
		else:
			prv_signal=sum(macd_list[:9])/9
	prv_signal = macd_value*k+prv_signal*(1-k)
	return prv_signal

#histogram
def histo(macd_value , signal_value):
	return macd_value - signal_value

#pivot point

def pvpn():
	last=dt100[-14:]
	pp_list=[]
	for p in last:
		h=float(p[3])
		l=float(p[4])
		c=float(p[5])
		pp=(h+l+c)/3
		pp_list.append(pp)
	pp=sum(pp_list)/len(pp_list)
	return pp
	
	
#support
def supp(p):
	s1=2 * p - float(dt100[-1][3])
	s2=p-(float(dt100[-1][3]) - float(dt100[-1][4]))
	return s1 , s2 

#resistance
def rest(p):
	r1=2 * p - float(dt100[-1][4])
	r2=p + (float(dt100[-1][3]) - float(dt100[-1][4]))
	return r1 , r2
	
def std():
		closses=[float(s[5]) for s in dt100[-20:]]
		return pd.Series(closses).std()
		
def ma():
	ma10=sum([float(dt100[i][5])for i in range(10)])/10
	
	ma20=sum([float(dt100[e][5])for e in range(20)])/20
	
	ma50=sum([float(dt100[a][5])for a in range(50)])/50
	return ma10 , ma20 , ma50
	
def stochastic():
	close=float(dt100[-1][5])
	mx=max([float(dt100[i][3])for i in range(-20,0)])
	mn=min([float(dt100[i][4])for i in range(-20,0)])
	return ((close-mn)/(mx-mn))*100

result=False	
def buy():
	global result ,close_price,open_price
	open=open_price[-1]
	close=close_price[-1]
	ma10_value , ma20_value , ma50_value=ma()
	rsi_value=rsi()
	ema12_value=ema12()
	ema14_value=ema14()
	ema26_value=ema26()
	std_value=std()
	upper=ma20_value+(2*std_value)
	lower=ma20_value-(2*std_value)
	macd_value = macd_line()
	sgnl_value=signal_line(macd_value)
	histo_value = histo(macd_value,sgnl_value)
	pvpn_value = pvpn()
	supp1_valu,supp2_valu= supp(pvpn_value)
	rest1_value , rest2_value= rest(pvpn_value)
	#signal_value , value=snl()
	sto_value=stochastic()
	qnt_now=float(dt100[-1][6])
	qnt_value=qntt()
	buyscore=0
	if rsi_value<=35: 
		buyscore+=2
		print("RSI")
	if sto_value<=40:
		buyscore+=2
		print("stochastic")
	if close_price[-1]<= lower:
		buyscore += 1
		print("close price")
	if ema12_value > ema26_value:
		buyscore+= 1
		print("ema12>ema26")
	if macd_value > sgnl_value:
		buyscore += 1
		print("macd")
	if qnt_now>qnt_value:
		buyscore += 1
		print("Quentity")
	print("\n| Signal buy : ",buyscore,"\n")
	
	rsisto=rsi_value<=30 and sto_value<=30
	
	trend_up=(ma10_value > ma20_value and ma20_value >ma50_value)or (qnt_now>ma50_value)
	trend_down= (ma10_value < ma20_value and ma20_value < ma50_value)or(qnt_now<ma50_value) 
	
	if result==False :
		
		#if buyscore>=4 and trend_up and rsi_value<=30 :
			#result = True
		#	return "Buy Signal with buy Score  "
		if (ema12_value > ema26_value and ma10_value > ma20_value and ma20_value > ma50_value and macd_value > sgnl_value and histo_value > 0 and 42 < rsi_value < 58 and qnt_now > qnt_value and close > open and trend_up):
		      result = True
		      return "Buy Strong Trend Alignment + MACD + Volume"
		elif (histo_value > 0 and ema12_value > ema26_value and 40 < rsi_value < 60 and qnt_now > qnt_value and close > open and trend_up):
		        	result = True
		        	return "Buy MACD Hist + EMA + Volume + Candle"	
		elif (rsi_value < 33 and trend_up and qnt_now > qnt_value and (close <= supp1_valu or close <=supp2_valu or close <= lower_b) and close > open):
		      result = True
		      return "Buy Deep RSI Oversold + Support + Volume"	
		elif (macd_value > sgnl_value and trend_up and qnt_now > qnt_value and close > open and rsi_value < 68):
		      result = True
		      return "Buy MACD Crossover + Trend + Volume"
		elif (ema12_value > ema26_value and ma10_value > ma20_value and qnt_now > qnt_value and rsi_value > 50 and close > open and trend_up):
		      result = True 
		      return "Buy Short Term Trend + Volume"
		elif (ema12_value > ema26_value and ma10_value > ma20_value and ma20_value > ma50_value and macd_value > sgnl_value and 40 < rsi_value < 55 and qnt_now > qnt_value and close > open):
			result = True
			return "Buy with line and power (Improved)"
		elif histo_value > 0 and ema12_value > ema26_value and close > open and 40 < rsi_value < 55 and qnt_now > qnt_value:
		    result = True
		    return "Buy with MACD Hist + Candle + Volume"
		elif rsi_value < 32 and trend_up and qnt_now > qnt_value and (close <= supp1_valu or close <= lower_b):
		  result = True
		  return "Buy Deep RSI Oversold + Trend + Volume + Support"
		elif macd_value > sgnl_value and trend_up and qnt_now > qnt_value and close > open and 40 < rsi_value < 65:
		  result = True
		  return "Buy MACD + Trend + Volume + Candle"
		elif ema12_value > ema26_value and ma10_value > ma20_value and ma20_value > ma50_value and qnt_now > qnt_value and rsi_value > 48 and close > open:
		  result = True 
		  return "Buy short term trend + strength + volume"
		elif close<=lower and sto_value <40 and(close <= supp1_valu or close <= supp2_valu )and qnt_now > qnt_value:
			result=True 
			return "Buy with oversold +support and volume "		
		elif rsisto and trend_up and qnt_now>qnt_value:
			result= True
			return "Buy Signal with rsi and stochastic " 
		elif macd_value>sgnl_value and trend_up and qnt_now>qnt_value:
			result=True
			return "Buy macd and trend and qntt"
		elif rsi_value <30 and qnt_now >qnt_value:
			result=True
			return "Buy with rsi and qentity"
		elif ema12_value >ema26_value and ma10_value>ma20_value and ma20_value>ma50_value and macd_value>sgnl_value and 30<rsi_value<50:
			result=True
			return "Buy with line and power"
		elif histo_value >0 and ema12_value > ema26_value and close > open and 30<rsi_value<50:
			result=True
			return "Buy with close open "
		elif ema12_value >ema26_value and ma10_value >ma20_value and qnt_now >qnt_value and 30<rsi_value>50 :
			result=True 
			return " Buy short term and trend + strength"
			
		else :
			return "Waiting"
			
	elif result==True :
		if rsi_value>=70 and sto_value>=70:
			result=False
			return "Sell with rsi and sto"
		elif trend_down and rsi_value>65:
			result=False
			return "Sell with trend down"
		elif close >=upper and sto_value >=70 and qnt_now >qnt_value:
			result=False
			return "Sell with overbought"
		elif histo_value <0 and close<open and rsi_value >=70:
			result=False
			return "Sell with mmnt down "
		else:
			return "Waiting"
	else:
			return "Waiting"
			
def Traiding():
	while True:
		second=t_f()
		detailes()
		#price=price[-1]
		
		print("\nPrice",crypto_symbol," :",price[-1],"\n")
		print("Close price : ",close_price[-1],"\n")
		ma10_value , ma20_value , ma50_value=ma()
		print("\n| MA10 : ",ma10_value)
		print("| MA20 : ",ma20_value)
		print("| MA50 : ",ma50_value)
		ema12_value=ema12()
		print("| EMA12 : ",ema12_value)
		ema14_value=ema14()
		print("| EMA14 : ",ema14_value)
		ema26_value=ema26()
		print("| EMA26 : ",ema26_value)
		std_value=std()
		print("| STD : ",std_value)
		upper=ma20_value+(2*std_value)
		print("| Upper B : ",upper)
		lower=ma20_value-(2*std_value)
		print("| Lower B : ",lower)
		macd_value = macd_line()
		print("| Macd Line : ",macd_value)
		sgnl_value=signal_line(macd_value)
		print("| Signal Line : ",sgnl_value)
		histo_value = histo(macd_value,sgnl_value)
		print("| Histogram : ",histo_value)
		pvpn_value = pvpn()
		print("| Pivot point : ",pvpn_value)
		supp1_value , supp2_value = supp(pvpn_value)
		print("| Support 1 : ",supp1_value)
		print("| Support 2 : ",supp2_value)
		qnt_value=qntt()
		print("| Quentity Now : ",dt100[-1][6])
		print("| Quentity : ",qnt_value)
		rest1_value , rest2_value= rest(pvpn_value)
		print("| Resistance 1 : ",rest1_value)
		print("| Resistance 2 : ",rest2_value)
		print("| Stochastic : ",stochastic())
		trend_up=ma10_value > ma20_value and ma20_value >ma50_value 
		print("| Trend up : ",trend_up)
		trend_down= ma10_value < ma20_value and ma20_value < ma50_value 
		print("| Trend down : ",trend_down)
		rsi_value=rsi()
		print("| RSI : ",rsi_value,"\n")
		#signal_value , value =snl()
		#print("| Signal : ",signal_value ,"  ",value)
		buy_value=buy()
		print("\n| The Final Decision : ", buy_value,"\n")
		
		if "Buy" in buy_value or "Sell" in buy_value: 
			msg=(f"""⚡ إشارة {crypto_symbol} جديدة

العملة: <b>{crypto_symbol}USDT</b>
السعر: <b>{price[-1]}</b>
الإشارة: <b>{buy_value}</b>
الوقت: <b>{time.strftime("%H:%M:%S - %d/%m/%Y")}</b>

@BTC_1000x_bot""")
			send_to_telegram(msg)
			
		time.sleep(second) 
		f"""
| Price : {price[-1]}
| RSI : {rsi_value}
| EMA12 : {ema12_value}
| EMA14 : {ema14_value}
| EMA26 : {ema26_value}
| MACD Line : {macd_value}
| Signal Line : {sgnl_value}
"""

Traiding()		

def get_analyse_dt():
	r_close=dt100[-1][2]
	r_high=dt100[-1][3]
	r_low=dt100[-1][4]
	r_open=dt100[-1][5]
	return r_open,r_high,r_low,r_close,rsi,ema14(),macd_line(),histo(macd_value,sgnl_value),pvpn(),supp(pvpn_value),rest(pvpn_value)
	

