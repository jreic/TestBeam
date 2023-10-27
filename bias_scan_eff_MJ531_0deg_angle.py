from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_bias_scan_MJ531_0deg_angle"), size=(600,600), log=False, pdf=True)
ps.c.SetLeftMargin(0.15)
ps.update_canvas()

plot_names = [ 
               "EfficiencyRef_Dut0",
               "Efficiency_Dut0"
             ]

# Adapter card had 11kOhm total according to https://docs.google.com/document/d/1xQe5dZbrX8M0AEe-T-NlyIX6yhK-nU5i73rB3I9S3rc/edit, so V_sensor = V_supply - 11kOhm * leakage current in microamps
#
# i.e. V_supply - 11 * Ileak/1000. = V_sensor
#
# V supply  | I_leak (uA)   | V_sensor
# 105       | 398.4         | 100.6
#  85       | 350.2         | 81.1478
#  65       | 310.8         | 61.5812
#  45       | 259           | 42.151
#  25       | 195           | 22.855
#  20       | 172.75        | 18.09975
#  15       | 150           | 13.35
#  10       | 123.2         | 8.6448
#   5       | 85.66666667   | 4.
#   0       | 13            | -0.143

for plot_name in plot_names :

    fpath105V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46712_46715/"+plot_name+".root"
    fpath85V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46719_46723/"+plot_name+".root"
    fpath65V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46724_46728/"+plot_name+".root"
    fpath45V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46729_46738/"+plot_name+".root"
    fpath25V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46739_46742/"+plot_name+".root"
    fpath20V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46743_46746/"+plot_name+".root"
    fpath15V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46747_46750/"+plot_name+".root"
    fpath10V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46752_46756/"+plot_name+".root"
    fpath5V   = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46757_46767/"+plot_name+".root"
    fpath0V   = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46762_46769/"+plot_name+".root"

    files = [ ROOT.TFile(fpath105V)
            , ROOT.TFile(fpath85V)
            , ROOT.TFile(fpath65V) 
            , ROOT.TFile(fpath45V) 
            , ROOT.TFile(fpath25V) 
            , ROOT.TFile(fpath20V) 
            , ROOT.TFile(fpath15V) 
            , ROOT.TFile(fpath10V) 
            , ROOT.TFile(fpath5V ) 
            , ROOT.TFile(fpath0V ) 
            ]

    labels = [100.6, 81.1, 61.2, 42.2, 22.9, 18.1, 13.4, 8.6, 4.0, -0.1]
    hists = []

    outhist = ROOT.TH1F(plot_name, plot_name, (int(max(labels))+11), int(min(labels)-1), int(max(labels))+10)

    leg = ROOT.TLegend(0.50, 0.60, 0.90, 0.90)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        eff = h.GetBinContent(1)
        err = h.GetBinError(1)
        if eff == 0 : eff = 1e-5
        outhist.SetBinContent(outhist.FindBin(labels[index]), eff)
        outhist.SetBinError(outhist.FindBin(labels[index]), err)

        ps.c.cd()
        ps.update_canvas()

    if plot_name == "hClusterSize_Dut0" :
        histmin = 5e-6
        histmax = 1
    elif "ResidualsClusterSize2" in plot_name :
        histmin = 1e-5
        histmax = 0.06
    elif "Residuals" in plot_name :
        histmin = 5e-6
        histmax = 0.04
    elif "Efficiency" in plot_name :
        histmin = 0.
        histmax = 1.0001

    outhist.GetYaxis().SetRangeUser(histmin, histmax)
    outhist.GetYaxis().SetTitleOffset(2.0)
    outhist.GetYaxis().SetTitle("efficiency")
    outhist.GetXaxis().SetTitle("bias voltage (V)")
    outhist.SetLineColor(ROOT.kBlack)
    outhist.SetMarkerColor(ROOT.kBlack)
    outhist.SetMarkerStyle(20)
    outhist.Draw("pE1")
    outhist.SetStats(0)
    #leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
