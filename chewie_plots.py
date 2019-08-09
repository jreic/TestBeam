from ROOTTools import *
import sys

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
plot_paths.append("Charge/Dut0/ClusterSize/hClusterSize_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")

for plot_path in plot_paths :
    h = f.Get(plot_path)
    plot_name = plot_path.split("/")[-1]

    # Plot TH2's with colz and no stat box
    if issubclass(type(h), ROOT.TH2) :
        h.SetStats(0)
        h.Draw("colz")
    else :
        h.Draw()

    ps.save(plot_name)
