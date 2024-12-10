# Tool for the creation of low-fidelity synthetic data

This tool was developed as a component of the Creation of Synthetic data project that BIT and Nesta completed for the Education Endowment Foundation (EEF). It was used to generate low-fidelity synthetic datasets of all randomised controlled trial datasets in the EEF’s data archive. Ultimately, the outputs will be included in a data catalogue that will accompany this archive.

## Acknowledgements

This work was commissioned for EEF, and funded through the Department for Education, part of the UK Government. The work has been supported by FFT Education, who is the data processor for EEF’s data archive, as well as by the Office for National Statistics, who manage the Secure Research Service through which the datasets in the archive are available. This work does not imply the endorsement of the ONS or other data owners.

This tool is a specialised version of BIT’s original synthetic datatool, developed for ADR UK. The current version was developed to specifically work on the EEF data and under the constraints of the ONS Secure Research Service where this data was stored. The original tool can be found in this repository, and links to guidance about what low-fidelity synthetic data is and how the tool works can be found in that repository.

## Using the tool

### Summary statistics generation

+ Copy the following into your working directory:
  + The `behavioural_synthetic` directory.
  + The `requirements.txt` file.
+ In most use cases you should be able to create a virtual environment and install the required components from `requirements.txt` using pip.
+ In the case of an environment such as the SRS most requirements should be available to you, but you should use the contents of the `behavioural_synthetic_SRS` directory instead of `behavioural_synthetic`, as the latter is written for a later version of Python and has more dependencies.
+ Follow the instructions in the notebook `summary_statistics.ipynb` in order to generate summary statistics for input to the synthetic data generation notebook.

### Synthetic data generation from summary statistics

+ Copy the following into your working directory:
  + The `behavioural_synthetic` directory.
  + The `requirements.txt` file.
  + The `QA_code.R` file.
    + Set the `lib.loc` parameter in each require statement in this file to the location of your R libraries.
+ Create a virtual environment for Python containing the required libraries using `requirements.txt`.
+ Set up the input and output directories.
+ Edit the `generation.ipynb` notebook to use those input and output directories as described in the notebook.
+ Follow the instructions in the notebook in order to generate synthetic data from summary statistics.

### Unit tests

+ Can be run for `behavioural_synthetic` using pytest.  
+ Note that in order to fulfil SRS export requirements, test data has been deleted from the unit tests in `behavioural_synthetic_SRS` and some reconstruction will be needed before they can be used.  While this code has passed these tests when we were using it, caution should be be exercised when using this version of the library unless the reconstruction has been carried out and unit tests can be performed.

**Caution:** If this tool is being used to generate synthetic data from a source containing personal or other sensitive information, the synthetic data output should still be subject to a disclosure control process before release. This is because misconfiguration of the tool, random chance, and the nature of the original data can occasionally lead to disclosive information still being present in the synthetic output (see 'Why is disclosure control still needed' in the User Guide). Proceed with care.

## Prerequisites

This tool requires that the following are installed:

### Summary statistics

+ Python 3.11 and the contents of requirements.txt (using behavioural_synthetic ) or
+ Python 3.7 and the general SRS conda loadout (using behavioural_synthetic_SRS)

### Synthetic data generation

+ Python 3.11 and the contents of requirements.txt.
+ R 4.4.1 or greater.  
+ Required R libraries: rlang, jsonlite, janitor, tidyverse, openxlsx.
