from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_angle_scan"), size=(600,600), log=True, pdf=True, pdf_log=True)
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
             ]

for plot_name in plot_names :

    fpath30deg = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16779_16798/"+plot_name+".root"
    fpath45deg = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16803_16835/"+plot_name+".root"
    fpath60deg = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16756_16778/"+plot_name+".root"
    fpath85deg = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16738_16755/"+plot_name+".root"

    files = [ ROOT.TFile(fpath30deg)
             ,ROOT.TFile(fpath45deg)
             ,ROOT.TFile(fpath60deg)
             ,ROOT.TFile(fpath85deg)
            ]

    #labels = ["30#circ","45#circ","60#circ","85#circ"]
    labels = ["27#circ","42#circ","50#circ","76#circ"] # Monicelli tells us these
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
    hists = []

    leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    #leg = ROOT.TLegend(0.50, 0.75, 0.90, 0.90)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        h.SetName(labels[index])
        h.SetLineColor(colors[index])
        h.SetMarkerColor(colors[index])
        h.SetLineWidth(2)
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

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
