from ROOTTools import *
import sys, os, warnings, math
from block_class import get_sensor_info

ROOT.gStyle.SetTitleX(0.32)
ROOT.gStyle.SetOptFit(0o0100) # adds Landau MPV to stat box
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning
eff_ymax = 1.000001
maxresidual = 35

plot_dir_name = "summary_all_angles"
scan_type = "angle"

filter_str = "FBK3D"
if len(sys.argv) > 1 :
    filter_str = sys.argv[1]

if filter_str == "IT5_bias_scan_Feb2021" :
    scan_type = "bias"

if filter_str == "MJ209_bias_scan_0deg_Nov2021" :
    plot_dir_name = "summary"
    scan_type = "bias"
elif filter_str == "MJ209_bias_scan_12deg_Nov2021" :
    plot_dir_name = "summary"
    scan_type = "bias"
elif filter_str == "MJ209_angle_scan_65V_Nov2021" :
    plot_dir_name = "summary"
    scan_type = "angle"

if filter_str == "MJ114_bias_scans_Dec2021" :
    plot_dir_name = "summary"
    scan_type = "bias"

if filter_str == "MJ116_bias_scans_Dec2021" :
    plot_dir_name = "summary"
    scan_type = "bias"

if filter_str == "CNM3D_bias_scans_Dec2021" :
    plot_dir_name = "summary"
    scan_type = "bias"

if "Dec2020" in filter_str :
    from block_list import blocksDec2020 as blocks
elif "Feb2021" in filter_str :
    from block_list import blocksFeb2021 as blocks
elif "3D" in filter_str :
    from block_list import blocksDec2019
    from block_list import blocksDec2020
    from block_list import blocksSpring2020
    from block_list import blocksMarch2021
    blocks = blocksDec2019 + blocksDec2020 + blocksSpring2020 + blocksMarch2021
if "April2021" in filter_str :
    from block_list import blocksApril2021 as blocks
if "June2021" in filter_str :
    from block_list import blocksJune2021 as blocks
if "Nov2021" in filter_str :
    from block_list import blocksNov2021 as blocks
if "Dec2021" in filter_str :
    from block_list import blocksDec2021 as blocks

plot_dir_name += "_"+filter_str

show_sensor_info = True if filter_str else False
fit_size_2 = True
fit_charge = False
subtract_telescope = False

ps = plot_saver(plot_dir(plot_dir_name), size=(600,600), log=False, pdf=True, pdf_log=False)

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
              ,"Efficiency/Dut0/Efficiency/EfficiencyNorm_Dut0"
              ,"Efficiency/Dut0/Efficiency/EfficiencyRefNorm_Dut0"
             ]

invalid_blocks = []

