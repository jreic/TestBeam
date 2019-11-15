from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_bias_scan"), size=(600,600), log=True, pdf=True, pdf_log=True)
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

    fpath800V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs15737_15748_contiguous/"+plot_name+".root"
    fpath700V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16466_16476/"+plot_name+".root"
    fpath600V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16434_16445/"+plot_name+".root"
    fpath500V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16446_16455/"+plot_name+".root"
    fpath400V = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs16477_16494/"+plot_name+".root"

    files = [ ROOT.TFile(fpath800V)
             ,ROOT.TFile(fpath700V)
             ,ROOT.TFile(fpath600V)
             ,ROOT.TFile(fpath500V)
             ,ROOT.TFile(fpath400V)
            ]

    labels = ["800V","700V","600V","500V","400V"]
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange]
    hists = []

    leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
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

        leg.AddEntry(h,h.GetName()+", mean = %.2f, #sigma = %.2f" % (h.GetMean(), h.GetStdDev()),"l")
        h.SetStats(0)
        hists.append(h)
        ps.update_canvas()

    if plot_name == "hClusterSize_Dut0" :
        histmin = 5e-6
        histmax = 1
    elif "ResidualsClusterSize2" in plot_name :
        histmin = 1e-5
        histmax = 0.05
    elif "Residuals" in plot_name :
        histmin = 5e-6
        histmax = 0.03

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
