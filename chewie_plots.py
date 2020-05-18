from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gROOT.ProcessLine(".L langaus_from_chewie.C+")

filepath = sys.argv[1]
filename = filepath.split("/")[-1]

# to save our plots
ps = plot_saver(plot_dir(filename.split(".")[0]), size=(600,600), log=False, pdf=True)

# the ROOT file
f = ROOT.TFile(filepath)

# histogram paths within the ROOT file
plot_paths = []
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRef_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNorm_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefRebinned_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormRebinned_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefZoomedIn_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/2DEfficiencyRefNormZoomedIn_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiencyRef_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/h2D4cellEfficiency_Dut0")
plot_paths.append("Efficiency/Dut0/CellEfficiency/h2D4cellEfficiencyRef_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize2_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize2_Dut0")
plot_paths.append("Charge/Dut0/ClusterSize/hClusterSize_Dut0")
plot_paths.append("Charge/Dut0/Landau/hCellLandau_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSizeUpTo4_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize1_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize2_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DCharge_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRef_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefRebinned_Dut0")
plot_paths.append("Charge/Dut0/2DCharge/h2DChargeRefZoomedIn_Dut0")
plot_paths.append("Charge/Dut0/2DCellCharge/h2DCellCharge_Dut0")

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

    if "2DCharge" in plot_name :
        h.SetMaximum(5000)
    elif "2DCellCharge" in plot_name :
        h.SetMaximum(5000)
    elif "CellEfficiency" in plot_name or ("2DEfficiency" in plot_name and not "Norm" in plot_name) :
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
        if "Landau" in plot_name :
            fit = ROOT.langausFit(h)
            h.GetXaxis().SetRangeUser(0, 25000)
            h.Draw()
            fit.Draw("same")
        else :
            h.Draw()

    ps.save(plot_name)

    if "CellEfficiency" in plot_name or "cellEfficiency" in plot_name :
        ps.c.Clear()
        hclone = h.Clone(plot_name+"_smallerRange")
        hclone.SetMinimum(0.8)
        hclone.SetMaximum(1.0)
        hclone.Draw("colz")
        ps.save(plot_name+"_smallerRange")
