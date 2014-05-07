(TeX-add-style-hook "tables"
 (lambda ()
    (LaTeX-add-bibliographies
     "literature.bib")
    (TeX-run-style-hooks
     "latex2e"
     "art11"
     "article"
     "11pt"
     "../pct_positive"
     "../pcor_positive"
     "../pct_sig_pcor"
     "../pct_sig")))

