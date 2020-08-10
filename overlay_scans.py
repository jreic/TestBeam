from ROOTTools import *
import sys
from block_dict import blocks

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box

sensor=sys.argv[1]
filter_str = None

is_angle_scan = True

# MJ135 was our temperature scan
if sensor == "135" : 
    is_angle_scan = False 

# to filter subsets out to avoid overcrowding
if len(sys.argv) > 2 :
    filter_str = sys.argv[2]

plot_dir_name = "Spring2020_TFPX_Results/scans/MJ%s_scan" % sensor

if filter_str : 
    angle_strs = ["A", "B", "C", "D", "E", "F", "G"]
    LKC_strs = ["K", "L", "M"]
    if filter_str in angle_strs :
        plot_dir_name += "_angle%s" % filter_str
        is_angle_scan = False
    elif filter_str in LKC_strs :
        plot_dir_name += "_LKC_%s" % filter_str

ps = plot_saver(plot_dir(plot_dir_name), size=(600,600), log=True, pdf=True, pdf_log=True)
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
              ,"hLandauClusterSize1_Dut0"
              ,"hLandauClusterSize2_Dut0"
              ,"hLandauClusterSize3_Dut0"
              ,"Efficiency_Dut0"
              ,"EfficiencyRef_Dut0"
             ]

for plot_name in plot_names :

    basepath = "~/public_html/TFPX/Spring2020_TFPX_Results/"

    files = []
    labels = []
    colors = []

    for key in sorted(blocks.keys()) :
        if sensor in key :

            if filter_str and filter_str not in key : continue

            fpath = basepath+blocks[key]+"/"+plot_name+".root"
            files.append(ROOT.TFile(fpath))

            label = ""

            if sensor == "135" : # temperature scan
                if   "A" in key : 
                    label += "13#circC"
                    color = ROOT.kBlack
                elif "H" in key : 
                    label += "5#circC"
                    color = ROOT.kRed
                elif "I" in key : 
                    label += "0#circC"
                    color = ROOT.kBlue
                elif "J" in key : 
                    label += "-5#circC"
                    color = ROOT.kGreen+2

            elif not is_angle_scan : # LKC scan
                if   "K" in key : 
                    label += "LKC20"
                    color = ROOT.kBlue
                elif "L" in key : 
                    label += "LKC27"
                    color = ROOT.kRed
                elif "M" in key : 
                    label += "LKC40"
                    color = ROOT.kBlack

            else : # angle scan
                if   "A" in key : 
                    label += "0#circ"
                    color = ROOT.kBlack
                elif "B" in key : 
                    label += "5#circ"
                    color = ROOT.kRed
                elif "C" in key : 
                    label += "10#circ"
                    color = ROOT.kBlue
                elif "D" in key : 
                    label += "15#circ"
                    color = ROOT.kGreen+2
                elif "E" in key : 
                    label += "20#circ"
                    color = ROOT.kViolet-3
                elif "F" in key : 
                    label += "24#circ"
                    color = ROOT.kOrange-6
                elif "G" in key : 
                    label += "29#circ"
                    color = ROOT.kCyan+1
                else : 
                    sys.exit("invalid key!")

            # for multiple blocks w/ same conditions
            if   key.endswith("1") : 
                label += " #1"
            elif key.endswith("2") : 
                label += " #2"
                color += 10 # FIXME this is completely arbitrary

            labels.append(label)
            colors.append(color)

    hists = []

    if not "Efficiency" in plot_name :
        leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    else :
        leg = ROOT.TLegend(0.50, 0.25, 0.85, 0.40)
    leg.SetMargin(0.15)

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        h.SetName(labels[index])
        h.SetLineColor(colors[index])
        h.SetMarkerColor(colors[index])
        h.SetLineWidth(2)
        if not "Efficiency" in plot_name :
            den = h.Integral()
            if den == 0 : den = 1.
            h.Scale(1/den)

        ps.c.cd()
        if index == 0 :
            h.Draw()
            h.GetYaxis().SetRangeUser(0.001,1)
            if "Efficiency" in plot_name : 
                h.GetYaxis().SetTitle("efficiency")
            else :
                h.GetYaxis().SetTitle("fraction / bin")
            h.GetYaxis().SetTitleOffset(2.0)
        else :
            h.Draw("same")

        if not "Efficiency" in plot_name :
            leg.AddEntry(h,h.GetName()+", mean = %.2f, #sigma = %.2f" % (h.GetMean(), h.GetStdDev()),"l")
        else :
            leg.AddEntry(h,h.GetName()+", eff = %.6f" % h.GetBinContent(1),"l")
        h.SetStats(0)
        hists.append(h)
        ps.update_canvas()

    if plot_name == "hClusterSize_Dut0" :
        histmin = 5e-6
        histmax = 1
    elif "ResidualsClusterSize2" in plot_name :
        histmin = 1e-5
        histmax = 0.08
    elif "Residuals" in plot_name :
        histmin = 5e-6
        histmax = 0.06
    elif "Landau" in plot_name :
        histmin = 1e-5
        histmax = 0.025
    elif "Efficiency" in plot_name :
        histmin = 0.8
        histmax = 1

    hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    leg.Draw()
    ps.update_canvas()
    ps.save(plot_name)
