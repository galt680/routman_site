from __future__ import division
import pandas as pd
import numpy as np
try:
	import quandl as q
except:
	import Quandl as q
from mv import VIX,VX1,VX2,VXST,T1,T2,VX3,VXST,VXV
from passwords import auth

def decider(signal,value1,value2, reverse = False):
	if reverse == False:
		if signal > value1:
			return 1
		elif signal < value2:
			return -1
		else:
			return 0
	else:
		if signal < value1:
			return 1
		elif signal > value2:
			return -1
		else:
			return 0


#vforce is the vix - 50dayMA of the VIX. below zero is good, between 0-10% is neutral, and above 10% is bad.
def VForce(VIX = VIX):
# take the most recent value of the vix
	VIX1 = VIX[-1]
# convert the list of VIX values	 to pandas series so as to get the moving average. Window length in rolling is length of moving average
	VIX = pd.Series(VIX)
	mVIX = VIX.rolling(window = 50, center = False).mean()
# get last value of moving average
	mVIX = mVIX.tail(1)
# calculate vforce and round
	vforce	= round(float((VIX1/mVIX) - 1),2)
	# vforce = round(vforce,100)
	print decider(vforce, 0,.1,reverse = True)
	return decider(vforce, 0,.1,reverse = True)
# contango represents  difference between VX1 and VX2 above 5% is bullish and below -5% is bearish XIV = (64,-32) VXX = (-2,-31)
def Contango(VX1 = VX1, VX2 = VX2):
# get most recent values of VX1 and VX3
	VX1 = VX1[-1]
	VX2 = VX2[-1]
# calculate contango and round
	contango = round((VX2/VX1)-1,2)
	return decider(contango,.05,-.05)

	print "The Contango is %s"%contango
# The % difference between VX1 and VIX. Over 5% is good, between 0% and 5% is neutral, below 0% is negative
def Roll_Yield(VIX = VIX,VX1 = VX1):
# Get the latest values of VIX and VX1
	VIX = VIX[-1]
	VX1 = VX1[-1]
# Calculate the Roll_Yield
	rolly = round(((VX1/VIX)-1),2)
	return decider(rolly,.05,0)
	print "The Roll_Yield is %s"%rolly
# get the contango_roll which is % differance of VX2 and VIX. Above 10% is good between 0% and 10% is neutral and below 0% is bad.
def Contango_Roll(VIX = VIX, VX2 = VX2):
	VIX = VIX[-1]
	VX2 = VX2[-1]
	contango_roll = ((VX2/VIX) - 1)
	return decider(contango_roll,.1,0)
	print "The Contango Roll is %s"%contango_roll


#The difference between VIX and VXST. above 1 is good, below zero is bad; else neutral.
def VDelta(VIX = VIX, VXST = VXST):
	VIX = VIX[-1]
	VXST = VXST[-1]
	vdelta = VIX - VXST
	return decider(vdelta,1,0)
	print "The Vdelta is %s"%vdelta

# higher than 25 is good; below 0 is bad and else is neutral
def VCO(VIX = VIX,VX1 = VX1, VX2 = VX2, VX3 = VX3):
	if T1 < 10:
		VIX = VIX[-1]
		VX2 = VX2[-1]
		VX3 = VX3[-1]
		vco = VIX -45 + 1000 * ((VX3/VX2)-1)
	else:
		VIX = VIX[-1]
		VX1 = VX1[-1]
		VX2 = VX2[-1]
		vco = VIX -45 + 1000 * ((VX2/VX1)-1)
	return decider(vco,25,0)
	print "The VCO is %s"%vco


# Over 50 is good under zero is bad else is neutral
def VTRO(VIX = VIX, VXST = VXST,VXV = VXV, VX1 = VX1, VX2 = VX2):
	VTRO1 = (1000 * ((21/84)*(VIX[-1]/VXST[-1] - 1) + ((84 - T1 - T2) /84)*(VX1[-1]/VIX[-1] - 1) + (T2/84)*(VX2[-1]/VX1[-1] - 1) +(T1/84)*(VXV[-1]/VX2[-1] - 1)))
	VTRO2 = (1000 * ((21/84)*(VIX[-2]/VXST[-2] - 1) + ((84 - (T1+1) - (T2+1)) /84)*(VX1[-2]/VIX[-2] - 1) + ((T2+1)/84)*(VX2[-2]/VX1[-2] - 1) +((T1+1)/84)*(VXV[-2]/VX2[-2] - 1)))
	VTRO3 = (1000 * ((21/84)*(VIX[-3]/VXST[-3] - 1) + ((84 - (T1+2) - (T2+2)) /84)*(VX1[-3]/VIX[-3] - 1) + ((T2+2)/84)*(VX2[-3]/VX1[-3] - 1) +((T1+2)/84)*(VXV[-3]/VX2[-3] - 1)))
	vtro = (VTRO1 + VTRO2 + VTRO3)/3
	return decider(vtro,50,0)
	print "VTRO is at %s"%vtro


def VATR():
	VIXC = q.get("CBOE/VIX", authtoken = "UxWHyskR-2WjjvSsdxu4",transformation="rdiff")["VIX Close"]
	VIXC = list(VIXC)
	if VIXC[-1] != VIX[-1]:
		VIXC.append((VIX[-1]-VIX[-2])/VIX[-2])
	adj_vixc = []
	for value in VIXC:
		adj_vixc.append(abs(value))
#	  print np.mean(adj_vixc[-5:])
	vatr = []
	for x in range(0,11):
		vatr.append(round(np.mean(adj_vixc[-5-x:len(adj_vixc)-x]),4))
	vatr = vatr[0]
	if (.03<vatr<.09):
		return 1
	elif vatr> .09:
		return -1
	else:
		return 0
	print "The VATR is %s"%vatr
def vix_put_call():
	pcratio = (q.get("CBOE/VIX_PC",authtoken = auth)["VIX Put-Call Ratio"])
	if float(pcratio[-1:]) > pcratio.quantile(.95):
		return "The VIX Put/Call ratio is at %s, this is extremely overbought and bearish for the SPY."%float(pcratio[-1:])
	elif float(pcratio[-1:]) > pcratio.quantile(.85):
		return "The VIX Put/Call ratio is at %s, this is slightly overbought and bearish for the SPY."%float(pcratio[-1:])
	elif float(pcratio[-1:]) < pcratio.quantile(.05):
		return "The VIX Put/Call ratio is at %s, this is extremely oversold and bullish for the SPY."%float(pcratio[-1:])
	elif float(pcratio[-1:]) < pcratio.quantile(.15):
		return "The VIX Put/Call ratio is at %s, this is slightly oversold and bullish for the SPY."%float(pcratio[-1:])
	else:
		return "The VIX Put/Call ratio is at %s, this is a neutral reading."%float(pcratio[-1:])
def evaluate():
	statement = vix_put_call()
	a = Contango()
	b= Roll_Yield()
	c = VForce()
	d = Contango_Roll()
	e = VDelta()
	g = VATR()
	f = VCO()
	h = VTRO()
	total  = a + b + c	+ d +e + f + g +h
	if total > 4:
		return "The VIX is at %s,%s \n	The Full Volatility Index is bullish."%(VIX[-1],statement)
	else:
		return "The VIX is at %s,%s \n The Full Volatility Index is bearish."%(VIX[-1],statement)
if __name__ == "__main__":
	evaluate()


