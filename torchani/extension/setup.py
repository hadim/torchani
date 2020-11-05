import os
import torch
import subprocess
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

nvcc_args = ["-gencode=arch=compute_50,code=sm_50", "-gencode=arch=compute_60,code=sm_60",
             "-gencode=arch=compute_61,code=sm_61", "-gencode=arch=compute_70,code=sm_70",
             "-Xptxas=-v", '--expt-extended-lambda', '-use_fast_math']

include_dirs = []
cuda_version = float(torch.version.cuda)
if cuda_version >= 10:
    nvcc_args.append("-gencode=arch=compute_75,code=sm_75")
if cuda_version >= 11:
    nvcc_args.append("-gencode=arch=compute_80,code=sm_80")
if cuda_version >= 11.1:
    nvcc_args.append("-gencode=arch=compute_86,code=sm_86")

setup(
    name='cuaev',
    version='0.1',
    ext_modules=[
        CUDAExtension(
            name='cuaev',
            sources=['aev.cu'],
            include_dirs=include_dirs,
            extra_compile_args={'cxx': ['-std=c++14'],
                                'nvcc': nvcc_args})
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
