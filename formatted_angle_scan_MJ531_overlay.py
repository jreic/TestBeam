from ROOTTools import *
import sys
import numpy as np
import math

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning


ps = plot_saver(plot_dir("formatted_angle_scan_MJ531_overlay_cosine"), size=(600,600), log=False, pdf=True)
ps.c.SetLeftMargin(0.1)
ps.c.SetTopMargin(0.05)
ps.c.SetRightMargin(0.05)
ps.update_canvas()

ps2 = plot_saver(plot_dir("formatted_angle_scan_MJ531_overlay_cosine_supporting_plots"), size=(600,600), log=False, pdf=True)
ps2.c.SetLeftMargin(0.1)
ps2.c.SetTopMargin(0.05)
ps2.c.SetRightMargin(0.05)
ps2.update_canvas()

plot_paths = [] 
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize2_Dut0")


for plot_path in plot_paths :
    plot_name = plot_path.split("/")[-1]

    fpath0deg   = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46657_46667.root"
    fpath4deg   = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46668_46675.root"
    fpath8deg   = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46676_46682.root"
    fpath10deg  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46683_46690.root"
    fpath12deg  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46691_46697.root"
    fpath16deg  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46698_46704.root"
    fpath20deg  = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput_blocks_realign_angle_scan/Chewie_Runs46705_46711.root"

    files_anglescan = [ ROOT.TFile(fpath0deg)
            , ROOT.TFile(fpath4deg)
            , ROOT.TFile(fpath8deg)
            , ROOT.TFile(fpath10deg)
            , ROOT.TFile(fpath12deg)
            , ROOT.TFile(fpath16deg)
            , ROOT.TFile(fpath20deg)
            ]

    labels_anglescan = [0, 4, 8, 10, 12, 16, 20]

    graphs = []

    # keeping the structure from the bias scan script, where we actually do loop over multiple versions of these!
    datasets = [files_anglescan]
    labels = [labels_anglescan]

    for index_dataset in xrange(0, len(datasets)) :
        files = datasets[index_dataset]

        x = []
        y = []
        exl = []
        exh = []
        eyl = []
        eyh = []

        for index in xrange(0,len(files)) :
            f = files[index]
            angle = labels[index_dataset][index]
            
            # use a plot saver instance to save all of the relevant plots
            ps2.c.cd()

            # the plot and fit itself
            h = f.Get(plot_path)
            h.SetName(plot_name.replace("_Dut0","") + " %s#circ" % str(angle))
            gauspol0 = ROOT.fitGausPol0(h, 1.65*h.GetStdDev())
            fit = h.Fit(gauspol0, "RBLSQ")

            # make plots only for the nominal
            ps2.update_canvas()
            ps2.save(plot_name+"_"+str(angle))

            # extract residual and fit stat err from the fit result
            residual = fit.Parameter(2)
            err_stat = fit.ParError(2)

            # Set uncertainty by taking maximum of several fit range alternatives (1.5*RMS, 2*RMS, i.e. roughly 5% wider or narrower window)
            gauspol0_1p5RMS = ROOT.fitGausPol0(h, 1.5*h.GetStdDev())
            fit_1p5RMS = h.Fit(gauspol0_1p5RMS, "RBLSQ")
            residual_1p5RMS = fit_1p5RMS.Parameter(2)

            gauspol0_2RMS = ROOT.fitGausPol0(h, 2*h.GetStdDev())
            fit_2RMS = h.Fit(gauspol0_2RMS, "RBLSQ")
            residual_2RMS = fit_2RMS.Parameter(2)

            err_syst = max( abs(residual - residual_1p5RMS), abs(residual - residual_2RMS) )
            err = math.sqrt(err_stat**2 + err_syst**2)

            # Subtract off the telescope resolution!

            # Took telescope resolution from https://home.fnal.gov/~joeyr/TFPX/Chewie_Runs46657_46667/#hPredictedXErrors_Dut0. This is from the normal incidence data, i.e. it is the minimum of its resolution across the run blocks considered, which means we are not subtracting enough for the large angles. However, it only varies by a few percent overall, so not a huge deal.
            # Also note telescope X is DUT Y, and telescope Y is DUT X, and I am taking the mean value over the predicted errors distribution
            
            # update on 11/14/2023--too bad I have to hardcode this for now
            if index == 0 :
                xtele = 4.288
                ytele = 3.884
            if index == 1 :
                xtele = 4.292
                ytele = 3.889
            if index == 2 :
                xtele = 4.325
                ytele = 3.896
            if index == 3 :
                xtele = 4.359
                ytele = 3.905
            if index == 4 :
                xtele = 4.390
                ytele = 3.912
            if index == 5 :
                xtele = 4.475
                ytele = 3.928
            if index == 5 :
                xtele = 4.605
                ytele = 3.961

            # correct telescope resolution by 1/cos(angle), to account for the projection of the resolution onto the DUT's plane
            # i.e., note that the telescope's effective resolution at huge DUT turn angles is much worse than at normal incidence!
            # Also note that this is ONLY done for the telescope x / DUT y here, because that is the direction we rotated. If we rotated in the other axis, we would have to adjust that one instead!
            xtele = xtele / math.cos(math.radians(angle))

            if "XResiduals" in plot_name :
                residual = math.sqrt( residual**2 - ytele**2 )
            elif "YResiduals" in plot_name :
                residual = math.sqrt( residual**2 - xtele**2 )

            x.append(angle)
            y.append(residual)
            exl.append(1)
            exh.append(1)
            eyl.append(err)
            eyh.append(err)

        x = np.array(x, dtype='double')
        y = np.array(y, dtype='double')
        exl = np.array(exl, dtype='double')
        exh = np.array(exh, dtype='double')
        eyl = np.array(eyl, dtype='double')
        eyh = np.array(eyh, dtype='double')

        graph = ROOT.TGraphAsymmErrors(len(x),x,y,exl,exh,eyl,eyh)

        graph.SetTitle("CNM, 1.2#times10^{16} n_{eq}/cm^{2}, 1200e, bias = 100V")
        graph.SetLineColor(ROOT.kBlack)
        graph.SetMarkerColor(ROOT.kBlack)
        graph.SetMarkerStyle(20)
        graph.SetFillColor(0)

        if "Residual" in plot_name :
            xmin = 0
            xmax = 22
            ymin = 4
            ymax = 10
            #ymin = 0
            #ymax = 20

            graph.GetXaxis().SetRangeUser(xmin, xmax)
            graph.GetYaxis().SetRangeUser(ymin, ymax)

            graph.GetXaxis().SetTitleOffset(1.25)
            graph.GetXaxis().SetTitle("Rotation Angle [#circ]")

            graph.GetYaxis().SetTitleOffset(1.4)
            graph.GetYaxis().SetTitle("Resolution [#mum]")

        graphs.append(graph)

        ps.c.cd()
        graph.Draw("AP")
        ps.update_canvas()

    leg = ROOT.gPad.BuildLegend(0.35, 0.7, 0.9, 0.85)
    leg.SetBorderSize(0)

    ps.update_canvas()
    ps.save(plot_name)

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
    printout += " and "
    httpdir = "https://home.fnal.gov/~" + ps2.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
