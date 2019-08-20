#!/usr/bin/python

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# This script creates yaml files to build conda environments
# For generating a conda file for running only python code:
# $ python generate_conda_file.py
#
# For generating a conda file for running python gpu:
# $ python generate_conda_file.py --gpu


import argparse
import textwrap
from sys import platform


HELP_MSG = """
To create the conda environment:
$ conda env create -f {conda_env}.yaml

To update the conda environment:
$ conda env update -f {conda_env}.yaml

To register the conda environment in Jupyter:
$ conda activate {conda_env}
$ python -m ipykernel install --user --name {conda_env} \
--display-name "Python ({conda_env})"
"""

CHANNELS = ["defaults", "conda-forge", "pytorch"]

CONDA_BASE = {
    "python": "python==3.6.8",
    "pip": "pip>=19.1.1",
    "ipykernel": "ipykernel>=4.6.1",
    "jupyter": "jupyter>=1.0.0",
    "matplotlib": "matplotlib>=2.2.2",
    "numpy": "numpy>=1.13.3",
    "pandas": "pandas>=0.24.2",
    "pytest": "pytest>=3.6.4",
    "pytorch": "pytorch-cpu>=1.0.0",
    "scipy": "scipy>=1.0.0",
    "tensorflow": "tensorflow==1.12.0",
    "h5py": "h5py>=2.8.0",
    "tensorflow-hub": "tensorflow-hub==0.5.0",
    "py-xgboost": "py-xgboost<=0.80",
}

CONDA_GPU = {
    "numba": "numba>=0.38.1",
    "pytorch": "pytorch>=1.0.0",
    "tensorflow": "tensorflow-gpu==1.12.0",
}

PIP_BASE = {
    "allennlp": "allennlp==0.8.4",
    "azureml-sdk[automl]": "azureml-sdk[automl]==1.0.48",
    "azureml-train-automl": "azureml-train-automl==1.0.48",
    "azureml-dataprep": "azureml-dataprep==1.1.8",
    "azureml-widgets": "azureml-widgets==1.0.48",
    "azureml-mlflow": "azureml-mlflow>=1.0.43.1",
    "black": "black>=18.6b4",
    "cached-property": "cached-property==1.5.1",
    "dask": "dask[dataframe]==1.2.2",
    "papermill": "papermill>=1.0.1",
    "nteract-scrapbook": "nteract-scrapbook>=0.2.1",
    "pydocumentdb": "pydocumentdb>=2.3.3",
    "tqdm": "tqdm==4.31.1",
    "pyemd": "pyemd==0.5.1",
    "ipywebrtc": "ipywebrtc==0.4.3",
    "pre-commit": "pre-commit>=1.14.4",
    "scikit-learn": "scikit-learn>=0.19.0,<=0.20.3",
    "setuptools_scm": "setuptools_scm==3.2.",
    "sklearn-crfsuite": "sklearn-crfsuite>=0.3.6",
    "spacy": "spacy>=2.1.4",
    "spacy-models": (
        "https://github.com/explosion/spacy-models/releases/download/"
        "en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz"
    ),
    "gensim": "gensim>=3.7.0",
    "nltk": "nltk>=3.4",
    "pytorch-pretrained-bert": "pytorch-pretrained-bert>=0.6",
    "seqeval": "seqeval>=0.0.12",
}

PIP_GPU = {}

PIP_DARWIN = {}
PIP_DARWIN_GPU = {"horovod": "horovod>=0.16.1"}

PIP_LINUX = {}
PIP_LINUX_GPU = {"horovod": "horovod>=0.16.1"}
CONDA_LINUX = {"cudatoolkit": "cudatoolkit>=9.2"}

PIP_WIN32 = {}
PIP_WIN32_GPU = {}
CONDA_WIN32 = {"pytorch": "pytorch==1.0.0", "cudatoolkit": "cuda90"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
        This script generates a conda file for different environments.
        Plain python is the default,
        but flags can be used to support GPU functionality."""
        ),
        epilog=HELP_MSG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--name", help="specify name of conda environment")
    parser.add_argument(
        "--gpu", action="store_true", help="include packages for GPU support"
    )
    args = parser.parse_args()

    # set name for environment and output yaml file
    conda_env = "nlp_cpu"
    if args.gpu:
        conda_env = "nlp_gpu"

    # overwrite environment name with user input
    if args.name is not None:
        conda_env = args.name

    # update conda and pip packages based on flags provided
    conda_packages = CONDA_BASE
    pip_packages = PIP_BASE

    # check for os platform support
    if platform == "darwin":
        pip_packages.update(PIP_DARWIN)
        PIP_GPU.update(PIP_DARWIN_GPU)
    elif platform.startswith("linux"):
        conda_packages.update(CONDA_LINUX)
        pip_packages.update(PIP_LINUX)
        PIP_GPU.update(PIP_LINUX_GPU)
    elif platform == "win32":
        conda_packages.update(CONDA_WIN32)
        pip_packages.update(PIP_WIN32)
        PIP_GPU.update(PIP_WIN32_GPU)
    else:
        raise Exception("Unsupported platform. Must be Windows, Linux, or macOS")

    if args.gpu:
        conda_packages.update(CONDA_GPU)
        pip_packages.update(PIP_GPU)

    # write out yaml file
    conda_file = "{}.yaml".format(conda_env)
    with open(conda_file, "w") as f:
        for line in HELP_MSG.format(conda_env=conda_env).split("\n"):
            f.write("# {}\n".format(line))
        f.write("name: {}\n".format(conda_env))
        f.write("channels:\n")
        for channel in CHANNELS:
            f.write("- {}\n".format(channel))
        f.write("dependencies:\n")
        for conda_package in conda_packages.values():
            f.write("- {}\n".format(conda_package))
        f.write("- pip:\n")
        for pip_package in pip_packages.values():
            f.write("  - {}\n".format(pip_package))

    print("Generated conda file: {}".format(conda_file))
    print(HELP_MSG.format(conda_env=conda_env))
