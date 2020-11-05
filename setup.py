import importlib
from setuptools import setup, find_packages

ext_modules = []
cmdclass = {}

# Check whether torch is available
if importlib.util.find_spec("torch") is not None:
    import torch

    # Check whether Cuda is available
    if torch.cuda.is_available():

        from torch.utils.cpp_extension import BuildExtension, CUDAExtension

        nvcc_args = [
            "-gencode=arch=compute_50,code=sm_50",
            "-gencode=arch=compute_60,code=sm_60",
            "-gencode=arch=compute_61,code=sm_61",
            "-gencode=arch=compute_70,code=sm_70",
            "-Xptxas=-v",
            "--expt-extended-lambda",
            "-use_fast_math",
        ]

        cuda_version = float(torch.version.cuda)
        if cuda_version >= 10:
            nvcc_args.append("-gencode=arch=compute_75,code=sm_75")
        if cuda_version >= 11:
            nvcc_args.append("-gencode=arch=compute_80,code=sm_80")
        if cuda_version >= 11.1:
            nvcc_args.append("-gencode=arch=compute_86,code=sm_86")

        ext_modules = [
            CUDAExtension(
                name="cuaev",
                sources=["torchani/extension/aev.cu"],
                extra_compile_args={"cxx": ["-std=c++14"], "nvcc": nvcc_args},
            )
        ]

        cmdclass = {"build_ext": BuildExtension}


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="torchani",
    description="PyTorch implementation of ANI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiqm/torchani",
    author="Xiang Gao",
    author_email="qasdfgtyuiop@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=["torch", "lark-parser", "requests"],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)
