# Remedian

Implements the Remedian algorithm as described in http://web.ipac.caltech.edu/staff/fmasci/home/statistics_refs/Remedian.pdf,
but supports "ntile" rather than just median. Also does not require explicit setting of the exponent, which is adaptively
increased to accommodate arbitrary size.  Uses weighted averaging for the result as described in section 7 of this paper
