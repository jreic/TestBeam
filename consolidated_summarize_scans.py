from ROOTTools import *
import sys, warnings, math
from block_class import get_sensor_info

ROOT.gStyle.SetTitleX(0.28)
ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning
eff_ymax = 1.000001

plot_dir_name = "summary"
scan_type = "angle"

filter_str = "nominal_Feb2021"
if len(sys.argv) > 1 :
    filter_str = sys.argv[1]

if filter_str == "IT5_bias_scan_Feb2021" :
    scan_type = "bias"

if "Dec2020" in filter_str :
    from block_list import blocksDec2020 as blocks
elif "Feb2021" in filter_str :
    from block_list import blocksFeb2021 as blocks

plot_dir_name += "_"+filter_str

show_sensor_info = True if filter_str else False
fit_size_2 = True
fit_charge = False

ps = plot_saver(plot_dir(plot_dir_name), size=(1200,600), log=False, pdf=True, pdf_log=False)

plot_paths = [ 
               "Charge/Dut0/ClusterSize/hClusterSize_Dut0"
              ,"Resolution/Dut0/XResiduals/hXResiduals_Dut0"
              ,"Resolution/Dut0/YResiduals/hYResiduals_Dut0"
              ,"Resolution/Dut0/XResiduals/hXResidualsClusterSize1_Dut0"
              ,"Resolution/Dut0/YResiduals/hYResidualsClusterSize1_Dut0"
              ,"Resolution/Dut0/XResiduals/hXResidualsClusterSize2_Dut0"
              ,"Resolution/Dut0/YResiduals/hYResidualsClusterSize2_Dut0"
              ,"Charge/Dut0/Landau/hLandauClusterSize1_Dut0"
              ,"Charge/Dut0/Landau/hLandauClusterSize2_Dut0"
              ,"Charge/Dut0/Landau/hLandauClusterSize3_Dut0"
              ,"Charge/Dut0/Landau/hLandauClusterSizeUpToMax_Dut0"
              ,"Efficiency/Dut0/Efficiency/Efficiency_Dut0"
              ,"Efficiency/Dut0/Efficiency/EfficiencyRef_Dut0"
             ]

