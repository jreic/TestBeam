from ROOTTools import *
import sys

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box

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
plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiency_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")
plot_paths.append("Charge/Dut0/ClusterSize/hClusterSize_Dut0")
plot_paths.append("Charge/Dut0/Landau/hCellLandau_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize1_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize2_Dut0")

# Telescope residuals
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

for plot_path in plot_paths :
    h = f.Get(plot_path)
    plot_name = plot_path.split("/")[-1]

    if plot_name == "hCellEfficiency_Dut0" :
        num = 0
        den = 0
        for ibinx in xrange(0,h.GetNbinsX()+2) :
            for ibiny in xrange(0, h.GetNbinsY()+2) :
                val = h.GetBinContent(ibinx,ibiny)
                err = h.GetBinError(ibinx, ibiny)

                if val != 0 :
                    num += val
                    den += 1

        print("Integrated efficiency is "+str(num/den))

    if "Landau" in plot_name :
        h.Fit("landau","","",2800,50000) # maybe 2800 is too large to start??
        h.GetXaxis().SetRangeUser(0,25000)
        #h.GetXaxis().SetNdivisions(505)

    # Plot TH2's with colz and no stat box
    if issubclass(type(h), ROOT.TH2) :
        h.SetStats(0)
        h.Draw("colz")
    else :
        h.Draw()

    ps.save(plot_name)
