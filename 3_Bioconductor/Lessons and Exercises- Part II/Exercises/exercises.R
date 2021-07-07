# Exercise 1

# Consider the series GSE87495 from the GEO platform
# This series contains 6 samples of human cells in two conditions:
#   - 3 samples treated with doxycycline
#   - 3 samples with no doxycycline
# Read the csv file "GSE87495_counts.csv" into a dataframe df
# The last 6 columns contain the counts for each sample  
df = read.csv("GSE87495_counts.csv")

# We want to change the names of the samples of the dataset
# Define the variable "samples"
samples = c("no_dox_1", "with_dox_2", "no_dox_3",
             "with_dox_4", "no_dox_5", "with_dox_6")

# Change the df column names related to the samples using the names in the 
# variable "samples" defined previously


# Create SummarizedExperiment object SE: subset df (counts and genes) and assign colnames and rownames to the ones created.
# assay name must be "exp1"
# colData is a 6 x 1 dataframe with a STATUS variable "no_dox" or "with_dox" based on colnames
# Add dataType="rseq" as metadata.
# Shows the structure and its elements


#-------------------------------------------------------------------

#Exercise 2

# Create a new SummarizedExperiment DOX with only sample with dox from the 
# SummarizedExperiment of the previous Exercise


# Create a new random assay(matrix) and add it to DOX (values from normal distribution with mean = 0 and sd = 1)
# Hint: you can create a new SummarizedExperiment with 2 assays or replace the assays(DOX) list
# Hint: dimensions of the assays must be the same

# Select data of the gene with ENTREZID = 100288801


#-------------------------------------------------------------------

# Exercise 3

# Build a RangedSummarizedExperiment from the SummarizedExperiment SE (Exercise 1)
# adding to SE the following GRanges:
# - seqnames
# - ranges
# - strand
# - type

#Show the class of SE


# Donwload from AnnotationHub gtf file for Homo Sapiens 
# use the Ensembl database consider the GRCh37 genome (h19)
# Filter the SE row according to the GRanges obtained from GRanges obtained from AnnotationHub 
# How much rows have been removed?

#-------------------------------------------------------------------

# Exercise 4

# From the MultiAssayExperiment miniACC select only assay RNASeq2GeneNorm and miRNASeqGene
# This two assays have rows in common? Show the results
# This two assays have columns in common? Show the results
# show the number of male and female in the MultiAssayExperiment
# Select only female sample by creating a new MultiAssayExperiment called female
# From female add a new experiment as matrix with row and col equals to RNAseq but random data


#-------------------------------------------------------------------


#Exercise 5


# Try to extract the first SummarizedExperiment from miniACC using [ e [[
# Are there differences in the obtained results?
# Is it possible to extract samples with vital_status = 0?
# Motivate the answers

# Using the two methods [ and [[ in combination it is possible to set correctly
# colData(...)=colData(...)
# Is it possible to extract samples with vital_status = 0? Try


# Then try extracting the SummarizedExperiment using the getWithColData method (type ?getWithColData)
# Is it possible to extract samples with vital_status = 0?
# Motivate the answer


#-------------------------------------------------------------------

#Exercise 6

# Download TGCA Data for disease UCEC (only assay RNASeqGene and miRNASeqGene)

# Extract the SummarizedExperiment RNASeqGene from this MultiAssayExperiment 
# with all the methods seen in the previous exercise. Make sure colData is not empty.
# Hint: print ncol(assay) and nrow(colData).
# Hint: use the fuction anyReplicated (?anyReplicated) and mergeReplicates (?mergeReplicates)

# Try doing this exercise again without using the marging features (mergeReplicates)
# Hint: print colnames() and rownames().
# Hint: converting the colnames names of the SummarizedExperiment assay into the barcode
# containing only the patient information it is possible to identify (and remove) 
# the duplicates with the classic summarized operations. 
# TCGAbarcode(..., participant = TRUE)


#-------------------------------------------------------------------

#Exercise 7

# Create a MultiAssayExperiment with:
# - a SummarizedExperiment with 2 assays containing counts of 6 samples and 50 genes, samples information include 
#   Condition (control or case, randomly assigned with probability 50%) and samples are named sample1, sample2...
# - a matrix with 30 rows (named with "hsa_" and a random number) and 4 columns (called array1, array2...)
# Create also a data.frame with patients data (sex and name) and define a mapping for the SummarizedExperiment and matrix just created.


