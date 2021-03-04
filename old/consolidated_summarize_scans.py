from ROOTTools import *
import sys, warnings
from sensor_info import get_sensor_info

ROOT.gStyle.SetTitleX(0.28)
ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")

plot_dir_name = "Feb2021_TFPX_Results_as_of_March1/scratch_summary"

# FIXME note that this probably only works for nominal and for LKC20/27 stuff
filter_str = "nominal_Feb2021"
if len(sys.argv) > 1 :
    filter_str = sys.argv[1]

if "Dec2020" in filter_str :
    from block_dict import blocksDec2020 as blocks
elif "Feb2021" in filter_str :
    from block_dict import blocksFeb2021 as blocks

plot_dir_name += "_"+filter_str

show_sensor_info = True if filter_str else False
fit_size_2 = True

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

    # FIXME all old stuff to delete...
    #if filter_str and (not "nominal" in filter_str) and filter_str != "lkc" :
    #    plot_title += " ("
    #    if   "K" in filter_str : 
    #        plot_title += "LKC20"
    #    elif "L" in filter_str : 
    #        plot_title += "LKC27"
    #    elif "M" in filter_str : # FIXME note this is sort of useless since it's in the full summary too
    #        plot_title += "LKC40"
    #    plot_title += ")"

    basepath = "~/publicweb/TFPX/"

    files = []
    labels = []
    sensors = []
    variations = []

    orig_keys = sorted(blocks.keys())
    ordering = []
    if filter_str == "nominal_Dec2020" :
        ordering = ["131","135","180","185","183","184","186","193","194","114"]
    elif filter_str == "nominal_Feb2021" :
        #ordering = ["184","502","IT1","144irrad100V","IT5irrad0V","IT5irrad20V","IT5irrad100V","IT5irrad160V","IT5irrad180V","IT5irrad200V"]
        ordering = ["184","502","IT1","144irrad100V","IT5irrad200V"]
    elif filter_str == "IT5_bias_scan_Feb2021" :
        ordering = ["IT5irrad0V","IT5irrad20V","IT5irrad160V","IT5irrad180V","IT5irrad200V"]
    elif filter_str == "lkc" or "K" in filter_str or "L" in filter_str or "M" in filter_str :
        ordering = ["134"]
    sorted_keys = []
    for sensor in ordering :
        for key in orig_keys :
            if key == "134_EM1" : continue # skip this crummy one for now since the efficiency plots are empty

            if sensor in key :
                if "nominal" in filter_str :
                    pass
                    # old stuff that doesn't work anymore
                    #if "H" in key or "I" in key or "J" in key or "K" in key or "L" in key :
                    #    continue
                #elif filter_str == "lkc" :
                #    pass
                #elif not filter_str in key :
                #    continue
                sorted_keys.append(key)
    #print orig_keys
    #print sorted_keys

    all_variations = []
    color_variations = []
    if filter_str == "nominal_Dec2020" :
        all_variations = ["0","2","4","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","24"]
        varlabels = [var+"#circ" for var in all_variations]
        color_variations = [ROOT.kRed,ROOT.kBlack,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4,ROOT.kOrange,ROOT.kRed-2,ROOT.kBlue-2,ROOT.kGreen-2,ROOT.kGray+2,ROOT.kViolet+2]
    elif filter_str == "nominal_Feb2021" :
        all_variations = ["0","2","4","8","12","14","16","17","18","19","20","21","22","24"]
        varlabels = [var+"#circ" for var in all_variations]
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4]
    elif filter_str == "IT5_bias_scan_Feb2021" :
        all_variations = ["0V","20V","160V","180V","200V"]
        varlabels = [var for var in all_variations]
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4]
    if filter_str == "lkc" :
        all_variations = ["AK","BK","CK","DK","EK","AL","BL","CL","DL","EL","AM","BM","CM","DM","EM"]
        varlabels = ["0#circ","5#circ","10#circ","15#circ","20#circ"]*3
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3]*3
    if filter_str == "K" or filter_str == "L" or filter_str == "M" :
        all_variations = ["A","B","C","D","E"]
        varlabels = ["0#circ","5#circ","10#circ","15#circ","20#circ"]
        color_variations = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3]

    nbins = len(ordering) * len(all_variations)
    #print "nbins is",nbins,"len(ordering) is",len(ordering),"len(all_variations) is",len(all_variations)

    for key in sorted_keys :
        
        fpath = basepath+blocks[key]+"/"+plot_name+".root"
        #print fpath
        files.append(ROOT.TFile(fpath))

        sensor = key.split("_")[0]
        sensors.append(sensor)

        label = sensor+" "

        variation = ""
        # FIXME these are old and probably unnecessary now
        if   "_0" in key and filter_str != "0" : 
            label += "0#circ"
            variation = "0"
        if key.endswith("_2") and filter_str != "2" : 
            label += "2#circ"
            variation = "2"
        if "_4" in key and filter_str != "4" : 
            label += "4#circ"
            variation = "4"
        if "_6" in key and filter_str != "6" : 
            label += "6#circ"
            variation = "6"
        if "_7" in key and filter_str != "7" : 
            label += "7#circ"
            variation = "7"
        if "_8" in key and filter_str != "8" : 
            label += "8#circ"
            variation = "8"
        if "_10" in key and filter_str != "10" : 
            label += "10#circ"
            variation = "10"
        if "_12" in key and filter_str != "12" : 
            label += "12#circ"
            variation = "12"
        if "_14" in key and filter_str != "14" : 
            label += "14#circ"
            variation = "14"
        if "_15" in key and filter_str != "15" : 
            label += "15#circ"
            variation = "15"
        if "_16" in key and filter_str != "16" : 
            label += "16#circ"
            variation = "16"
        if "_17" in key and filter_str != "17" : 
            label += "17#circ"
            variation = "17"
        if "_18" in key and filter_str != "18" : 
            label += "18#circ"
            variation = "18"
        if "_19" in key and filter_str != "19" : 
            label += "19#circ"
            variation = "19"
        if "_20" in key and filter_str != "20" : 
            label += "20#circ"
            variation = "20"
        if "_21" in key and filter_str != "21" : 
            label += "21#circ"
            variation = "21"
        if "_22" in key and filter_str != "22" : 
            label += "22#circ"
            variation = "22"
        if "_24" in key and filter_str != "24" : 
            label += "24#circ"
            variation = "24"

        if "bias" in filter_str :
            label = sensor + " "
            if "0V" in key :
                label = "0V"
                variation = "0V"
            if "20V" in key :
                label = "20V"
                variation = "20V"
            if "40V" in key :
                label = "40V"
                variation = "40V"
            if "60V" in key :
                label = "60V"
                variation = "60V"
            if "80V" in key :
                label = "80V"
                variation = "80V"
            if "100V" in key :
                label = "100V"
                variation = "100V"
            if "120V" in key :
                label = "120V"
                variation = "120V"
            if "140V" in key :
                label = "140V"
                variation = "140V"
            if "160V" in key :
                label = "160V"
                variation = "160V"
            if "180V" in key :
                label = "180V"
                variation = "180V"
            if "200V" in key :
                label = "200V"
                variation = "200V"

        if filter_str == "lkc" :
            if   "K" in key :
                label += " LKC20"
                variation += "K"
            elif "L" in key :
                label += " LKC27"
                variation += "L"
            elif "M" in key :
                label += " LKC40"
                variation += "M"

        # for multiple blocks w/ same conditions - FIXME broken now!
        #if   key.endswith("1") : 
        #    label += " #1"
        #elif key.endswith("2") and key != "134_EM2" : # FIXME special case being skipped for now... 
        #    label += " #2"
        #    variation += "2"

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
    for duplicate in [""] :
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

                            if "ResidualsClusterSize2" in plot_name and fit_size_2 :
                                gauspol0 = ROOT.fitGausPol0(h)
                                fit = h.Fit(gauspol0, "RBLSQ")
                                mean = fit.Parameter(1)
                                sigma = fit.Parameter(2)
                                if abs(mean) > 35 :
                                    printout = "bin %i has mean %f and sigma %f" % (output_bin, mean, sigma)
                                    printout = "\033[91m" + printout + "\033[0m"
                                    warnings.warn(printout)
                                out_hist.SetBinContent(output_bin,mean)
                                out_hist.SetBinError(output_bin,sigma)
                            elif not "Efficiency" in plot_name :
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

                        # set label at midpoint for each sensor
                        set_label = ibin_secondary == len(all_variations)/2

                        # special case: in lkc scan for only MJ134, set labels at midpoint of each lkc setting
                        # FIXME this is hardcoded, so not ideal
                        if filter_str == "lkc" :
                            set_label = ibin_secondary % 5 == 2

                        if set_label :
                            if show_sensor_info :
                                tmp_sensor = ordering[ibin_primary]
                                pitch, sensor_type = get_sensor_info(tmp_sensor)
                                if filter_str == "lkc" :
                                    if   "K" in all_variations[ibin_secondary] :
                                        tmp_sensor += " LKC20"
                                    elif "L" in all_variations[ibin_secondary] :
                                        tmp_sensor += " LKC27"
                                    elif "M" in all_variations[ibin_secondary] :
                                        tmp_sensor += " LKC40"
                                output_bin_label = "#splitline{"+tmp_sensor+"}{#splitline{"+pitch+"}{"+sensor_type+"}}"
                            else : 
                                output_bin_label = tmp_sensor 

                            out_hist.GetXaxis().SetBinLabel(tmp_bin,output_bin_label)
                            out_hist.LabelsOption("h")

            if plot_name == "hClusterSize_Dut0" :
                y_axis_title = "average cluster size #pm RMS"
                out_hist.GetYaxis().SetRangeUser(0,4)
            elif "XResidualsClusterSize2" in plot_name and fit_size_2 :
                y_axis_title = "avg fitted X residual #pm #sigma (#mum)"
                out_hist.GetYaxis().SetRangeUser(-35,35)
            elif "YResidualsClusterSize2" in plot_name and fit_size_2 :
                y_axis_title = "avg fitted Y residual #pm #sigma (#mum)"
                out_hist.GetYaxis().SetRangeUser(-35,35)
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
                if "bias" in filter_str :
                    out_hist.GetYaxis().SetRangeUser(0,1.000001)
                else :
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
        leg = ps.c.BuildLegend(0.55,0.92,0.98,0.99)
        leg.SetNColumns(7)

    leg_primitives = leg.GetListOfPrimitives()
    iprim = 0

    for prim in leg_primitives :
        if "duplicate" in prim.GetLabel() :
            leg_primitives.Remove(prim)
        elif filter_str == "lkc" and iprim >= 5 : # only need legend to show each angle once. this isn't an ideal way to do it, but oh well 
            leg_primitives.Remove(prim)
        iprim += 1

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

            if filter_str == "lkc" and ibin_secondary % 5 == 0:
                line_position = out_hist.GetXaxis().GetBinLowEdge(tmp_bin)
                line = ROOT.TLine(line_position, ps.c.GetUymin(), line_position, ps.c.GetUymax())
                line.SetLineStyle(2)
                line.SetLineWidth(1)
                line.Draw()
                lines.append(line)

            elif ibin_secondary == 0 and ibin_primary != 0:
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
