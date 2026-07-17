#!/usr/bin/env python
#   Script to convert Illumina sequences with bracket notation to FASTA with IUPAC codes
#   Input: tab-delimited file with SNP name and sequence containing [A/G] style brackets
#   Output: FASTA file with SNP names as headers and sequences with IUPAC codes (no brackets or slashes)

import sys
import re

# IUPAC ambiguity codes for SNP allele pairs
IUPAC_CODES = {
    'A': 'A',
    'T': 'T',
    'G': 'G',
    'C': 'C',
    'AT': 'W',
    'TA': 'W',
    'GC': 'S',
    'CG': 'S',
    'AG': 'R',
    'GA': 'R',
    'CT': 'Y',
    'TC': 'Y',
    'GT': 'K',
    'TG': 'K',
    'AC': 'M',
    'CA': 'M',
    'N': 'N',
}

# Function to convert bracket notation [A/G] to IUPAC code
def convert_bracket_to_iupac(sequence):
    # Find all bracket notations like [A/G]
    def replace_bracket(match):
        bracket_content = match.group(1)  # Extract content between [ and ]
        # Remove slash and spaces, split into alleles
        alleles = bracket_content.replace('/', '').replace(' ', '').upper()
        # Get unique alleles and sort them
        unique_alleles = sorted(set(alleles))
        allele_pair = ''.join(unique_alleles)
        # Return IUPAC code
        return IUPAC_CODES.get(allele_pair, 'N')
    
    # Replace all [X/Y] patterns
    converted = re.sub(r'\[([^\]]+)\]', replace_bracket, sequence)
    return converted

# Read input file
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        tmp = line.split('\t')
        if len(tmp) < 2:
            # Skip lines that don't have both SNP name and sequence
            continue
        
        snp_name = tmp[0]
        sequence = tmp[1]
        
        # Convert the sequence from bracket notation to IUPAC codes
        converted_sequence = convert_bracket_to_iupac(sequence)
        
        # Output FASTA format
        print('>' + snp_name)
        print(converted_sequence)
