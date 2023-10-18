from ROOTTools import *
import sys

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptFit(0o0100) # adds Landau MPV to stat box
ROOT.gStyle.SetOptStat(0) # adds Landau MPV to stat box
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gROOT.ProcessLine(".L fit_helpers.C+")
ROOT.gErrorIgnoreLevel = ROOT.kWarning

filepath = "/uscms/home/joeyr/nobackup/MJ531_studies_for_paper/ChewieOutput/"
outname = "MJ531_run_by_run_additional_bias_scan"

runNumbers = [
46712, 46713, 46714, 46715, 46716, 46719, 46720, 46721, 46722, 46723, 46724, 46725, 46726, 46727, 46728, 46729, 46730, 46731, 46738, 46739, 46740, 46741, 46742, 46743, 46744, 46745, 46746, 46747, 46748, 46749, 46750, 46752, 46753, 46754, 46755, 46756, 46757, 46758, 46759, 46760, 46761, 46767, 46762, 46763, 46764, 46765, 46766, 46768, 46769, 46771, 46772, 46773, 46777, 46778,]
#46626, 46627, 46628, 46629, 46630, 46634, 46639, 46640, 46641, 46642, 46643, 46644, 46645, 46646, 46647, 46648, 46650, 46651, 46652, 46653, 46654, 46655, 46656, 46657, 46658, 46659, 46660, 46662, 46664, 46665, 46666, 46667, 46668, 46669, 46670, 46671, 46672, 46673, 46674, 46675, 46676, 46677, 46678, 46679, 46680, 46681, 46682, 46683, 46684, 46685, 46687, 46688, 46689, 46690, 46691, 46692, 46693, 46694, 46695, 46696, 46697, 46698, 46699, 46700, 46701, 46702, 46703, 46704, 46705, 46706, 46707, 46708, 46709, 46710, 46711, 46712, 46713, 46714, 46716, 46771, 46772, 46773, 51142, 51149, 51150, 51151, 51152, 51153, 51154, 51155, 51156, 51158, 51159, 51160, 51162, 51164, 51165, 51166, 51169, 51170, 51171, 51173, 51174, 51175, 51176, 51177, 51178, 51179, 51180, 51181, 51182, 51183, 51184, 51186, 51187, 51188, 51189, 51190, 51191, 51192, 51193, 51194, 51195, 51196, 51197, 51198, 51199, 51201, 51202, 51208, 51210, 51211, 51212, 51213, 51214, 51216, 51217, 51219, 51221, 51222, 51224, 51226, 51227, 51228, 51230, 51231, 51233, 51234, 51235, 51236, 51237, 51238, 51239, 51240, 51241, 51242, 51243, 51244, 51245, 51246, 51247, 51279, 51280, 51281, 51282, 51283, 51284, 51285, 51286, 51287, 51288]

# to save our plots
ps = plot_saver(plot_dir(outname.split(".")[0]), size=(2600,600), log=False, pdf=True)

# histogram paths within the ROOT file
plot_paths = []
plot_paths.append("Efficiency/Dut0/Efficiency/Efficiency_Dut0")
plot_paths.append("Efficiency/Dut0/Efficiency/EfficiencyRef_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResiduals_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResiduals_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize1_Dut0")
plot_paths.append("Resolution/Dut0/XResiduals/hXResidualsClusterSize2_Dut0")
plot_paths.append("Resolution/Dut0/YResiduals/hYResidualsClusterSize2_Dut0")
plot_paths.append("Resolution/Dut0/Errors/hPredictedXErrors_Dut0")
plot_paths.append("Resolution/Dut0/Errors/hPredictedYErrors_Dut0")
plot_paths.append("Charge/Dut0/ClusterSize/hClusterSize_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSizeUpToMax_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize1_Dut0")
plot_paths.append("Charge/Dut0/Landau/hLandauClusterSize2_Dut0")

output_plots_mean = []
output_plots_rms = []
for plot_path in plot_paths :
    prefix = plot_path.split("/")[-1]
    plot_name = prefix+"_mean"

    if "Efficiency" in prefix :
        plot_name = prefix

    h_mean = ROOT.TH1F(plot_name, plot_name, len(runNumbers), runNumbers[0], runNumbers[-1]+1)
    for index, runNumber in enumerate(runNumbers) :
        h_mean.GetXaxis().SetBinLabel(index+1, str(runNumber))

    h_mean.GetXaxis().SetTitle("run number")
    h_mean.GetXaxis().SetTitleOffset(1.55)
    h_mean.GetYaxis().SetTitle("efficiency" if "Efficiency" in plot_name else "mean")
    h_mean.GetYaxis().SetTitleOffset(0.47)
    output_plots_mean.append(h_mean)

    plot_name = prefix+"_rms"
    if "Efficiency" in prefix :
        plot_name = prefix+"_uncert"

    h_rms = h_mean.Clone(plot_name)
    h_rms.SetTitle(plot_name)
    h_rms.GetYaxis().SetTitle("max uncert" if "Efficiency" in plot_name else "rms")
    output_plots_rms.append(h_rms)


for i_runNumber, runNumber in enumerate(runNumbers) :

    ibin = i_runNumber+1

    # the ROOT file
    f = ROOT.TFile(filepath+"Chewie_Run%i.root" % runNumber)

    for i_plot_path, plot_path in enumerate(plot_paths) :
        ROOT.gStyle.SetOptTitle(1)
        h = f.Get(plot_path)
        if not h : 
            print("%s not found, skipping" % plot_path)
            continue
        plot_name = plot_path.split("/")[-1]

        # draw charge distributions with their Landau x Gaussian fits
        #if "Landau" in plot_name and h.GetEntries() > 0 :
        #    langaus = ROOT.langausFit(h)
        #    fit = h.Fit(langaus, "RBLSQ")
        #    h.GetXaxis().SetRangeUser(0, 25000)
        #    h.Draw()
        # FIXME here could get the fit result

        if "Efficiency" in plot_path :
            h_norm = f.Get(plot_path.replace("_Dut0","Norm_Dut0"))

            eff = h.GetBinContent(1)
            nevents = h_norm.GetBinContent(1)
            uncert = max(clopper_pearson_abs_err(nevents, eff))

            output_plots_mean[i_plot_path].SetBinContent(ibin, eff)
            output_plots_rms[i_plot_path].SetBinContent(ibin, uncert)

        else :
            mean = h.GetMean()
            rms = h.GetRMS()

            output_plots_mean[i_plot_path].SetBinContent(ibin, mean)
            output_plots_rms[i_plot_path].SetBinContent(ibin, rms)

for i_plot_path, plot_path in enumerate(plot_paths) :

    hist = output_plots_mean[i_plot_path]
    hist.Draw()
    
    ps.c.SetMargin(0.03,0.01,0.1,0.1)
    ps.save(hist.GetName())


    hist = output_plots_rms[i_plot_path]
    hist.Draw()
    
    ps.c.SetMargin(0.03,0.01,0.1,0.1)
    ps.save(hist.GetName())

printout = "\nDone! Outputs are at %s" % ps.plot_dir
if ps.plot_dir.startswith('/publicweb/') :
    httpdir = "https://home.fnal.gov/~" + ps.plot_dir[len("/publicweb/*/"):]
    printout += " (%s)" % httpdir
print(printout)
