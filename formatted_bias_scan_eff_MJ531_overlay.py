from ROOTTools import *
import sys
import numpy as np

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning


ps = plot_saver(plot_dir("formatted_bias_scan_MJ531_overlay"), size=(600,600), log=False, pdf=True)
ps.c.SetLeftMargin(0.1)
ps.c.SetTopMargin(0.05)
ps.c.SetRightMargin(0.05)
ps.update_canvas()

plot_paths = [] 
plot_paths.append("Efficiency/Dut0/Efficiency/Efficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyRef_Dut0")
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

    graphs = []

    datasets = [files0deg, files10deg]
    labels = [labels0deg, labels10deg]

    for index_dataset in xrange(0, len(datasets)) :
        files = datasets[index_dataset]

        x = []
        y = []
        exl = []
        exh = []
        eyl = []
        eyh = []

        for index in xrange(0,len(files)) :
            f = files[index]
            h = f.Get(plot_path)
            
            if "Efficiency" in plot_name :
                h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))

                nevents = h_norm.GetBinContent(1)
                eff = h.GetBinContent(1)

                abs_err_down, abs_err_up = clopper_pearson_abs_err(nevents, eff)

                voltage = labels[index_dataset][index]

                x.append(voltage)
                y.append(eff*100)
                exl.append(0)
                exh.append(0)
                eyl.append(abs_err_down*100)
                eyh.append(abs_err_up*100)

            elif "Landau" in plot_name :
                langaus = ROOT.langausFit(h)
                fit = h.Fit(langaus, "RBLSQ0")
                h.GetXaxis().SetRangeUser(0, 25000)

                mpv = fit.Parameter(1)/1000.
                mpverr = fit.ParError(1)/1000.

                if fit.Chi2() / fit.Ndf() > 5 : continue

                #print h.Integral(), mpv, "+/-", mpverr, fit.Chi2()/fit.Ndf()

                voltage = labels[index_dataset][index]

                x.append(voltage)
                y.append(mpv)
                exl.append(0)
                exh.append(0)
                eyl.append(mpverr)
                eyh.append(mpverr)

        x = np.array(x, dtype='double')
        y = np.array(y, dtype='double')
        exl = np.array(exl, dtype='double')
        exh = np.array(exh, dtype='double')
        eyl = np.array(eyl, dtype='double')
        eyh = np.array(eyh, dtype='double')

        # protection against empty arrays!
        if len(x) == 0 : continue

        graph = ROOT.TGraphAsymmErrors(len(x),x,y,exl,exh,eyl,eyh)
        is0deg = (files == files0deg)

        graph.SetTitle("CNM, 1.#color[2]{4}#times10^{16} n_{eq}/cm^{2}, " + ("1200e, turn = 0#circ" if is0deg else "1600e, turn = 10#circ"))
        graph.SetLineColor(ROOT.kBlack if is0deg else ROOT.kRed)
        graph.SetMarkerColor(ROOT.kBlack if is0deg else ROOT.kRed)
        graph.SetMarkerStyle(20 if is0deg else 24)
        graph.SetFillColor(0)

        if "Efficiency" in plot_name :
            xmin = 0
            xmax = 101
            ymin = 0.
            ymax = 1.005*100

            graph.GetXaxis().SetRangeUser(xmin, xmax)
            graph.GetYaxis().SetRangeUser(ymin, ymax)

            graph.GetXaxis().SetTitleOffset(1.25)
            graph.GetXaxis().SetTitle("Bias Voltage [V]")

            graph.GetYaxis().SetTitleOffset(1.4)
            graph.GetYaxis().SetTitle("Efficiency [%]")

        elif "Landau" in plot_name :
            xmin = 0
            xmax = 101
            ymin = 0.
            ymax = 7 # in units of ke 

            graph.GetXaxis().SetRangeUser(xmin, xmax)
            graph.GetYaxis().SetRangeUser(ymin, ymax)

            graph.GetXaxis().SetTitleOffset(1.25)
            graph.GetXaxis().SetTitle("Bias Voltage [V]")

            graph.GetYaxis().SetTitleOffset(1.4)
            graph.GetYaxis().SetTitle("MPV Charge [ke]")

        graphs.append(graph)

        ps.c.cd()
        graph.Draw("AP" if is0deg else "P")
        ps.update_canvas()

    if "Efficiency" in plot_name :
        leg = ROOT.gPad.BuildLegend(0.35, 0.3, 0.9, 0.45)
        leg.SetBorderSize(0)
    elif "Landau" in plot_name :
        leg = ROOT.gPad.BuildLegend(0.15, 0.79, 0.7, 0.94)
        leg.SetBorderSize(0)

    ps.update_canvas()
    ps.save(plot_name)

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
