from ROOTTools import *
import sys
from block_dict import blocks
from sensor_info import get_sensor_info

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box

plot_dir_name = "Dec2020_TFPX_Results_as_of_Jan16th/summary"

filter_str = None
if len(sys.argv) > 1 :
    filter_str = sys.argv[1]
    plot_dir_name += "_"+filter_str

show_sensor_info = True if filter_str else False

ps = plot_saver(plot_dir(plot_dir_name), size=(1200,600), log=False, pdf=True, pdf_log=False)

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
              ,"hLandauClusterSizeUpToMax_Dut0"
              ,"Efficiency_Dut0"
              ,"EfficiencyRef_Dut0"
             ]

for plot_name in plot_names :

    plot_title = plot_name
    if plot_title.startswith("h") : plot_title = plot_title[1:]
    plot_title = plot_title.replace("_","")
    plot_title = plot_title.replace("ResidualsClusterSize"," residuals cluster size ")
    plot_title = plot_title.replace("Residuals"," residuals")
    plot_title = plot_title.replace("LandauClusterSize","Charge distribution for clusters of size ")
    plot_title = plot_title.replace("UpToMax","up to 9")
    plot_title = plot_title.replace("ClusterSize","Cluster size distribution")
    plot_title = plot_title.replace("Efficiency","Overall efficiency")
    plot_title = plot_title.replace("Ref"," ref.")
    plot_title = plot_title.replace("Dut0","")
    plot_title += " summary"

    if filter_str :
        plot_title += " ("
        if   "A" in filter_str : 
            plot_title += "0#circ"
        elif "B" in filter_str : 
            plot_title += "5#circ"
        elif "C" in filter_str : 
            plot_title += "10#circ"
        elif "D" in filter_str : 
            plot_title += "15#circ"
        elif "E" in filter_str : 
            plot_title += "20#circ"
        elif "F" in filter_str : 
            plot_title += "24#circ"
        elif "G" in filter_str : 
            plot_title += "29#circ"
        elif "K" in filter_str : 
            plot_title += "LKC20"
        elif "L" in filter_str : 
            plot_title += "LKC27"
        elif "M" in filter_str : 
            plot_title += "LKC40"
        plot_title += ")"

    basepath = "~/publicweb/TFPX/"

    files = []
    labels = []

    orig_keys = sorted(blocks.keys())
    ordering = ["136","131","139","135","134","125","128","133","144","127","130","114","116"]
    sorted_keys = []
    for sensor in ordering :
        for key in orig_keys :

            if key == "134_EM1" : continue # skip this crummy one for now

            if sensor in key :
                if filter_str :
                    if not (key.endswith(filter_str) or key.endswith(filter_str+"1") or key.endswith(filter_str+"2") or filter_str+"M" in key) : continue
                sorted_keys.append(key)
    #print orig_keys
    #print sorted_keys

    for key in sorted_keys :
        
        fpath = basepath+blocks[key]+"/"+plot_name+".root"
        files.append(ROOT.TFile(fpath))

        sensor = key.split("_")[0]

        label = sensor+" "

        if sensor == "135" and not filter_str : # temperature scan
            if   "A" in key : 
                label += "13#circC"
            elif "H" in key : 
                label += "5#circC"
            elif "I" in key : 
                label += "0#circC"
            elif "J" in key : 
                label += "-5#circC"

        else :
            if not filter_str :
                if   "K" in key : 
                    label += "LKC20 "
                elif "L" in key : 
                    label += "LKC27 "
                elif "M" in key : 
                    label += "LKC40 "

            if   "A" in key and filter_str != "A" : 
                label += "0#circ"
            elif "B" in key and filter_str != "B" : 
                label += "5#circ"
            elif "C" in key and filter_str != "C" : 
                label += "10#circ"
            elif "D" in key and filter_str != "D" : 
                label += "15#circ"
            elif "E" in key and filter_str != "E" : 
                label += "20#circ"
            elif "F" in key and filter_str != "F" : 
                label += "24#circ"
            elif "G" in key and filter_str != "G" : 
                label += "29#circ"

        # for multiple blocks w/ same conditions
        if   key.endswith("1") : 
            label += " #1"
        elif key.endswith("2") : 
            label += " #2"

        if show_sensor_info :
            pitch, sensor_type = get_sensor_info(sensor)
            label = "#splitline{"+label+"}{#splitline{"+pitch+"}{"+sensor_type+"}}"

        labels.append(label)

    hists = []

    #if not "Efficiency" in plot_name :
    #    leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    #else :
    #    leg = ROOT.TLegend(0.50, 0.25, 0.85, 0.40)
    #leg.SetMargin(0.15)

    nbins = len(sorted_keys)
    out_hist = ROOT.TH1F(plot_name+"_summary", plot_title, nbins, 0, nbins)
    if "Efficiency" in plot_name : 
        out_hist.GetYaxis().SetTitle("efficiency")
    # FIXME for others

    for index in xrange(0,len(files)) :
        f = files[index]
        can = f.Get("c0")
        h = can.GetPrimitive(plot_name)
        h.SetName(labels[index])
        h.SetLineWidth(2)

        if not "Efficiency" in plot_name :
            mean = h.GetMean()
            rms = h.GetRMS()
            out_hist.SetBinContent(index+1,mean)
            out_hist.SetBinError(index+1,rms)
        else :
            out_hist.SetBinContent(index+1,h.GetBinContent(1))

        out_hist.GetXaxis().SetBinLabel(index+1,labels[index])

    if plot_name == "hClusterSize_Dut0" :
        y_axis_title = "average cluster size #pm RMS"
    elif "XResiduals" in plot_name :
        y_axis_title = "average X residual #pm RMS (#mum)"
    elif "YResiduals" in plot_name :
        y_axis_title = "average Y residual #pm RMS (#mu m)"
    elif "Landau" in plot_name :
        y_axis_title = "average charge #pm RMS (electrons)"
    elif "Efficiency" in plot_name :
        y_axis_title = "efficiency"

    ps.c.cd()
    #ps.c.SetGrid()
    out_hist.SetStats(0)
    out_hist.GetYaxis().SetTitle(y_axis_title)
    out_hist.SetMarkerStyle(20)
    out_hist.SetLineWidth(2)
    out_hist.SetMarkerColor(ROOT.kBlack)
    out_hist.SetLineColor(ROOT.kBlack)
    ps.c.SetBottomMargin(0.2)
    ps.c.SetLeftMargin(0.10)
    ps.c.SetRightMargin(0.02)
    if "Efficiency" in plot_name :
        out_hist.Draw("p")
        out_hist.GetYaxis().SetRangeUser(0.8,1.000001)
    else :
        out_hist.Draw("pE1")

    # add y-axis gridlines for visibility
    ps.c.SetGridy()

    ps.update_canvas()

    lines = []

    # add lines for plots for fixed angle summarizing multiple sensor types
    for ibin in xrange(1,out_hist.GetXaxis().GetNbins()) :
        sensor_this = out_hist.GetXaxis().GetBinLabel(ibin)
        sensor_next = out_hist.GetXaxis().GetBinLabel(ibin+1)

        sensor_this = sensor_this.replace(" ","").replace("#1","").replace("#2","").replace("#splitline{","")[0:3]
        sensor_next = sensor_next.replace(" ","").replace("#1","").replace("#2","").replace("#splitline{","")[0:3]
        
        if get_sensor_info(sensor_this) != get_sensor_info(sensor_next) :
            line_position = out_hist.GetXaxis().GetBinUpEdge(ibin)
            line = ROOT.TLine(line_position, ps.c.GetUymin(), line_position, ps.c.GetUymax())
            line.SetLineStyle(2)
            line.SetLineWidth(1)
            line.Draw()
            lines.append(line)

    ps.update_canvas()

    #if plot_name == "hClusterSize_Dut0" :
    #    histmin = 5e-6
    #    histmax = 1
    #elif "ResidualsClusterSize2" in plot_name :
    #    histmin = 1e-5
    #    histmax = 0.08
    #elif "Residuals" in plot_name :
    #    histmin = 5e-6
    #    histmax = 0.06
    #elif "Landau" in plot_name :
    #    histmin = 1e-5
    #    histmax = 0.025
    #elif "Efficiency" in plot_name :
    #    histmin = 0.8
    #    histmax = 1

    #hists[0].GetYaxis().SetRangeUser(histmin, histmax)
    #leg.Draw()
    #ps.update_canvas()
    ps.save(plot_name)
