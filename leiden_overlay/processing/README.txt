#--- Single Genes ---#
For single gene data, all that needs to be run is the "./run_script.sh" BASH script.

For example, if the data is wanted for the dysferlin gene (DYSF) variants from Leiden,
type in './run_script.sh DYSF' into the terminal.

The results are then outputted into the ../results/ folder, with a separate one
for each gene (labelled by the gene abbreviation).

#--- All Genes ---#
To run this script for all the genes in the Leiden database together, all that
needs to be run is the "./big_script.sh" BASH script (no arguments necessary).


#--- The Leiden Matrix ---#
To create the Leiden Matrix (a complete matrix of all the variants for all genes
inside the Leiden database, with their pathogenicity, ExAC frequency, etc. all
noted), first run the script for all the genes as mentioned above (i.e. run
"./big_script.sh"). Then, run "./finish_mat.sh" with no arguments to create the
full matrix as "big_mat.txt" within the current "processing" folder. This is a
tab delimited file that can hence be opened in Excel or other spreadsheet software.
