from ROOTTools import *
import sys
import math

ROOT.gStyle.SetOptFit(0100) # adds Landau MPV to stat box

chewie_output_dir = "Chewie_Runs15067_15078"

ps = plot_saver(plot_dir("eff_uncertainties_"+chewie_output_dir), size=(600,600), pdf=True, log=False)
ps.c.SetRightMargin(0.15)
ps.update_canvas()

plot_names = [ 
               "2DEfficiencyRefRebin8Reformatted_Dut0"
              ,"2DEfficiencyRefNormRebin8Reformatted_Dut0"
             ]


fpathEff = "/uscms/home/joeyr/publicweb/TFPX/"+chewie_output_dir+"/"+plot_names[0]+".root"
fpathDen = "/uscms/home/joeyr/publicweb/TFPX/"+chewie_output_dir+"/"+plot_names[1]+".root"

fEff = ROOT.TFile(fpathEff)
fDen = ROOT.TFile(fpathDen)

cEff = fEff.Get("c0")
print plot_names[0].replace("Reformatted","")
print plot_names[1].replace("Reformatted","")
hEff = cEff.GetPrimitive(plot_names[0].replace("Reformatted",""))

cDen = fDen.Get("c0")
hDen = cDen.GetPrimitive(plot_names[1].replace("Reformatted","").replace("2D",""))

hUncDown = hDen.Clone("hUncDown")
hUncDown.SetTitle("2D efficiency Clopper-Pearson uncertainty (down)")
hUncDown.Reset()

hUncUp = hDen.Clone("hUncUp")
hUncUp.SetTitle("2D efficiency Clopper-Pearson uncertainty (up)")
hUncUp.Reset()

for ibinx in xrange(0,hEff.GetNbinsX()+2) :
    for ibiny in xrange(0,hEff.GetNbinsY()+2) :
        den = hDen.GetBinContent(ibinx,ibiny)
        eff = hEff.GetBinContent(ibinx,ibiny)
        num = eff*den

        if den == 0 : 
            cp_eff = 0
            cp_unc_down = 0
            cp_unc_up = 0
        else :
            cp_eff,cp_unc_down,cp_unc_up = clopper_pearson(num,den)

        #unc = math.sqrt( num*num*(num+den) / den**3 ) # Poisson
        #if den == 0 : den = 1
        #unc = math.sqrt( eff*(1-eff) / den ) # binomial

        if den != 0 and cp_unc_up == cp_eff :
            cp_unc_up += 1e-6 # just so the up error isn't empty

        #print ibinx, ibiny, den, eff, unc
        hUncDown.SetBinContent(ibinx, ibiny, cp_eff-cp_unc_down)
        hUncUp.SetBinContent(ibinx, ibiny, cp_unc_up-cp_eff)

ps.c.cd()
hUncDown.Draw("colz")
ps.save("efficiency_uncertainty_down")

hUncUp.Draw("colz")
ps.save("efficiency_uncertainty_up")
