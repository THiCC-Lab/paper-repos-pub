from process_text import process_text
from hdm_read import hdm_read

fname_in = "sample_text.txt"
fname_processed = "sample_out.txt"
process_text(fname_in, fname_processed)
hdm_read(fname_processed)