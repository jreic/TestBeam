#!/usr/bin/env python
from ROOT import *
import os
from array import array

gStyle.SetOptStat(000000000)

filelist =[]
runlist = array( 'd' )
Xmean, Ymean, Xrms, Yrms = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

indir="root_files/"
for file in os.listdir(indir):
    if file.endswith(".root") and file.startswith("Chewie_Run") and (not file.startswith("Chewie_Runs")):
        runlist.append(float(file.lstrip("Chewie_Run").rstrip(".root")))

        tfile = TFile.Open(indir+file, "read")
        hX = tfile.Get("Resolution/Dut0/XResiduals/hXResiduals_Dut0;1")
        hY = tfile.Get("Resolution/Dut0/YResiduals/hYResiduals_Dut0;1")
        Xmean.append(hX.GetMean())
        Xrms.append(hX.GetRMS())
        Ymean.append(hY.GetMean())
        Yrms.append(hY.GetRMS())
        print file+"; X Mean: "+str(hX.GetMean())+"; Y Mean: "+str(hY.GetMean())+"; X RMS: "+str(hX.GetRMS())+"; Y RMS: "+str(hY.GetRMS())




gXmean = TGraph(len(runlist),runlist,Xmean)
gXrms = TGraph(len(runlist),runlist,Xrms)
gYmean = TGraph(len(runlist),runlist,Ymean)
gYrms = TGraph(len(runlist),runlist,Yrms)

Block = TBox(700,0,100,1000)
Block.SetFillColorAlpha(kRed, 0.35)

gXmean.SetMarkerStyle(20)
gXrms.SetMarkerStyle(20)
gYmean.SetMarkerStyle(20)
gYrms.SetMarkerStyle(20)

gXmean.SetTitle("DUT X Residuals Mean")
gXrms.SetTitle("DUT X Residuals RMS")
gYmean.SetTitle("DUT Y Residuals Mean")
gYrms.SetTitle("DUT Y Residuals RMS")
gXmean.GetXaxis().SetTitle("Run Number")
gXmean.GetYaxis().SetTitle("X Mean")
gYmean.GetXaxis().SetTitle("Run Number")
gYmean.GetYaxis().SetTitle("Y Mean")
gXrms.GetXaxis().SetTitle("Run Number")
gXrms.GetYaxis().SetTitle("X RMS")
gYrms.GetXaxis().SetTitle("Run Number")
gYrms.GetYaxis().SetTitle("Y RMS")

cXmean = TCanvas('X Mean', 'X Mean', 1200, 400) 
gXmean.Draw('AP')
Block.Draw('Same')
cXmean.SaveAs('XMean.png')

cYmean = TCanvas('Y Mean', 'Y Mean', 1200, 400) 
gYmean.Draw('AP')
cYmean.SaveAs('YMean.png')

cXrms = TCanvas('X RMS', 'X RMS', 1200, 400) 
gXrms.Draw('AP')
cXrms.SaveAs('Xrms.png')

cYrms = TCanvas('Y RMS', 'Y RMS', 1200, 400) 
gYrms.Draw('AP')
cYrms.SaveAs('Yrms.png')
cYrms.SaveAs('Yrms.C')

