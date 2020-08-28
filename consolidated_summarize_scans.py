from ROOTTools import *
import sys
from block_dict import blocks
from sensor_info import get_sensor_info

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box

plot_dir_name = "Spring2020_TFPX_Results/summaries/consolidated_summary"

# FIXME note that this probably only works for nominal and for LKC20/27 stuff
filter_str = "nominal"
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
    plot_title = plot_title.replace("ClusterSize","Cluster size distribution")
    plot_title = plot_title.replace("Efficiency","Overall efficiency")
    plot_title = plot_title.replace("Ref"," ref.")
    plot_title = plot_title.replace("Dut0","")
    plot_title += " summary"

    if filter_str and filter_str != "nominal" :
        plot_title += " ("
        if   "K" in filter_str : 
            plot_title += "LKC20"
        elif "L" in filter_str : 
            plot_title += "LKC27"
        elif "M" in filter_str : # FIXME note this is sort of useless since it's in the full summary too
            plot_title += "LKC40"
        plot_title += ")"

    basepath = "~/public_html/TFPX/Spring2020_TFPX_Results/"

    files = []
    labels = []
    sensors = []
    variations = []

    orig_keys = sorted(blocks.keys())
    ordering = []
    if filter_str == "nominal" :
        ordering = ["136","131","139","135","134","125","128","133","144","127","130","114","116"]
    elif "K" in filter_str or "L" in filter_str or "M" in filter_str :
        ordering = ["134"]
    sorted_keys = []
    for sensor in ordering :
        for key in orig_keys :

            if key == "134_EM1" : continue # skip this crummy one for now since the efficiency plots are empty

            if sensor in key :
                if filter_str == "nominal" :
                    if "H" in key or "I" in key or "J" in key or "K" in key or "L" in key :
                        continue
                elif not filter_str in key :
                    continue
                sorted_keys.append(key)
    #print orig_keys
    #print sorted_keys

    all_variations = []
    color_variations = []
    if filter_str == "nominal" :
        all_variations = ["A","B","C","D","E","F","G"]
        varlabels = ["0#circ","5#circ","10#circ","15#circ","20#circ","24#circ","29#circ"]
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1]
    if filter_str == "K" or filter_str == "L" or filter_str == "M" :
        all_variations = ["A","B","C","D","E"]
        varlabels = ["0#circ","5#circ","10#circ","15#circ","20#circ"]
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3]

    nbins = len(ordering) * len(all_variations)

    for key in sorted_keys :
        
        fpath = basepath+blocks[key]+"/"+plot_name+".root"
        files.append(ROOT.TFile(fpath))

        sensor = key.split("_")[0]
        sensors.append(sensor)

        label = sensor+" "

        if   "A" in key and filter_str != "A" : 
            label += "0#circ"
            variation = "A"
        elif "B" in key and filter_str != "B" : 
            label += "5#circ"
            variation = "B"
        elif "C" in key and filter_str != "C" : 
            label += "10#circ"
            variation = "C"
        elif "D" in key and filter_str != "D" : 
            label += "15#circ"
            variation = "D"
        elif "E" in key and filter_str != "E" : 
            label += "20#circ"
            variation = "E"
        elif "F" in key and filter_str != "F" : 
            label += "24#circ"
            variation = "F"
        elif "G" in key and filter_str != "G" : 
            label += "29#circ"
            variation = "G"

        # for multiple blocks w/ same conditions
        if   key.endswith("1") : 
            label += " #1"
        elif key.endswith("2") and key != "134_EM2" : # FIXME special case being skipped for now... 
            label += " #2"
            variation += "2"

        if show_sensor_info :
            pitch, sensor_type = get_sensor_info(sensor)
            label = "#splitline{"+label+"}{#splitline{"+pitch+"}{"+sensor_type+"}}"

        labels.append(label)
        variations.append(variation)

    hists = []

    #if not "Efficiency" in plot_name :
    #    leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.90)
    #else :
    #    leg = ROOT.TLegend(0.50, 0.25, 0.85, 0.40)
    #leg.SetMargin(0.15)

    #nbins = len(sorted_keys)
    for duplicate in ["", "2"] :
        for varindex in xrange(0, len(all_variations)) :
            var = all_variations[varindex]
            varlabel = varlabels[varindex]
            if duplicate != "" :
                varlabel += "_duplicate" + duplicate
            out_hist = ROOT.TH1F(plot_name+"_summary_"+var+duplicate, varlabel, nbins, 0, nbins)

            for index in xrange(0,len(files)) :

                this_sensor = sensors[index]
                this_var = variations[index]

                if var+duplicate != this_var : continue

                f = files[index]
                can = f.Get("c0")
                h = can.GetPrimitive(plot_name)
                h.SetName(labels[index])
                h.SetLineWidth(2)
                
                for ibin_primary in xrange(0,len(ordering)) :
                    for ibin_secondary in xrange(0,len(all_variations)) :
                        if this_sensor == ordering[ibin_primary] and this_var == all_variations[ibin_secondary]+duplicate :
                            output_bin = len(all_variations)*ibin_primary + ibin_secondary 
                            output_bin += 1 # for the root bin ordering

                            if not "Efficiency" in plot_name :
                                mean = h.GetMean()
                                rms = h.GetRMS()
                                out_hist.SetBinContent(output_bin,mean)
                                out_hist.SetBinError(output_bin,rms)
                            else :
                                out_hist.SetBinContent(output_bin,h.GetBinContent(1))


            # now set the bin labels... this is ugly since it was being finnicky
            if duplicate == "" :
                for ibin_primary in xrange(0,len(ordering)) :
                    for ibin_secondary in xrange(0,len(all_variations)) :

                        tmp_bin = len(all_variations)*ibin_primary + ibin_secondary 
                        tmp_bin += 1 # for the root bin ordering

                        if ibin_secondary == len(all_variations)/2 :
                            if show_sensor_info :
                                tmp_sensor = ordering[ibin_primary]
                                pitch, sensor_type = get_sensor_info(tmp_sensor)
                                output_bin_label = "#splitline{"+tmp_sensor+"}{#splitline{"+pitch+"}{"+sensor_type+"}}"
                            else : 
                                output_bin_label = tmp_sensor 

                            out_hist.GetXaxis().SetBinLabel(tmp_bin,output_bin_label)
                            out_hist.LabelsOption("h")

            if plot_name == "hClusterSize_Dut0" :
                y_axis_title = "average cluster size #pm RMS"
                out_hist.GetYaxis().SetRangeUser(0,4)
            elif "XResiduals" in plot_name :
                y_axis_title = "average X residual #pm RMS (#mum)"
                out_hist.GetYaxis().SetRangeUser(-35,35)
            elif "YResiduals" in plot_name :
                y_axis_title = "average Y residual #pm RMS (#mu m)"
                out_hist.GetYaxis().SetRangeUser(-35,35)
            elif "Landau" in plot_name :
                y_axis_title = "average charge #pm RMS (electrons)"
                out_hist.GetYaxis().SetRangeUser(0,25000)
            elif "Efficiency" in plot_name :
                y_axis_title = "efficiency"
                out_hist.GetYaxis().SetRangeUser(0.8,1.000001)

            out_hist.SetLineColor(color_variations[varindex])
            out_hist.SetMarkerColor(color_variations[varindex])
            hists.append(out_hist)

            ps.c.cd()
            out_hist.SetStats(0)
            out_hist.GetYaxis().SetTitle(y_axis_title)
            if duplicate == "" :
                out_hist.SetMarkerStyle(20)
                out_hist.SetMarkerSize(1)
            else :
                out_hist.SetMarkerStyle(20+2*int(duplicate))
                out_hist.SetMarkerSize(1.25)
            out_hist.SetLineWidth(2)
            ps.c.SetBottomMargin(0.2)
            ps.c.SetLeftMargin(0.10)
            ps.c.SetRightMargin(0.02)

            drawopt = ""
            if varindex != 0 or duplicate != "":
                drawopt += "same "

            if out_hist.GetEntries() > 0 :
                if "Efficiency" in plot_name :
                    out_hist.Draw(drawopt+"p X0")
                else :
                    out_hist.Draw(drawopt+"p E1 X0")

            hists.append(out_hist)
            ps.update_canvas()
    #print hists

    # add y-axis gridlines for visibility
    ps.c.SetGridy()
    leg = None
    if filter_str == "K" or filter_str == "L" or filter_str == "M" :
        leg = ps.c.BuildLegend(0.82,0.92,0.98,0.99)
        leg.SetNColumns(3)
    else :
        leg = ps.c.BuildLegend(0.77,0.92,0.98,0.99)
        leg.SetNColumns(4)
    leg_primitives = leg.GetListOfPrimitives()
    for prim in leg_primitives :
        if "duplicate" in prim.GetLabel() :
            leg_primitives.Remove(prim)

    ps.update_canvas()
    
    # https://root-forum.cern.ch/t/change-histograms-title-on-canvas/17854/9
    primitives = ps.c.GetListOfPrimitives()
    primitives[1].SetTitle(plot_title)
    primitives.Remove(primitives.FindObject("title"))
    ps.update_canvas()

    lines = []

    # add lines for plots for fixed angle summarizing multiple sensor types
    for ibin_primary in xrange(0,len(ordering)) :
        for ibin_secondary in xrange(0,len(all_variations)) :

            tmp_bin = len(all_variations)*ibin_primary + ibin_secondary 
            tmp_bin += 1 # for the root bin ordering

            if ibin_secondary == 0 and ibin_primary != 0:
                tmp_sensor = ordering[ibin_primary]
                tmp_sensor_prev = ordering[ibin_primary-1]

                line_position = out_hist.GetXaxis().GetBinLowEdge(tmp_bin)
                line = ROOT.TLine(line_position, ps.c.GetUymin(), line_position, ps.c.GetUymax())
                if get_sensor_info(tmp_sensor) == get_sensor_info(tmp_sensor_prev) :
                    line.SetLineStyle(2)
                    line.SetLineWidth(1)
                else :
                    line.SetLineStyle(1)
                    line.SetLineWidth(2)
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
