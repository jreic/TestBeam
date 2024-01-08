from ROOTTools import *
import sys
import numpy as np

rebinfactor = 5

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning


ps = plot_saver(plot_dir("overlay_bias_scan_MJ531_distributions"), size=(600,600), log=False, pdf=True)
ps.c.SetLeftMargin(0.14)
ps.c.SetTopMargin(0.05)
ps.c.SetRightMargin(0.05)
ps.update_canvas()

plot_paths = [] 
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSizeUpToMax_Dut0")

# Adapter card had 11kOhm total according to https://docs.google.com/document/d/1xQe5dZbrX8M0AEe-T-NlyIX6yhK-nU5i73rB3I9S3rc/edit, so V_sensor = V_supply - 11kOhm * leakage current in microamps
#
# i.e. V_supply - 11 * Ileak/1000. = V_sensor
#
# In 0deg_angle data (Nov 2021)
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
#
# In 10deg_angle data (Dec 2021)
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

for plot_path in plot_paths :
    plot_name = plot_path.split("/")[-1]

    fpath0deg_105V = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46712_46715.root"
    fpath0deg_85V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46719_46723.root"
    fpath0deg_65V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46724_46728.root"
    fpath0deg_45V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46729_46738.root"
    fpath0deg_25V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46739_46742.root"
    fpath0deg_20V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46743_46746.root"
    fpath0deg_15V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46747_46750.root"
    fpath0deg_10V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46752_46756.root"
    fpath0deg_5V   = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46757_46767.root"
    #fpath0deg_0V   = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs46762_46769.root"


    files0deg = [ ROOT.TFile(fpath0deg_105V)
            , ROOT.TFile(fpath0deg_85V)
            , ROOT.TFile(fpath0deg_65V) 
            , ROOT.TFile(fpath0deg_45V) 
            , ROOT.TFile(fpath0deg_25V) 
            , ROOT.TFile(fpath0deg_20V) 
            , ROOT.TFile(fpath0deg_15V) 
            , ROOT.TFile(fpath0deg_10V) 
            , ROOT.TFile(fpath0deg_5V ) 
            #, ROOT.TFile(fpath0deg_0V ) 
            ]

    labels0deg = [100.6, 81.1, 61.2, 42.2, 22.9, 18.1, 13.4, 8.6, 4.0] #, 0.0]

    fpath10deg_100V = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51160_51166.root"
    fpath10deg_90V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51169_51174.root"
    fpath10deg_80V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51175_51178.root"
    fpath10deg_70V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51179_51181.root"
    fpath10deg_60V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51182_51184.root"
    fpath10deg_50V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51186_51188.root"
    fpath10deg_40V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51189_51191.root"
    fpath10deg_30V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51192_51194.root"
    fpath10deg_20V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51195_51198.root"
    fpath10deg_10V  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks/Chewie_Runs51199_51202.root"

    files10deg = [ ROOT.TFile(fpath10deg_100V)
            , ROOT.TFile(fpath10deg_90V)
            , ROOT.TFile(fpath10deg_80V)
            , ROOT.TFile(fpath10deg_70V)
            , ROOT.TFile(fpath10deg_60V)
            , ROOT.TFile(fpath10deg_50V)
            , ROOT.TFile(fpath10deg_40V)
            , ROOT.TFile(fpath10deg_30V)
            , ROOT.TFile(fpath10deg_20V)
            , ROOT.TFile(fpath10deg_10V)
            ]

    labels10deg = [98.0, 88.1, 78.2, 68.4, 58.5, 48.6, 38.7, 28.9, 19.1, 9.4]

    colors = [ROOT.kRed+2,ROOT.kRed,ROOT.kOrange+1,ROOT.kYellow+1,ROOT.kGreen+1,ROOT.kAzure+1,ROOT.kBlue+1,ROOT.kViolet+6,ROOT.kViolet-4,ROOT.kMagenta]

    hists = []

    leg = ROOT.TLegend(0.63, 0.48, 0.945, 0.83)
    leg.SetMargin(0.15)

    #datasets = files0deg
    #labels = labels0deg
    files = files10deg
    labels = labels10deg

    for index in xrange(0,len(files)) :
        f = files[index]
        h = f.Get(plot_path)

        if "Landau" in plot_name :
            h.SetName(str(labels[index]))
            h.SetTitle(str(labels[index]))
            h.SetLineWidth(2)
            h.SetLineColor(colors[index])
            h.SetMarkerColor(colors[index])

            h.Rebin(rebinfactor)
            h.Scale(1/h.Integral())
            h.GetXaxis().SetRangeUser(0, 15000)

            ps.c.cd()
            if index == 0 :
                h.Draw("hist")
                h.GetXaxis().SetTitleOffset(1.27)
                h.GetYaxis().SetRangeUser(0.001,1)
                h.GetYaxis().SetTitle("fraction / bin")
                h.GetYaxis().SetTitleOffset(1.87)
            else :
                h.Draw("hist same")

        leg.AddEntry(h," -"+h.GetName()+"V, mean = %.1f ke" % (h.GetMean()/1000.),"l")
        h.SetStats(0)
        hists.append(h)
        ps.update_canvas()

    if "Landau" in plot_name :
        histmin = 5e-6
        histmax = 0.03*rebinfactor

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)

    plotlabel = ROOT.TLatex()
    plotlabel.SetNDC()
    plotlabel.SetTextFont(42)
    plotlabel.SetTextSize(0.027)
    plotlabel.DrawLatex(0.635, 0.90, "CNM, (1.2^{+0.20}_{-0.22}) #times 10^{16} n_{eq}/cm^{2}")
    plotlabel.DrawLatex(0.635, 0.85, "1600e, turn = 10#circ")

    leg.SetBorderSize(0)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
