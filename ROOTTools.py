#!/usr/bin/env python

import sys, os, ROOT

# keep ROOT from parsing out -h/--help
_saved = []
for _x in '-h', '--help':
    _i = -1
    if _x in sys.argv:
        _i = sys.argv.index(_x)
    if _i >= 0:
        _saved.append((_i,_x))
        sys.argv.remove(_x)
sys.argv.append('-b')     # Start ROOT in batch mode;
import ROOT; ROOT.TCanvas # make sure libGui gets initialized while '-b' is specified;
sys.argv.remove('-b')     # and don't mess up sys.argv.
for _off, (_i, _x) in enumerate(_saved):
    sys.argv.insert(_i+_off, _x)

def plot_dir(x='', make=False, temp=False):
    hostname = os.environ['HOSTNAME']
    username = os.environ['USER']
    d = None
    if 'fnal.gov' in hostname :
        d = '/publicweb/%s/%s/TFPX' % (username[0],username)
        if not os.path.isdir(d) :
            d = '~/nobackup/chewie_plots/'
        #d = '~/nobackup/copy_to_classe'
    elif 'classe.cornell.edu' in hostname :
        d = '~/public_html/TFPX'
    if d:
        x = os.path.join(d,x)
    else:
        raise NotImplementedError("can't handle host %s and user %s" % (hostname, username))
    if make:
        try:
            os.makedirs(x)
        except OSError:
            pass
    return x

