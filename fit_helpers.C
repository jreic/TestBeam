#include "TH1.h"
#include "TF1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TMath.h"


//-----------------------------------------------------------------------
// Taken from Chewie's ChargeUniMiB.cpp and Utilities.cpp
// (which itself is largely from https://github.com/cxx-hep/root-cern/blob/master/tutorials/fit/langaus.C)
//-----------------------------------------------------------------------
double langaus(double *x, double *par)
{
  double invsq2pi = 0.3989422804014;   // (2 pi)^(-1/2)
  double mpshift  = -0.22278298;       // Landau maximum location

  // Control constants
  double np = 100.0;      // number of convolution steps
  double sc =   5.0;      // convolution extends to +-sc Gaussian sigmas

  // Variables
  double xx;
  double mpc;
  double fland;
  double sum = 0.0;
  double xlow,xupp;
  double step;
  double i;


  // MP shift correction
  mpc = par[1] - mpshift * par[0];

  // Range of convolution integral
  xlow = x[0] - sc * par[3];
  xupp = x[0] + sc * par[3];

  step = (xupp-xlow) / np;

  // Convolution integral of Landau and Gaussian by sum
  for(i=1.0; i<=np/2; i++) {
    xx = xlow + (i-.5) * step;
    fland = TMath::Landau(xx,mpc,par[0]) / par[0];
    sum += fland * TMath::Gaus(x[0],xx,par[3]);

    xx = xupp - (i-.5) * step;
    fland = TMath::Landau(xx,mpc,par[0]) / par[0];
    sum += fland * TMath::Gaus(x[0],xx,par[3]);
  }

  return (par[2] * step * sum * invsq2pi / par[3]);
}



TF1* langausFit(TH1F* histo)
{
  TF1* langaus_ = new TF1("langaus",langaus,0,60000,4);
  TAxis* xAxis           ;
  double range           ;
  double integral        ;
  double gausPar      [3];
  double landauPar    [3];
  double fitRange     [2];
  double startValues  [4];
  double parsLowLimit [4];
  double parsHighLimit[4];

  TF1* landau = new TF1("myLandau","landau",0,60000);
  TF1* gaus   = new TF1("myGaus"  ,"gaus"  ,0,60000);

  fitRange[0]=0.4*(histo->GetMean());
  fitRange[1]=1.8*(histo->GetMean());

  gaus->SetRange(fitRange[0],fitRange[1]);
  histo->Fit(gaus,"0QR");
  for(int p=0; p<3; p++)
    gausPar[p] = gaus->GetParameter(p);

  landau->SetRange(fitRange[0],fitRange[1]);
  histo->Fit(landau,"0QR");
  for(int p=0; p<3; p++)
    landauPar[p] = landau->GetParameter(p);

  xAxis    = histo->GetXaxis();
  range    = xAxis->GetXmax() - xAxis->GetXmin();
  integral = ((histo->Integral())*range)/(histo->GetNbinsX());

  startValues[0]=landauPar[2];
  startValues[1]=landauPar[1];
  startValues[2]=integral    ;
  startValues[3]=gausPar[2]  ;

  parsLowLimit [0] = startValues[0] - 0.68*startValues[0];
  parsHighLimit[0] = startValues[0] + 0.68*startValues[0];
  parsLowLimit [1] = startValues[1] - 0.68*startValues[1];
  parsHighLimit[1] = startValues[1] + 0.68*startValues[1];
  parsLowLimit [2] = startValues[2] - 0.68*startValues[2];
  parsHighLimit[2] = startValues[2] + 0.68*startValues[2];
  parsLowLimit [3] = startValues[3] - 0.68*startValues[3];
  parsHighLimit[3] = startValues[3] + 0.68*startValues[3];

  langaus_->SetRange(fitRange[0],fitRange[1]);
  langaus_->SetParameters(startValues);
  langaus_->SetParNames("LWidth","MPV","Area","GSigma");

  for (int p=0; p<4; p++) {
    langaus_->SetParLimits(p, parsLowLimit[p], parsHighLimit[p]);
  }

  TFitResultPtr r = histo->Fit(langaus_,"RBL");
  int fitStatus = r;

  return langaus_;
}


//-----------------------------------------------------------------------
// gaus + pol0 fit for residuals of size 2 
// (where pol0 models misalignment)
//-----------------------------------------------------------------------
TF1* fitGausPol0(TH1F* histo)
{
  //float fitwidth = 2.0; // 2 sigma might be overkill since it starts to capture the tails?
  float fitwidth = 1.25; // 1.25 sigma is ~80% of events, so we can ignore just the tails
  float lower = histo->GetMean()-fitwidth*histo->GetStdDev();
  float upper = histo->GetMean()+fitwidth*histo->GetStdDev();

  TAxis* xAxis           ;
  double range           ;
  double integral        ;
  double gausPar      [3];
  double pol0Par      [1];
  double startValues  [4];
  double parsLowLimit [4];
  double parsHighLimit[4];

  TF1* pol0 = new TF1("myPol0","pol0",lower,upper);
  TF1* gaus = new TF1("myGaus","gaus",lower,upper);

  gaus->SetRange(lower, upper);
  histo->Fit(gaus,"0QR");
  for(int p=0; p<3; p++)
    gausPar[p] = gaus->GetParameter(p);

  pol0->SetRange(lower, upper);
  histo->Fit(pol0,"0QR");
  for(int p=0; p<1; p++)
    pol0Par[p] = pol0->GetParameter(p);

  xAxis    = histo->GetXaxis();
  range    = xAxis->GetXmax() - xAxis->GetXmin();
  integral = ((histo->Integral())*range)/(histo->GetNbinsX());

  startValues[0]=gausPar[0];
  startValues[1]=gausPar[1];
  startValues[2]=gausPar[2];
  startValues[3]=pol0Par[0];

  parsLowLimit [0] = startValues[0] - 0.68*startValues[0];
  parsHighLimit[0] = startValues[0] + 0.68*startValues[0];
  parsLowLimit [1] = startValues[1] - 0.68*startValues[1];
  parsHighLimit[1] = startValues[1] + 0.68*startValues[1];
  parsLowLimit [2] = startValues[2] - 0.68*startValues[2];
  parsHighLimit[2] = startValues[2] + 0.68*startValues[2];

  // Need to allow the pol0 pars to float further than the others
  parsLowLimit [3] = startValues[3] - startValues[3];
  parsHighLimit[3] = startValues[3] + startValues[3];

  TF1* gauspol0_ = new TF1("gauspol0","gaus(0)+pol0(3)",lower,upper);
  gauspol0_->SetRange(lower, upper);
  gauspol0_->SetParameters(startValues);
  gauspol0_->SetParNames("Constant","Mean","Sigma","pol0");

  for (int p=0; p<4; p++) {
    gauspol0_->SetParLimits(p, parsLowLimit[p], parsHighLimit[p]);
  }

  TFitResultPtr r = histo->Fit(gauspol0_,"RBL");
  int fitStatus = r;

  return gauspol0_;
}
