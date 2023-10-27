from ROOTTools import *
import sys,math

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box


ps = plot_saver(plot_dir("overlay_angle_scan_eff_and_resolution_MJ531_Nov2021"), size=(600,600), log=False, pdf=True)
ps.c.SetLeftMargin(0.15)
ps.update_canvas()

plot_names = [ 
               "EfficiencyRef_Dut0",
               "Efficiency_Dut0",
               "hXResiduals_Dut0",
               "hYResiduals_Dut0",
             ]


for plot_name in plot_names :

    fpath0deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46657_46667/"+plot_name+".root"
    fpath4deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46668_46675/"+plot_name+".root"
    fpath8deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46676_46682/"+plot_name+".root"
    fpath10deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46683_46690/"+plot_name+".root"
    fpath12deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46691_46697/"+plot_name+".root"
    fpath16deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46698_46704/"+plot_name+".root"
    fpath20deg  = "/uscms/home/joeyr/publicweb/TFPX/Chewie_Runs46705_46711/"+plot_name+".root"

    files = [ ROOT.TFile(fpath0deg)
            , ROOT.TFile(fpath4deg)
            , ROOT.TFile(fpath8deg)
            , ROOT.TFile(fpath10deg)
            , ROOT.TFile(fpath12deg)
            , ROOT.TFile(fpath16deg)
            , ROOT.TFile(fpath20deg)
            ]

    labels = [0, 4, 8, 10, 12, 16, 20]

    hists = []

    outhist = ROOT.TH1F(plot_name, plot_name, (int(max(labels)))+1, int(min(labels)), int(max(labels))+1)

    leg = ROOT.TLegend(0.50, 0.60, 0.90, 0.90)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)

        if "Eff" in plot_name :
            eff = h.GetBinContent(1)
            err = h.GetBinError(1)
            if eff == 0 : eff = 1e-5
            outhist.SetBinContent(outhist.FindBin(labels[index]), eff)
            outhist.SetBinError(outhist.FindBin(labels[index]), err)
        elif "Residuals" in plot_name :
            residual = h.GetStdDev()
            err = h.GetStdDevError()

            # Subtract off the telescope resolution!
            # Took telescope resolution from https://home.fnal.gov/~joeyr/TFPX/Chewie_Runs46657_46667/#hPredictedXErrors_Dut0. This is from the normal incidence data, i.e. it is the minimum of its resolution across the run blocks considered, which means we are not subtracting enough for the large angles. However, it only varies by a few percent overall, so not a huge deal.
            # Also note telescope X is DUT Y, and telescope Y is DUT X, and I am taking the mean value over the predicted errors distribution
            
            if "XResiduals" in plot_name :
                residual = math.sqrt( residual**2 - 3.884**2 )
            elif "YResiduals" in plot_name :
                residual = math.sqrt( residual**2 - 4.289**2 )

            outhist.SetBinContent(outhist.FindBin(labels[index]), residual)
            outhist.SetBinError(outhist.FindBin(labels[index]), err)
        else :
            print "did not implement this histogram!!"

        ps.c.cd()
        ps.update_canvas()

    if plot_name == "hClusterSize_Dut0" :
        histmin = 5e-6
        histmax = 1
    elif "ResidualsClusterSize2" in plot_name :
        histmin = 1e-5
        histmax = 0.06
    elif "Residuals" in plot_name :
        histmin = 0
        histmax = 30
        outhist.GetYaxis().SetTitle("residual (um)")
    elif "Efficiency" in plot_name :
        histmin = 0.
        histmax = 1.0001
        outhist.GetYaxis().SetTitle("efficiency")

    outhist.GetYaxis().SetRangeUser(histmin, histmax)
    outhist.GetYaxis().SetTitleOffset(2.0)
    outhist.GetXaxis().SetTitle("incident angle (#circ)")
    outhist.SetLineColor(ROOT.kBlack)
    outhist.SetMarkerColor(ROOT.kBlack)
    outhist.SetMarkerStyle(20)
    outhist.Draw("pE1")
    outhist.SetStats(0)
    #leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
