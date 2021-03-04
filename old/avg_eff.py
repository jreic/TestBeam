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
plot_paths.append("Efficiency/Dut0/Efficiency/Efficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyRef_Dut0")

plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyNorm_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyRefNorm_Dut0")

# Corrinne convinced me that these aren't actually necessary, 
# and it was more difficult to interpret an efficiency whenever
# empty bins were present!
#plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiency_Dut0")
#plot_paths.append("Efficiency/Dut0/CellEfficiency/hCellEfficiencyRef_Dut0")

eff_arr = []

for plot_path in plot_paths :
    h = f.Get(plot_path)
    plot_name = plot_path.split("/")[-1]

    #if plot_name == "hCellEfficiencyRef_Dut0" or plot_name == "hCellEfficiency_Dut0" :
    #    num = 0
    #    den = 0
    #    for ibinx in xrange(0,h.GetNbinsX()+2) :
    #        for ibiny in xrange(0, h.GetNbinsY()+2) :

    #            xbinlowedge = h.GetXaxis().GetBinLowEdge(ibinx)
    #            ybinlowedge = h.GetYaxis().GetBinLowEdge(ibiny)

    #            # FIXME note this is only valid for 50x50 sensors
    #            if xbinlowedge < -25 or xbinlowedge >= 25 or ybinlowedge < -25 or ybinlowedge >= 25 :
    #                continue

    #            num += h.GetBinContent(ibinx,ibiny)
    #            den += 1

    #    if den == 0 : den = 1
    #    eff = "%.2f" % (num/den)
    #    print("Integrated " + plot_name + " efficiency is " + eff)

    if plot_name == "Efficiency_Dut0" or plot_name == "EfficiencyRef_Dut0" :
        eff = "%.2f" % h.GetBinContent(1)
        print(plot_name + " efficiency is " + eff)
    if plot_name == "EfficiencyNorm_Dut0" or plot_name == "EfficiencyRefNorm_Dut0" :
        eff = "%.2f" % h.GetBinContent(1)
        print(plot_name + " nTracks is " + eff)

    eff_arr.append(eff)

# assumes the order to be put on the Twiki is the same as the plot_paths appends were made
table_str = "|"
for eff in eff_arr :
    table_str += " " + eff + " |"
print table_str
