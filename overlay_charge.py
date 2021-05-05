from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")

ps = plot_saver(plot_dir("overlay_charge"), size=(600,600), log=True, pdf=True, pdf_log=True)
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
              ,"hLandauClusterSize2_Dut0"
             ]

for plot_name in plot_names :


    fpath193 = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs31975_32138/"+plot_name+".root"
    #fpath194 = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs31681_31691/"+plot_name+".root"
    fpath194 = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs31681_32662/"+plot_name+".root"

    files = [ ROOT.TFile(fpath193)
             ,ROOT.TFile(fpath194)
            ]

    labels = ["193 (25x100)","194 (50x50)"]

    colors = [ROOT.kRed,ROOT.kBlue]
    hists = []

    if "Landau" in plot_name :
        leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    else :
        leg = ROOT.TLegend(0.50, 0.60, 0.90, 0.90)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        h.SetName(labels[index])
        h.SetLineColor(colors[index])
        h.SetMarkerColor(colors[index])
        h.SetLineWidth(1)
        if plot_name == "hClusterSize_Dut0" :
            h.SetLineWidth(2)
        h.Rebin(5)
        h.Scale(1/h.Integral())
        drawopt = ""

        if "Landau" in plot_name and h.GetEntries() > 0 :
            langaus = ROOT.langausFit(h)
            fit = h.Fit(langaus, "RBLSQ", "", 9000, 25000)
            #fit = h.Fit(langaus, "RBLSQ")
            h.GetFunction("langaus").SetLineColor(colors[index]+1)
            h.GetXaxis().SetRangeUser(0, 30000)
            #drawopt += "HIST"

        ps.c.cd()
        if index == 0 :
            h.Draw(drawopt)
            h.GetYaxis().SetRangeUser(0.001,1)
            h.GetYaxis().SetTitle("a.u.")
            h.GetYaxis().SetTitleOffset(2.0)
        else :
            h.Draw(drawopt+" same")

        #leg.AddEntry(h,h.GetName()+", mean = %.2f #pm %.2f, #sigma = %.2f #pm %.2f" % (h.GetMean(), h.GetMeanError(), h.GetStdDev(), h.GetStdDevError()),"l")
        if "Landau" in plot_name :
            leg.AddEntry(h,h.GetName()+", MPV = %.1f ke" % round(fit.Parameter(1)/1000, 1),"l")
        elif plot_name == "hClusterSize_Dut0" :
            leg.AddEntry(h,h.GetName()+", mean = %.2f" % (h.GetMean()),"l")
        else :
            leg.AddEntry(h,h.GetName()+", mean = %.2f, #sigma = %.2f" % (h.GetMean(), h.GetStdDev()),"l")
        h.SetStats(0)
        hists.append(h)
        ps.update_canvas()

    if plot_name == "hClusterSize_Dut0" :
        histmin = 5e-6
        histmax = 1
        hists[0].GetYaxis().SetTitle("fraction")
    elif "ResidualsClusterSize2" in plot_name :
        histmin = 1e-5
        histmax = 0.06
    elif "Residuals" in plot_name :
        histmin = 5e-6
        histmax = 0.04
    elif "LandauClusterSize2" in plot_name :
        histmin = 5e-6
        histmax = 0.015*5
    elif "Landau" in plot_name :
        histmin = 5e-6
        histmax = 0.027*5

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
