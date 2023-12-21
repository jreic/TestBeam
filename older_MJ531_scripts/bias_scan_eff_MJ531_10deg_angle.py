from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_bias_scan_MJ531_10deg_angle"), size=(600,600), log=False, pdf=True)
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
# 100       | 180.8         | 98.0
#  90       | 176.0         | 88.1
#  80       | 160.5         | 78.2
#  70       | 150.0         | 68.4
#  60       | 138.0         | 58.5
#  50       | 127.0         | 48.6
#  40       | 114.66667     | 38.7
#  30       | 103           | 28.9
#  20       | 85            | 19.1
#  10       | 58            |  9.4

for plot_name in plot_names :

    fpath100V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51160_51166/"+plot_name+".root"
    fpath90V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51169_51174/"+plot_name+".root"
    fpath80V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51175_51178/"+plot_name+".root"
    fpath70V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51179_51181/"+plot_name+".root"
    fpath60V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51182_51184/"+plot_name+".root"
    fpath50V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51186_51188/"+plot_name+".root"
    fpath40V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51189_51191/"+plot_name+".root"
    fpath30V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51192_51194/"+plot_name+".root"
    fpath20V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51195_51198/"+plot_name+".root"
    fpath10V  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs51199_51202/"+plot_name+".root"

    files = [ ROOT.TFile(fpath100V)
            , ROOT.TFile(fpath90V)
            , ROOT.TFile(fpath80V)
            , ROOT.TFile(fpath70V)
            , ROOT.TFile(fpath60V)
            , ROOT.TFile(fpath50V)
            , ROOT.TFile(fpath40V)
            , ROOT.TFile(fpath30V)
            , ROOT.TFile(fpath20V)
            , ROOT.TFile(fpath10V)
            ]

    labels = [98.0, 88.1, 78.2, 68.4, 58.5, 48.6, 38.7, 28.9, 19.1, 9.4]

    hists = []

    outhist = ROOT.TH1F(plot_name, plot_name, (int(max(labels))+12), int(min(labels)-10), int(max(labels))+2)

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