for plot_path in plot_paths :

    plot_name = plot_path.split("/")[-1]

    plot_title = plot_name
    if plot_title.startswith("h") : plot_title = plot_title[1:]
    plot_title = plot_title.replace("_","")
    plot_title = plot_title.replace("ResidualsClusterSize"," residuals cluster size ")
    plot_title = plot_title.replace("Residuals"," residuals")
    plot_title = plot_title.replace("LandauClusterSizeUpToMax", "Charge distribution for cluster size#leq9")
    plot_title = plot_title.replace("LandauClusterSize","Charge distribution for clusters of size ")
    plot_title = plot_title.replace("ClusterSize","Cluster size distribution")
    plot_title = plot_title.replace("Efficiency","Overall efficiency")
    plot_title = plot_title.replace("Ref"," ref.")
    plot_title = plot_title.replace("Dut0","")
    plot_title += " summary"

    #basepath = "~/publicweb/TFPX/"
    basepath = "~/nobackup/Chewie_root_files/"

    labels = []
    sensors = []
    variations = []

    ordering = []
    if filter_str == "nominal_Dec2020" :
        ordering = ["131","135","180","185","183","184","186","193","194","114"]
    elif filter_str == "nominal_Feb2021" :
        ordering = ["184","502","IT1","144irrad","IT5irrad"]
    elif filter_str == "IT5_bias_scan_Feb2021" :
        ordering = ["IT5irrad"]

    largest_duplicate = 0
    sorted_blocks = []
    for sensor in ordering :
        for block in blocks :

            if sensor == block.sensor_name :

                if filter_str == "nominal_Feb2021" :
                    if block.sensor_name == "144irrad" and block.bias != 100 : continue
                    if block.sensor_name == "IT5irrad" and block.bias != 200 : continue
                if filter_str == "IT5_bias_scan_Feb2021" :
                    if block.angle != 0 : continue

                sensors.append(sensor)
                sorted_blocks.append(block)

                block.root_file = ROOT.TFile(basepath+block.run_range+".root")

                # for overlaying separate run blocks w/ identical conditions
                largest_duplicate = max(largest_duplicate,block.duplicate)

    if scan_type == "angle" :
        variations = sorted(set(block.angle for block in sorted_blocks))
        varlabels = ["%s#circ" % var for var in variations]
    elif scan_type == "bias" :
        variations = sorted(set(block.bias for block in sorted_blocks))
        varlabels = ["%sV" % var for var in variations]

    n_vars = len(variations)
    colors = [ROOT.kRed,ROOT.kBlack,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4,ROOT.kOrange,ROOT.kRed-2,ROOT.kBlue-2,ROOT.kGreen-2,ROOT.kGray+2,ROOT.kViolet+2]
    #colors = [ROOT.kGray,ROOT.kBlack,ROOT.kRed,ROOT.kGreen,ROOT.kBlue,ROOT.kYellow+1,ROOT.kMagenta,ROOT.kCyan,ROOT.kOrange,ROOT.kSpring,ROOT.kTeal,ROOT.kAzure,ROOT.kViolet,ROOT.kPink] # FIXME add more on to here

    nbins = len(ordering) * len(variations)

    hists = []

    for duplicate in xrange(0, largest_duplicate+1) :
        for varidx in xrange(0, len(variations)) :
            var = variations[varidx]
            varlabel = varlabels[varidx]

            out_hist_name = plot_name+"_summary_"+str(var)
            out_hist_label = varlabel
            if duplicate > 0 :
                out_hist_name  += "duplicate"+str(duplicate)
                out_hist_label += "duplicate"+str(duplicate)
            out_hist = ROOT.TH1F(out_hist_name, out_hist_label, nbins, 0, nbins)
            hists.append(out_hist)

            for block in sorted_blocks :

                if scan_type == "angle" :
                    if block.angle != var : continue
                elif scan_type == "bias" :
                    if block.bias != var : continue

                if block.duplicate != duplicate :
                    continue

                f = block.root_file
                h = f.Get(plot_path)
                h.SetName(block.run_range)
                h.SetLineWidth(2)

                ibin_secondary = varidx
                for ibin_primary in xrange(0,len(ordering)) :
                    if block.sensor_name == ordering[ibin_primary] and var == variations[ibin_secondary] :
                        output_bin = len(variations)*ibin_primary + ibin_secondary
                        output_bin += 1 # for the root bin ordering

                        if "Landau" in plot_name and h.GetEntries() > 0 and fit_charge :
                            langaus = ROOT.langausFit(h)
                            fit = h.Fit(langaus, "RBLSQ0")
                            mpv = fit.Parameter(1)
                            lwidth = fit.Parameter(0)
                            gsigma = fit.Parameter(3)
                            err = math.sqrt(lwidth**2+gsigma**2)

                            out_hist.SetBinContent(output_bin, mpv)
                            out_hist.SetBinError(output_bin, err)
                        elif "ResidualsClusterSize2" in plot_name and fit_size_2 :
                            gauspol0 = ROOT.fitGausPol0(h)
                            fit = h.Fit(gauspol0, "RBLSQ0")
                            mean = fit.Parameter(1)
                            sigma = fit.Parameter(2)
                            if abs(mean) > 35 :
                                printout = "bin %i has mean %f and sigma %f" % (output_bin, mean, sigma)
                                printout = "\033[91m" + printout + "\033[0m"
                                warnings.warn(printout)
                            out_hist.SetBinContent(output_bin,mean)
                            out_hist.SetBinError(output_bin,sigma)
                        elif "Efficiency" in plot_name :
                            h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))
                            nevents = h_norm.GetBinContent(1)
                            eff = h.GetBinContent(1)
                            abs_err_down, abs_err_up = clopper_pearson_abs_err(nevents, eff)
                            max_err = max(abs_err_down, abs_err_up)

                            out_hist.SetBinContent(output_bin,eff)
                            out_hist.SetBinError(output_bin,max_err)
                        else :
                            mean = h.GetMean()
                            rms = h.GetRMS()
                            out_hist.SetBinContent(output_bin,mean)
                            out_hist.SetBinError(output_bin,rms)

            # now set the bin labels... this is ugly since it was being finnicky
            for ibin_primary in xrange(0,len(ordering)) :
                for ibin_secondary in xrange(0,len(variations)) :

                    tmp_bin = len(variations)*ibin_primary + ibin_secondary 
                    tmp_bin += 1 # for the root bin ordering

                    # set label at midpoint for each sensor
                    set_label = ibin_secondary == len(variations)/2

                    if set_label :
                        tmp_sensor = ordering[ibin_primary]
                        pitch, sensor_type = get_sensor_info(tmp_sensor)
                        if filter_str == "nominal_Feb2021" :
                            if tmp_sensor == "144irrad" :
                                tmp_sensor += " 100V"
                            elif tmp_sensor == "IT5irrad" :
                                tmp_sensor += " 200V"
                        elif filter_str == "IT5_bias_scan_Feb2021" :
                            tmp_sensor += " 0#circ incident angle"

                        output_bin_label = "#splitline{"+tmp_sensor+"}{#splitline{"+pitch+"}{"+sensor_type+"}}"

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
                y_axis_title = "average Y residual #pm RMS (#mum)"
                out_hist.GetYaxis().SetRangeUser(-35,35)
            elif "Landau" in plot_name :
                if fit_charge :
                    y_axis_title = "fitted charge #pm (width #otimes #sigma) (electrons)"
                else :
                    y_axis_title = "average charge #pm RMS (electrons)"
                out_hist.GetYaxis().SetRangeUser(0,25000)
            elif "Efficiency" in plot_name :
                y_axis_title = "efficiency"
                out_hist.GetYaxis().SetRangeUser(0.95,eff_ymax)

            out_hist.SetLineColor(colors[varidx])
            out_hist.SetMarkerColor(colors[varidx])

            ps.c.cd()
            out_hist.SetStats(0)
            out_hist.GetXaxis().SetTickLength(0)
            out_hist.GetYaxis().SetTitle(y_axis_title)
            if duplicate == 0 :
                out_hist.SetMarkerStyle(20)
                out_hist.SetMarkerSize(1)
                out_hist.SetLineWidth(2)
            else :
                out_hist.SetMarkerStyle(20+4*duplicate)
                out_hist.SetMarkerSize(1.25)
                out_hist.SetLineWidth(1)
            ps.c.SetBottomMargin(0.2)
            ps.c.SetLeftMargin(0.10)
            ps.c.SetRightMargin(0.02)

            drawopt = ""
            if varidx != 0 or duplicate != 0 :
                drawopt += "same "

            if out_hist.GetEntries() > 0 :
                out_hist.Draw(drawopt+"p E1 X0")
            ps.update_canvas()

    # add y-axis gridlines for visibility
    ps.c.SetGridy()
    leg = None
    leg = ps.c.BuildLegend(0.55,0.92,0.98,0.99)
    leg.SetNColumns(7)

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

    def drawLines(ps, hist, ordering, variations, ymin, ymax) :
        lines = []

        # add lines for plots for fixed angle summarizing multiple sensor types
        for ibin_primary in xrange(0,len(ordering)) :
            for ibin_secondary in xrange(0,len(variations)) :

                tmp_bin = len(variations)*ibin_primary + ibin_secondary 
                tmp_bin += 1 # for the root bin ordering

                if ibin_secondary == 0 and ibin_primary != 0:
                    tmp_sensor = ordering[ibin_primary]
                    tmp_sensor_prev = ordering[ibin_primary-1]

                    line_position = hist.GetXaxis().GetBinLowEdge(tmp_bin)
                    line = ROOT.TLine(line_position, ymin, line_position, ymax)
                    if get_sensor_info(tmp_sensor) == get_sensor_info(tmp_sensor_prev) :
                        line.SetLineStyle(2)
                        line.SetLineWidth(1)
                    else :
                        line.SetLineStyle(1)
                        line.SetLineWidth(2)
                    line.Draw()
                    lines.append(line)
        return lines

    lines = drawLines(ps, hists[0], ordering, variations, ps.c.GetUymin(), ps.c.GetUymax())

    ps.update_canvas()
    ps.save(plot_name)

    if "Efficiency" in plot_name :
        hists[0].GetYaxis().SetRangeUser(0.8,eff_ymax)
        # I expected that ps.c.GetUymin/max would work, but it didn't for these so I hardcode instead
        lines = drawLines(ps, hists[0], ordering, variations, 0.8, eff_ymax)
        ps.update_canvas()
        ps.save(plot_name+"_0.8to1")

        hists[0].GetYaxis().SetRangeUser(0,eff_ymax)
        lines = drawLines(ps, hists[0], ordering, variations, 0, eff_ymax)
        ps.update_canvas()
        ps.save(plot_name+"_0to1")
        

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
