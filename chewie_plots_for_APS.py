from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0o0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning

filepath = sys.argv[1]
filename = filepath.split("/")[-1]

# to save our plots
#ps = plot_saver(plot_dir("Spring2020/"+filename.split(".")[0]), size=(600,600), log=False, pdf=False)
ps = plot_saver(plot_dir(filename.split(".")[0]+"_forAPS"), size=(600,600), log=False, pdf=True)

# the ROOT file
f = ROOT.TFile(filepath)

# histogram paths within the ROOT file
plot_paths = []
plot_paths.append("Efficiency/Dut0/Efficiency/Efficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyRef_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRef_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNorm_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefRebinned_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormRebinned_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefZoomedIn_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormZoomedIn_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefZoomedIn50x50_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormZoomedIn50x50_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefZoomedIn25x100_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormZoomedIn25x100_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiencyRef_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiencyNorm_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiencyRefNorm_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/h2D4cellEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/h2D4cellEfficiencyRef_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize2_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize2_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualCalculatedSize2_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualCalculatedSize2_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsDigital_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsDigital_Dut0")
plot_paths.append("Resolution/Dut0/Errors/hPredictedXErrors_Dut0")
plot_paths.append("Resolution/Dut0/Errors/hPredictedYErrors_Dut0")
plot_paths.append("Charge/Dut0/ClusterSize/hClusterSize_Dut0")
plot_paths.append("Charge/Dut0/Landau/hCellLandau_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSizeUpTo4_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSizeUpToMax_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize1_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize2_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize3_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize4_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize5_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize6_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize7_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize8_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize9_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DCharge_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRef_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefRebinned_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefZoomedIn_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefZoomedIn50x50_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefZoomedIn25x100_Dut0")
plot_paths.append("Charge/Dut0/2DCellCharge/h2DCellCharge_Dut0")
plot_paths.append("Charge/Dut0/2DCellCharge/h2DCellChargeSize1_Dut0")
plot_paths.append("Charge/Dut0/2DCellCharge/h2DCellChargeSize2_Dut0")
plot_paths.append("Charge/Dut0/2DCellCharge/h2DClusterSize_Dut0")
plot_paths.append("Charge/Dut0/XAsymmetry/h1DXcellChargeAsymmetryInv_Dut0")
plot_paths.append("Charge/Dut0/YAsymmetry/h1DYcellChargeAsymmetryInv_Dut0")

