from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_partial_bias_scan_March2021_MJ127"), size=(600,600), log=True, pdf=True, pdf_log=True)
ps.c.SetLeftMargin(0.15)
ps.update_canvas()

plot_names = [ 
               "hClusterSize_Dut0"
              ,"hXResiduals_Dut0"
              ,"hYResiduals_Dut0"
              ,"hXResidualsClusterSize1_Dut0"
              ,"hYResidualsClusterSize1_Dut0"
              ,"hXResidualsClusterSize2_Dut0"
              ,"hYResidualsClusterSize2_Dut0"
              ,"hLandauClusterSizeUpToMax_Dut0"
              ,"hLandauClusterSize1_Dut0"
             ]

for plot_name in plot_names :

    fpath80V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35586_35590/"+plot_name+".root"
    fpath60V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35592_35598/"+plot_name+".root"
    fpath40V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35599_35601/"+plot_name+".root"
    fpath20V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35602_35605/"+plot_name+".root"
    fpath15V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35607_35610/"+plot_name+".root"
    fpath10V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35611_35613/"+plot_name+".root"
    fpath5V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35614_35617/"+plot_name+".root"
    fpath0V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs35618_35620/"+plot_name+".root"

    #files = [ ROOT.TFile(fpath80V)
    #         ,ROOT.TFile(fpath60V)
    #         ,ROOT.TFile(fpath40V)
    #         ,ROOT.TFile(fpath20V)
    #         ,ROOT.TFile(fpath15V)
    #         ,ROOT.TFile(fpath10V)
    #         ,ROOT.TFile(fpath5V)
    #         ,ROOT.TFile(fpath0V)
    #        ]

    #labels = ["80V","60V","40V","20V","15V","10V","5V","0V"]

    files = [ ROOT.TFile(fpath0V)
             ,ROOT.TFile(fpath5V)
             ,ROOT.TFile(fpath10V)
             ,ROOT.TFile(fpath15V)
             ,ROOT.TFile(fpath20V)
             ,ROOT.TFile(fpath40V)
             ,ROOT.TFile(fpath60V)
             ,ROOT.TFile(fpath80V)
            ]

    labels = ["0V","5V","10V","15V","20V","40V","60V","80V"]

    colors = [ROOT.kRed,ROOT.kOrange+1,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4,ROOT.kOrange,ROOT.kRed-2,ROOT.kBlue-2,ROOT.kSpring+4,ROOT.kGray+2,ROOT.kViolet+2, ROOT.kPink+1]
    hists = []

    #leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    leg = ROOT.TLegend(0.50, 0.60, 0.90, 0.90)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        h.SetName(labels[index])
        h.SetLineColor(colors[index])
        h.SetMarkerColor(colors[index])
        h.SetLineWidth(2)
        if labels[index] == "0V" or labels[index] == "5V" :
            h.SetLineWidth(1)
        h.Scale(1/h.Integral())

        ps.c.cd()
        if index == 0 :
            h.Draw()
            h.GetYaxis().SetRangeUser(0.001,1)
            h.GetYaxis().SetTitle("fraction / bin")
            h.GetYaxis().SetTitleOffset(2.0)
        else :
            h.Draw("same")

        #leg.AddEntry(h,h.GetName()+", mean = %.2f #pm %.2f, #sigma = %.2f #pm %.2f" % (h.GetMean(), h.GetMeanError(), h.GetStdDev(), h.GetStdDevError()),"l")
        leg.AddEntry(h,h.GetName()+", mean = %.2f, #sigma = %.2f" % (h.GetMean(), h.GetStdDev()),"l")
        h.SetStats(0)
        hists.append(h)
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
    elif "Landau" in plot_name :
        histmin = 5e-6
        histmax = 0.10

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