for plot_path in plot_paths :

    plot_name = plot_path.split("/")[-1]

    plot_title = plot_name
    if plot_title.startswith("h") : plot_title = plot_title[1:]
    plot_title = plot_title.replace("_","")
    plot_title = plot_title.replace("ResidualsClusterSize"," residuals cluster size ")
    plot_title = plot_title.replace("Residuals"," residuals")
    plot_title = plot_title.replace("LandauClusterSizeUpToMax", "Charge for cluster size#leq9")
    plot_title = plot_title.replace("LandauClusterSize","Charge for cluster size ")
    plot_title = plot_title.replace("ClusterSize","Cluster size")
    plot_title = plot_title.replace("Efficiency","Overall efficiency")
    plot_title = plot_title.replace("Ref"," ref.")
    plot_title = plot_title.replace("Norm"," denominator")
    plot_title = plot_title.replace("Dut0","")

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
    elif filter_str == "3D_50x50_all" :
        ordering = ["114","114_Sp20","116_Sp20","194"]
    elif filter_str == "3D_50x50" :
        ordering = ["114","194"]
    elif filter_str == "3D_25x100_all" :
        ordering = ["193","IT19","113_Dec19"]
        maxresidual = 50
    elif filter_str == "3D_25x100" :
        ordering = ["193","IT19"]
        maxresidual = 50
    elif filter_str == "FBK3D" :
        ordering = ["193","194"]
        maxresidual = 20
    elif filter_str == "April2021" :
        ordering = ["116","207"]
    elif filter_str == "June2021" :
        ordering = ["IT4"]
    elif "Nov2021" in filter_str :
        ordering = ["209"]
    elif filter_str == "MJ114_bias_scans_Dec2021" :
        ordering = ["114"]
    elif filter_str == "MJ116_bias_scans_Dec2021" :
        ordering = ["116"]
    elif "Dec2021" in filter_str :
        ordering = ["114","116"]

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
                if filter_str == "MJ209_bias_scan_0deg_Nov2021" :
                    if block.angle != 0 : continue
                if filter_str == "MJ209_bias_scan_12deg_Nov2021" :
                    if block.angle != 12 : continue
                if filter_str == "MJ209_angle_scan_65V_Nov2021" :
                    if block.bias != 65 : continue
                if "bias_scans_Dec2021" in filter_str :
                    if block.angle != 0 : continue
                if filter_str == "MJ114_bias_scans_Dec2021" :
                    if block.sensor_name != "114" : continue
                if filter_str == "MJ116_bias_scans_Dec2021" :
                    if block.sensor_name != "116" : continue
                #if block.angle > 8 : continue

                fpath = os.path.expanduser(basepath+block.run_range+".root") # to expand the ~
                if not os.path.exists(fpath) :
                    invalid_blocks.append(fpath)
                    continue

                block.root_file = ROOT.TFile(fpath)

                sensors.append(sensor)
                sorted_blocks.append(block)

                # for overlaying separate run blocks w/ identical conditions
                largest_duplicate = max(largest_duplicate,block.duplicate)

    if scan_type == "angle" :
        variations = sorted(set(block.angle for block in sorted_blocks))
        varlabels = ["%s#circ" % var for var in variations]
    elif scan_type == "bias" :
        variations = sorted(set(block.bias for block in sorted_blocks))
        varlabels = ["%sV" % var for var in variations]

    n_vars = len(variations)
    colors = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kViolet-3,ROOT.kOrange-6,ROOT.kCyan+1,ROOT.kMagenta,ROOT.kTeal+5,ROOT.kAzure+2,ROOT.kYellow+2,ROOT.kSpring,ROOT.kGray,ROOT.kAzure-4,ROOT.kOrange,ROOT.kRed-2,ROOT.kBlue-2,ROOT.kSpring+4,ROOT.kGray+2,ROOT.kViolet+2, ROOT.kPink+1]

    # FIXME in the future if doing a bias scan, we could modify this so we don't have 100+ bins, and instead subdivide better
    nbins = int(max(variations))+1

    hists = []

    for index, sensor in enumerate(ordering) :
        out_hist_name = plot_name+"_summary_"+sensor
        sensor_name_for_legend = sensor
        if filter_str == "3D_50x50" :
            if   sensor == "114" : sensor_name_for_legend += " (CNM, -51V)"
            elif sensor == "194" : sensor_name_for_legend += " (FBK, -30V)"
        if filter_str == "3D_25x100" :
            if sensor == "IT19" : sensor_name_for_legend += " (FBK, -30V)"
            if sensor == "193"  : sensor_name_for_legend += " (FBK, -25/30V)"
        if filter_str == "FBK3D" :
            if sensor == "193"  : sensor_name_for_legend += " (25x100)"
            if sensor == "194"  : sensor_name_for_legend += " (50x50)"

        if filter_str == "MJ209_bias_scan_0deg_Nov2021" :
            sensor_name_for_legend += " (0#circ)"
        elif filter_str == "MJ209_bias_scan_12deg_Nov2021" :
            sensor_name_for_legend += " (12#circ)"
        elif filter_str == "MJ209_angle_scan_65V_Nov2021" :
            sensor_name_for_legend += " (-65V)"

        if "bias_scans_Dec2021" in filter_str :
            if   sensor == "114" : sensor_name_for_legend += " (1650e)"
            elif sensor == "116" : sensor_name_for_legend += " (2100e)"

        out_hist = ROOT.TH1F(out_hist_name, sensor_name_for_legend, nbins, 0, nbins)
        if scan_type == "angle"  : out_hist.GetXaxis().SetTitle("angle (#circ)")
        elif scan_type == "bias" : out_hist.GetXaxis().SetTitle("bias (-V)")
        hists.append(out_hist)

        for block in sorted_blocks :
            if block.sensor_name != sensor : continue
            if block.duplicate != 0 : continue

            #print block.sensor_name, block.angle
            f = block.root_file
            h = f.Get(plot_path)
            if not issubclass(type(h),ROOT.TH1) : continue

            if scan_type == "angle"  : output_bin = out_hist.FindBin(block.angle)
            elif scan_type == "bias" : output_bin = out_hist.FindBin(block.bias)

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
                sigma_fit_err = max(fit.LowerError(2), fit.UpperError(2))

                track_resolution = 0
                track_resolution_rms = 0
                
                if subtract_telescope :
                    if "X" in plot_name :
                        # note X DUT == Y telescope
                        h_track_resolution = f.Get("Resolution/Dut0/Errors/hPredictedYErrors_Dut0")
                    else :
                        # note X DUT == Y telescope
                        h_track_resolution = f.Get("Resolution/Dut0/Errors/hPredictedXErrors_Dut0")

                    track_resolution = h_track_resolution.GetMean()
                    track_resolution_rms = h_track_resolution.GetRMS()

                sigma = math.sqrt(sigma**2 - track_resolution**2)
                sigma_fit_err = math.sqrt(sigma_fit_err**2 + track_resolution_rms**2)

                out_hist.SetBinContent(output_bin,sigma)
                out_hist.SetBinError(output_bin,sigma_fit_err)
            elif "Residuals" in plot_name :
                rms = h.GetRMS()
                rmserr = h.GetRMSError()

                track_resolution = 0
                track_resolution_rms = 0
                
                if subtract_telescope :
                    if "X" in plot_name :
                        # note X DUT == Y telescope
                        h_track_resolution = f.Get("Resolution/Dut0/Errors/hPredictedYErrors_Dut0")
                    else :
                        # note X DUT == Y telescope
                        h_track_resolution = f.Get("Resolution/Dut0/Errors/hPredictedXErrors_Dut0")

                    track_resolution = h_track_resolution.GetMean()
                    track_resolution_rms = h_track_resolution.GetRMS()

                rms = math.sqrt(rms**2 - track_resolution**2)
                rmserr = math.sqrt(rmserr**2 + track_resolution_rms**2)

                out_hist.SetBinContent(output_bin,rms)
                out_hist.SetBinError(output_bin,rmserr)
            elif "Efficiency" in plot_name and not "Norm" in plot_name :
                h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))
                nevents = h_norm.GetBinContent(1)
                eff = h.GetBinContent(1)
                abs_err_down, abs_err_up = clopper_pearson_abs_err(nevents, eff)
                max_err = max(abs_err_down, abs_err_up)

                out_hist.SetBinContent(output_bin,eff)
                out_hist.SetBinError(output_bin,max_err)
            elif "Efficiency" in plot_name and "Norm" in plot_name :
                h_norm = f.Get(plot_path)
                nevents = h_norm.GetBinContent(1)

                out_hist.SetBinContent(output_bin,nevents)
                out_hist.SetBinError(output_bin,math.sqrt(nevents))
            else :
                mean = h.GetMean()
                rms = h.GetRMS()
                out_hist.SetBinContent(output_bin,mean)
                out_hist.SetBinError(output_bin,rms)

        if plot_name == "hClusterSize_Dut0" :
            y_axis_title = "average cluster size #pm RMS"
            out_hist.GetYaxis().SetRangeUser(0,4)
        elif "XResidualsClusterSize2" in plot_name and fit_size_2 :
            y_axis_title = "avg fitted X residual #sigma (#mum)"
            out_hist.GetYaxis().SetRangeUser(0,maxresidual)
        elif "YResidualsClusterSize2" in plot_name and fit_size_2 :
            y_axis_title = "avg fitted Y residual #sigma (#mum)"
            out_hist.GetYaxis().SetRangeUser(0,maxresidual)
        elif "XResiduals" in plot_name :
            y_axis_title = "X residual RMS (#mum)"
            out_hist.GetYaxis().SetRangeUser(0,maxresidual)
        elif "YResiduals" in plot_name :
            y_axis_title = "Y residual RMS (#mum)"
            out_hist.GetYaxis().SetRangeUser(0,maxresidual)
        elif "Landau" in plot_name :
            if fit_charge :
                y_axis_title = "fitted charge #pm (width #otimes #sigma) (electrons)"
            else :
                y_axis_title = "average charge #pm RMS (electrons)"
            out_hist.GetYaxis().SetRangeUser(0,25000)
        elif "Efficiency" in plot_name and not "Norm" in plot_name :
            y_axis_title = "efficiency"
            out_hist.GetYaxis().SetRangeUser(0.98,eff_ymax)
        elif "Efficiency" in plot_name and "Norm" in plot_name :
            y_axis_title = "n_tracks"

        out_hist.SetLineColor(colors[index])
        out_hist.SetMarkerColor(colors[index])

        ps.c.cd()
        out_hist.SetStats(0)
        out_hist.GetYaxis().SetTitle(y_axis_title)
        if "Landau" in plot_name :
            out_hist.GetYaxis().SetTitleOffset(2.1)
        elif "Efficiency" in plot_name :
            out_hist.GetYaxis().SetTitleOffset(2.1)
        else :
            out_hist.GetYaxis().SetTitleOffset(1.5)
        out_hist.SetMarkerStyle(20)
        out_hist.SetMarkerSize(1)
        out_hist.SetLineWidth(2)

        #if duplicate == 0 :
        #    out_hist.SetMarkerStyle(20)
        #    out_hist.SetMarkerSize(1)
        #    out_hist.SetLineWidth(2)
        #else :
        #    # making the duplicates distinguishable
        #    out_hist.SetMarkerStyle(23+duplicate)
        #    out_hist.SetMarkerSize(1.25)
        #    out_hist.SetLineWidth(1)
        ps.c.SetBottomMargin(0.10)
        ps.c.SetLeftMargin(0.15)
        ps.c.SetRightMargin(0.02)

        drawopt = ""
        if index != 0 :
            drawopt += "same "

        if out_hist.GetEntries() > 0 :
            out_hist.Draw(drawopt+"p E1")
        ps.update_canvas()

    # add y-axis gridlines for visibility
    ps.c.SetGridx()
    ps.c.SetGridy()
    leg = None
    leg = ps.c.BuildLegend(0.55,0.92,0.98,0.99)
    leg.SetNColumns(2)

    leg_primitives = leg.GetListOfPrimitives()

    for prim in leg_primitives :
        if "duplicate" in prim.GetLabel() :
            leg_primitives.Remove(prim)

    ps.update_canvas()

    primitives = ps.c.GetListOfPrimitives()
    primitive_hist = None
    for primitive in primitives :
        if issubclass(type(primitive), ROOT.TH1) :
            primitive_hist = primitive
    primitive_hist.SetTitle(plot_title)
    primitives.Remove(primitives.FindObject("title"))
    ps.update_canvas()

    ps.save(plot_name)

    if "Efficiency" in plot_name and not "Norm" in plot_name :
        hists[0].GetYaxis().SetRangeUser(0.8,eff_ymax)
        # I expected that ps.c.GetUymin/max would work, but it didn't for these so I hardcode instead
        #lines = drawLines(ps, hists[0], ordering, variations, 0.8, eff_ymax)
        ps.update_canvas()
        ps.save(plot_name+"_0.8to1")

        hists[0].GetYaxis().SetRangeUser(0,eff_ymax)
        #lines = drawLines(ps, hists[0], ordering, variations, 0, eff_ymax)
        ps.update_canvas()
        ps.save(plot_name+"_0to1")
        
if len(invalid_blocks) > 0 :
    print "The following blocks were invalid (maybe not in the right directory?)"
    for invalid in sorted(set(invalid_blocks)) :
        print invalid

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