# Telescope residuals
plot_paths.append("Resolution/Strip_Telescope_Upstream0/XResiduals/hXResiduals_Strip_Telescope_Upstream0")
plot_paths.append("Resolution/Strip_Telescope_Upstream0/YResiduals/hYResiduals_Strip_Telescope_Upstream0")
plot_paths.append("Resolution/Strip_Telescope_Upstream1/XResiduals/hXResiduals_Strip_Telescope_Upstream1")
plot_paths.append("Resolution/Strip_Telescope_Upstream1/YResiduals/hYResiduals_Strip_Telescope_Upstream1")
plot_paths.append("Resolution/Strip_Telescope_Upstream2/XResiduals/hXResiduals_Strip_Telescope_Upstream2")
plot_paths.append("Resolution/Strip_Telescope_Upstream2/YResiduals/hYResiduals_Strip_Telescope_Upstream2")
plot_paths.append("Resolution/Strip_Telescope_Upstream3/XResiduals/hXResiduals_Strip_Telescope_Upstream3")
plot_paths.append("Resolution/Strip_Telescope_Upstream3/YResiduals/hYResiduals_Strip_Telescope_Upstream3")
plot_paths.append("Resolution/Strip_Telescope_Upstream4/XResiduals/hXResiduals_Strip_Telescope_Upstream4")
plot_paths.append("Resolution/Strip_Telescope_Upstream4/YResiduals/hYResiduals_Strip_Telescope_Upstream4")
plot_paths.append("Resolution/Strip_Telescope_Upstream5/XResiduals/hXResiduals_Strip_Telescope_Upstream5")
plot_paths.append("Resolution/Strip_Telescope_Upstream5/YResiduals/hYResiduals_Strip_Telescope_Upstream5")
plot_paths.append("Resolution/Strip_Telescope_Upstream6/XResiduals/hXResiduals_Strip_Telescope_Upstream6")
plot_paths.append("Resolution/Strip_Telescope_Upstream6/YResiduals/hYResiduals_Strip_Telescope_Upstream6")
plot_paths.append("Resolution/Strip_Telescope_Upstream7/XResiduals/hXResiduals_Strip_Telescope_Upstream7")
plot_paths.append("Resolution/Strip_Telescope_Upstream7/YResiduals/hYResiduals_Strip_Telescope_Upstream7")
plot_paths.append("Resolution/Telescope_Downstream0/XResiduals/hXResiduals_Telescope_Downstream0")
plot_paths.append("Resolution/Telescope_Downstream0/YResiduals/hYResiduals_Telescope_Downstream0")
plot_paths.append("Resolution/Telescope_Downstream1/XResiduals/hXResiduals_Telescope_Downstream1")
plot_paths.append("Resolution/Telescope_Downstream1/YResiduals/hYResiduals_Telescope_Downstream1")
plot_paths.append("Resolution/Telescope_Downstream2/XResiduals/hXResiduals_Telescope_Downstream2")
plot_paths.append("Resolution/Telescope_Downstream2/YResiduals/hYResiduals_Telescope_Downstream2")
plot_paths.append("Resolution/Telescope_Downstream3/XResiduals/hXResiduals_Telescope_Downstream3")
plot_paths.append("Resolution/Telescope_Downstream3/YResiduals/hYResiduals_Telescope_Downstream3")
plot_paths.append("Resolution/Strip_Telescope_Downstream0/XResiduals/hXResiduals_Strip_Telescope_Downstream0")
plot_paths.append("Resolution/Strip_Telescope_Downstream0/YResiduals/hYResiduals_Strip_Telescope_Downstream0")
plot_paths.append("Resolution/Strip_Telescope_Downstream1/XResiduals/hXResiduals_Strip_Telescope_Downstream1")
plot_paths.append("Resolution/Strip_Telescope_Downstream1/YResiduals/hYResiduals_Strip_Telescope_Downstream1")
plot_paths.append("Resolution/Strip_Telescope_Downstream2/XResiduals/hXResiduals_Strip_Telescope_Downstream2")
plot_paths.append("Resolution/Strip_Telescope_Downstream2/YResiduals/hYResiduals_Strip_Telescope_Downstream2")
plot_paths.append("Resolution/Strip_Telescope_Downstream3/XResiduals/hXResiduals_Strip_Telescope_Downstream3")
plot_paths.append("Resolution/Strip_Telescope_Downstream3/YResiduals/hYResiduals_Strip_Telescope_Downstream3")
plot_paths.append("Resolution/Strip_Telescope_Downstream4/XResiduals/hXResiduals_Strip_Telescope_Downstream4")
plot_paths.append("Resolution/Strip_Telescope_Downstream4/YResiduals/hYResiduals_Strip_Telescope_Downstream4")
plot_paths.append("Resolution/Strip_Telescope_Downstream5/XResiduals/hXResiduals_Strip_Telescope_Downstream5")
plot_paths.append("Resolution/Strip_Telescope_Downstream5/YResiduals/hYResiduals_Strip_Telescope_Downstream5")
plot_paths.append("Resolution/Strip_Telescope_Downstream6/XResiduals/hXResiduals_Strip_Telescope_Downstream6")
plot_paths.append("Resolution/Strip_Telescope_Downstream6/YResiduals/hYResiduals_Strip_Telescope_Downstream6")
plot_paths.append("Resolution/Strip_Telescope_Downstream7/XResiduals/hXResiduals_Strip_Telescope_Downstream7")
plot_paths.append("Resolution/Strip_Telescope_Downstream7/YResiduals/hYResiduals_Strip_Telescope_Downstream7")

