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

        print("Integrated hCellEfficiency_Dut0 efficiency is "+str(num/den))

    # FIXME these will be wrong for other run configurations
    if "Landau" in plot_name :
        if "16477_16484" in filename :
            h.Fit("landau","","",1800,25000)
        elif "16446_16455" in filename :
            h.Fit("landau","","",2300,25000)
        else :
            h.Fit("landau","","",2800,25000)

        h.GetXaxis().SetRangeUser(0,25000)

    # Plot TH2's with colz and no stat box
    if issubclass(type(h), ROOT.TH2) :
        h.SetStats(0)
        h.Draw("colz")
    else :
        h.Draw()

    ps.save(plot_name)


    # now plot rebinned efficiency maps
    if plot_name == "2DEfficiencyRef_Dut0" :
        h_den_default_binning = f.Get(plot_path.replace("EfficiencyRef","EfficiencyRefNorm"))
        h_num_default_binning = h.Clone("2DEfficiencyRefNum_Dut0")
        h_num_default_binning.Multiply(h_num_default_binning,h_den_default_binning)

        for rebinFactor in [2,4,8] :
            h_num = h_num_default_binning.Clone("2DEfficiencyRefNumRebin%s_Dut0" % rebinFactor)
            h_den = h_den_default_binning.Clone("EfficiencyRefNormRebin%s_Dut0" % rebinFactor)
            h_num.Rebin2D(rebinFactor,rebinFactor)
            h_den.Rebin2D(rebinFactor,rebinFactor)
            h_eff = h_num.Clone("2DEfficiencyRefRebin%s_Dut0" % rebinFactor)
            h_eff.SetTitle("2D efficiency distribution rebin%s Dut0" % rebinFactor)
            h_eff.Divide(h_num,h_den)

            h_eff.SetStats(0)
            h_eff.Draw("colz")
            ps.save("2DEfficiencyRefRebin%s_Dut0" % rebinFactor)

            # formatting only for large rebinning
            if rebinFactor >= 8 :

                # format x-axis
                x_start = 129
                x_end = 264
                h_eff.GetXaxis().SetRangeUser(x_start,x_end+1)
                for xbin in xrange(x_start,x_end,rebinFactor) :
                    ibinx = h_eff.GetXaxis().FindBin(xbin)
                    h_eff.GetXaxis().SetBinLabel(ibinx, "%s-%s" % (xbin, xbin+rebinFactor-1) )

                # format y-axis
                y_start = 1
                y_end = 192
                h_eff.GetYaxis().SetRangeUser(y_start,y_end+1)
                for ybin in xrange(y_start,y_end,rebinFactor) :
                    ibiny = h_eff.GetYaxis().FindBin(ybin)
                    h_eff.GetYaxis().SetBinLabel(ibiny, "%s-%s" % (ybin, ybin+rebinFactor-1) )

                # remove tickmarks; otherwise we'd need to play around here a bit more to get them aligned right
                h_eff.GetXaxis().SetTickLength(0)
                h_eff.GetYaxis().SetTickLength(0)

                # move "row" label
                h_eff.GetYaxis().SetTitle("")
                tlatex = ROOT.TLatex()
                tlatex.SetTextSize(0.04)
                tlatex.SetTextFont(42)
                tlatex.DrawLatexNDC(0.025,0.9,"row")

                h_eff.SetStats(0)
                h_eff.Draw("colz")
                ps.save("2DEfficiencyRefRebin%sReformatted_Dut0" % rebinFactor)


print "FIXME for landau fits per run block"