class plot_saver:
    i = 0
    
    def __init__(self, plot_dir=None, html=True, log=True, root=True, root_log=False, pdf=False, pdf_log=False, C=False, C_log=False, size=(820,630), per_page=-1, canvas_margins=None):
        self.c = ROOT.TCanvas('c%i' % plot_saver.i, '', *size)
        if canvas_margins is not None:
            if type(canvas_margins) == int or type(canvas_margins) == float:
                top, bottom, left, right = tuple(canvas_margins for x in xrange(4))
            else:
                top, bottom, left, right = canvas_margins
            self.c.SetTopMargin(top)
            self.c.SetBottomMargin(bottom)
            self.c.SetLeftMargin(left)
            self.c.SetRightMargin(right)
        plot_saver.i += 1
        self.saved = []
        self.html = html
        self.set_plot_dir(plot_dir)
        self.log = log
        self.root = root
        self.root_log = root_log
        self.pdf = pdf
        self.pdf_log = pdf_log
        self.C = C
        self.C_log = C_log
        self.per_page = per_page

    def __del__(self):
        self.write_index()

    def update_canvas(self):
        self.c.Update()

    def anchor_name(self, fn):
        return os.path.splitext(os.path.basename(fn))[0].replace('.', '_').replace('/', '_')
    
    def write_index(self):
        if not self.saved or not self.html:
            return
        html = open(os.path.join(self.plot_dir, 'index.html'), 'wt')
        if self.per_page > 0:
            nsaved = len(self.saved)
            ndxs = range(0, nsaved, self.per_page)
            npages = len(ndxs)
            for page, ndx in enumerate(ndxs):
                self.write_index_page(self.saved[ndx:ndx+self.per_page], page, npages)
        else:
            self.write_index_page(self.saved, 0, 1)
            
    def write_index_page(self, saved, page, num_pages):
        def html_fn(page):
            if page == 0:
                return 'index.html'
            else:
                return 'index_%i.html' % page
            return 
        html = open(os.path.join(self.plot_dir, html_fn(page)), 'wt')
        html.write('<html><head><title>%s</title></head><body><pre>\n' % self.plot_dir.split('/')[-1])
        def write_pages_line():
            html.write('pages: ')
            for i in xrange(num_pages):
                if i == page:
                    html.write('<b>%i</b>  ' % i)
                else:
                    html.write('<a href="%s">%i</a>  ' % (html_fn(i), i))
            html.write('\n')
        if num_pages > 1:
            write_pages_line()
        html.write('<a href="..">.. (parent directory)</a>\n')
        for i, save in enumerate(saved):
            if type(save) == str:
                # this is just a directory link
                html.write('<a href="%s">%10i%32s%s</a>\n' % (save, i, 'change directory: ', save))
                continue

            fn, log, root, root_log, pdf, pdf_log, C, C_log = save

            bn = os.path.basename(fn)
            html.write('<a href="#%s">%10i</a> ' % (self.anchor_name(fn), i))
            if log:
                html.write(' <a href="%s">log</a>' % os.path.basename(log))
            else:
                html.write('    ')
            if root:
                html.write(' <a href="%s">root</a>' % os.path.basename(root))
            else:
                html.write('     ')
            if root_log:
                html.write(' <a href="%s">root_log</a>' % os.path.basename(root_log))
            else:
                html.write('     ')
            if pdf:
                html.write(' <a href="%s">pdf</a>' % os.path.basename(pdf))
            else:
                html.write('     ')
            if pdf_log:
                html.write(' <a href="%s">pdf_log</a>' % os.path.basename(pdf_log))
            else:
                html.write('     ')
            if C:
                html.write(' <a href="%s">C</a>' % os.path.basename(C))
            else:
                html.write('     ')
            if C_log:
                html.write(' <a href="%s">C_log</a>' % os.path.basename(C_log))
            else:
                html.write('     ')
            html.write('  <a href="%s">%s</a>' % (bn, bn))
            html.write('\n')
        html.write('<br><br>')
        for i, save in enumerate(saved):
            if type(save) == str:
                continue # skip dir entries
            fn, log, root, root_log, pdf, pdf_log, C, C_log = save
            bn = os.path.basename(fn)
            rootlink = ', <a href="%s">root</a>' % os.path.basename(root) if root else ''
            html.write('<h4 id="%s"><a href="#%s">%s</a>%s</h4><br>\n' % (self.anchor_name(fn), self.anchor_name(fn), bn.replace('.png', ''), rootlink))
            if log:
                html.write('<img src="%s"><img src="%s"><br><br>\n' % (bn, os.path.basename(log)))
            else:
                html.write('<img src="%s"><br><br>\n' % bn)
        if num_pages > 1:
            write_pages_line()
        html.write('</pre></body></html>\n')
        
    def set_plot_dir(self, plot_dir):
        self.write_index()
        self.saved = []
        if plot_dir is not None and '~' in plot_dir:
            plot_dir = os.path.expanduser(plot_dir)
        self.plot_dir = plot_dir
        if plot_dir is not None:
            os.system('mkdir -p %s' % self.plot_dir)

    def save_dir(self, n):
        if self.plot_dir is None:
            raise ValueError('save_dir called before plot_dir set!')
        self.saved.append(n)

    def save(self, n, log=None, root=None, root_log=None, pdf=None, pdf_log=None, C=None, C_log=None, logz=None, other_c=None):
        can = self.c if other_c is None else other_c

        if logz:
            logfcn = can.SetLogz
        else:
            logfcn = can.SetLogy

        log = self.log if log is None else log
        root = self.root if root is None else root
        root_log = self.root_log if root_log is None else root_log
        pdf = self.pdf if pdf is None else pdf
        pdf_log = self.pdf_log if pdf_log is None else pdf_log
        C = self.C if C is None else C
        C_log = self.C_log if C_log is None else C_log
        
        if self.plot_dir is None:
            raise ValueError('save called before plot_dir set!')
        can.SetLogy(0)
        fn = os.path.join(self.plot_dir, n + '.png')
        can.SaveAs(fn)
        if root:
            root = os.path.join(self.plot_dir, n + '.root')
            can.SaveAs(root)
        if root_log:
            logfcn(1)
            root_log = os.path.join(self.plot_dir, n + '_log.root')
            can.SaveAs(root_log)
            logfcn(0)
        if log:
            logfcn(1)
            log = os.path.join(self.plot_dir, n + '_log.png')
            can.SaveAs(log)
            logfcn(0)
        if pdf:
            pdf = os.path.join(self.plot_dir, n + '.pdf')
            can.SaveAs(pdf)
        if pdf_log:
            logfcn(1)
            pdf_log = os.path.join(self.plot_dir, n + '_log.pdf')
            can.SaveAs(pdf_log)
            logfcn(0)
        if C:
            C = os.path.join(self.plot_dir, n + '.C')
            can.SaveAs(C_fn)
        if C_log:
            logfcn(1)
            C_log = os.path.join(self.plot_dir, n + '_log.C')
            can.SaveAs(C_log)
            logfcn(0)
        self.saved.append((fn, log, root, root_log, pdf, pdf_log, C, C_log))

def clopper_pearson(n_on, n_tot, alpha=1-0.6827, equal_tailed=True):
    if equal_tailed:
        alpha_min = alpha/2
    else:
        alpha_min = alpha

    lower = 0
    upper = 1

    if n_on > 0:
        lower = ROOT.Math.beta_quantile(alpha_min, n_on, n_tot - n_on + 1)
    if n_tot - n_on > 0:
        upper = ROOT.Math.beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on)

    if n_on == 0 and n_tot == 0:
        return 0, lower, upper
    else:
        return float(n_on)/n_tot, lower, upper

def clopper_pearson_poisson_means(x, y, alpha=1-0.6827):
    r, rl, rh = clopper_pearson(x, x+y, alpha)
    pl = rl/(1-rl)
    if y == 0 or abs(rh - 1) < 1e-9:
        return None, pl, None
    return r/(1-r), pl, rh/(1 - rh)


__all__ = [
    'plot_dir',
    'plot_saver',
    'ROOT',
    'clopper_pearson',
    'clopper_pearson_poisson_means',
    ]