for plot_path in plot_paths :
    h = f.Get(plot_path)
    if not h : 
        print("%s not found, skipping" % plot_path)
        continue
    plot_name = plot_path.split("/")[-1]

    if "2DCharge" in plot_name or "2DCellCharge" in plot_name :
        h.SetMaximum(15000) # I think this was for MJ13, where 5k electrons really was a sensible maximum...
        pass
    elif "h2DClusterSize_Dut0" in plot_name :
        h.SetMinimum(1)
        h.SetMaximum(2)
    elif ("CellEfficiency" in plot_name or "2DEfficiency" in plot_name) and not "Norm" in plot_name :
        h.SetMinimum(0)
        h.SetMaximum(1)

    # Plot TH2's with colz and no stat box
    if issubclass(type(h), ROOT.TH2) :
        ps.c.SetMargin(0.12,0.14,0.12,0.10)
        if not "Zoomed" in plot_name :
            h.GetYaxis().SetTitleOffset(1.5)
        h.SetStats(0)
        h.Draw("colz")
    else :
        ps.c.SetMargin(0.1,0.1,0.1,0.1)

        # draw charge distributions with their Landau x Gaussian fits
        if "Landau" in plot_name and h.GetEntries() > 0 :
            h.GetXaxis().SetRangeUser(1000,25000)
            langaus = ROOT.langausFit(h)
            fit = h.Fit(langaus, "RBLSQ", "", 8000, 20000)
            #h.GetXaxis().SetRangeUser(0, 25000)
            h.Draw()
        elif "Predicted" in plot_name and "Errors" in plot_name :
            h.GetXaxis().SetRangeUser(3, 6)
            h.Draw()
        elif "ResidualsClusterSize1" in plot_name and h.GetEntries() > 0 :
            h.Scale(1./h.Integral())
            gauspol0 = ROOT.fitGausPol0(h)
            h.SetStats(0)
            h.SetTitle("Data (RMS = %.1f #mum)" % round(h.GetStdDev(),1))
            h.SetLineWidth(2)
            h.SetLineColor(ROOT.kBlack)
            h.Draw()
            h.GetXaxis().SetRangeUser(-50,50)
            if "X" in h.GetName() :
                h.GetXaxis().SetTitle("y residual (#mum), telescope coordinates")
            else :
                h.GetXaxis().SetTitle("x residual (#mum), telescope coordinates")
            h.GetYaxis().SetTitle("a.u.")
            ps.c.SetMargin(0.13,0.1,0.1,0.1)
            h.GetYaxis().SetTitleOffset(1.9)
            leg = ps.c.BuildLegend(0.65,0.80,0.9,0.9)
        #elif ("ResidualsClusterSize2" in plot_name or "ResidualCalculatedSize2" in plot_name or "Digital" in plot_name) and h.GetEntries() > 0 :
        elif ("Residuals" in plot_name) and h.GetEntries() > 0 :
            h.Scale(1./h.Integral())
            gauspol0 = ROOT.fitGausPol0(h)
            fit = h.Fit(gauspol0, "RBLSQ","",-30,30)
            fithist = h.GetFunction("gauspol0")
            sigma = fit.Parameter(2)
            h.SetStats(0)
            h.SetTitle("Data")
            h.SetLineWidth(2)
            h.SetLineColor(ROOT.kBlack)
            h.Draw()
            h.GetXaxis().SetRangeUser(-50,50)
            #h.GetXaxis().SetRangeUser(-25,25) # FIXME!!
            if "X" in h.GetName() :
                h.GetXaxis().SetTitle("y residual (#mum), telescope coordinates")
            else :
                h.GetXaxis().SetTitle("x residual (#mum), telescope coordinates")
            h.GetYaxis().SetTitle("a.u.")
            h.GetYaxis().SetTitleOffset(1.5)
            leg = ps.c.BuildLegend(0.6,0.7,0.9,0.9)
            leg.AddEntry(fithist, "Fit (#sigma = %.1f #mum)" % round(sigma,1), "l")
        elif "ChargeAsymmetryInv" in plot_name and h.GetEntries() > 0 :
            fit = h.Fit("pol1", "RQS", "", -0.5, 0.5)
            slope = fit.Parameter(1)
            fithist = h.GetFunction("pol1")
            ROOT.gStyle.SetStatH(0.1)
            h.SetLineWidth(2)
            h.SetLineColor(ROOT.kBlack)
            h.SetMarkerColor(ROOT.kBlack)
            h.Draw()
            h.SetStats(0)
            h.SetTitle("Data")
            h.GetYaxis().SetRangeUser(-20,20)
            h.GetYaxis().SetTitle("Distance from midpoint (#mum)")
            h.GetYaxis().SetTitleOffset(1.2)
            leg = ps.c.BuildLegend(0.5,0.7,0.9,0.9)
            leg.AddEntry(fithist, "Fit (slope = %.1f #mum)" % round(slope,1), "l")
        elif plot_name == "Efficiency_Dut0" or plot_name == "EfficiencyRef_Dut0" :
            h.GetYaxis().SetRangeUser(0,2)
            h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))
            nevents = h_norm.GetBinContent(1)
            eff = h.GetBinContent(1)

            # then draw it as text on the canvas
            abs_err_down, abs_err_up = clopper_pearson_abs_err(nevents, eff)
            eff_text      = ROOT.TText(0.84, 1.0,  "{eff:.4f}%".format(eff=eff*100))
            err_up_text   = ROOT.TText(1.086, 1.06, "+{err:.4f}%".format(err=abs_err_up*100))
            err_down_text = ROOT.TText(1.1, 0.96, "-{err:.4f}%".format(err=abs_err_down*100))
            h.Draw("AXIS")
            eff_text.Draw("same")
            err_up_text.Draw("same")
            err_down_text.Draw("same")
        else :
            h.Draw()

    ps.save(plot_name)

    if ("CellEfficiency" in plot_name or "cellEfficiency" in plot_name) and not "Norm" in plot_name :
        ps.c.Clear()
        hclone = h.Clone(plot_name+"_smallerRange")
        hclone.SetMinimum(0.92)
        hclone.SetMaximum(1.0)

        if "4cell" in plot_name :
            hclone.GetXaxis().SetRangeUser(-50,50)
        else :
            hclone.GetXaxis().SetRangeUser(-25,25)
            hclone.GetYaxis().SetRangeUser(-25,25)
        hclone.GetXaxis().SetTitle("x position in pixel cell (#mum)")
        hclone.GetYaxis().SetTitle("y position in pixel cell (#mum)")
        # short pitch is the one we rotate into, which is the telescope x

        hclone.Draw("colz")
        ps.save(plot_name+"_smallerRange")

        h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))
        h_num = hclone
        h_num.Multiply(h_norm)
        h_norm.Rebin2D(2,2)
        h_num.Rebin2D(2,2)

        h_eff_rebinned = h_num
        h_eff_rebinned.Divide(h_norm)
        h_eff_rebinned.SetMinimum(0.92)
        if "4cell" in plot_name :
            h_eff_rebinned.GetXaxis().SetRangeUser(-50,50)
        else :
            h_eff_rebinned.GetXaxis().SetRangeUser(-25,25)
            h_eff_rebinned.GetYaxis().SetRangeUser(-25,25)
        h_eff_rebinned.Draw("colz")
        ps.save(plot_name+"_smallerRange_rebinned")


printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
