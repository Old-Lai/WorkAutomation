import os
from ebayFileProcessor import ebayReport
os.system('clear')

title  = "#######################\n"
title += "# Ebay Reconcile Tool #\n"
title += "#######################\n"

ebayProcessor = ebayReport()
ebayProcessor.title = title

ebayProcessor.readFile()
ebayProcessor.separateType()
ebayProcessor.processReports()