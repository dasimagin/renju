#!/bin/bash -e

###############################################################################
# Nvidia 396.44-0 + CUDA 9.0.176-1
###############################################################################

export DEBIAN_FRONTEND=noninteractive

OS=ubuntu1604

nvidia_version=396.44-0
cuda_version=9.0.176-1

cuda_repo="http://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64"
ml_repo="http://developer.download.nvidia.com/compute/machine-learning/repos//${OS}/x86_64"

download_package() {
    local repo=${1}
    local file=${2}

    echo "Upload ${file}..."
    wget --quiet ${repo}/${file}
}

###############################################################################
# Install CUDA
###############################################################################

nvidia_version_major=${nvidia_version%.*} # a.b -> a

cuda_version_major_minor=${cuda_version%.*} #a.b.c -> a.b
cuda_version_code=${cuda_version_major_minor//./-} #a.b -> a-b

cuda_packages=(
    "nvidia-${nvidia_version_major}_${nvidia_version}ubuntu1_amd64.deb"
    "cuda-license-${cuda_version_code}_${cuda_version}_amd64.deb"
    "libcuda1-${nvidia_version_major}_${nvidia_version}ubuntu1_amd64.deb"
    "cuda-cufft-${cuda_version_code}_${cuda_version}_amd64.deb"
    "cuda-cublas-${cuda_version_code}_${cuda_version}_amd64.deb"
    "cuda-cusolver-${cuda_version_code}_${cuda_version}_amd64.deb"
    "cuda-curand-${cuda_version_code}_${cuda_version}_amd64.deb"
    "cuda-cudart-${cuda_version_code}_${cuda_version}_amd64.deb"
    "cuda-cusparse-${cuda_version_code}_${cuda_version}_amd64.deb"
)

ml_packages=(
    "libcudnn7_7.2.1.38-1+cuda${cuda_version_major_minor}_amd64.deb"
    "libnccl2_2.2.13-1+cuda${cuda_version_major_minor}_amd64.deb"
)

apt update
mkdir /usr/lib/nvidia

install_package() {
    local repo=${1}
    local package=${2}

    download_package $repo $package
    apt install --yes --fix-broken --no-install-recommends ./$package
    rm -f $package
}

for package in ${cuda_packages[*]}
do
    install_package $cuda_repo $package
done;

for package in ${ml_packages[*]}
do
    install_package $ml_repo $package
done;

###############################################################################
# Configure dynamic linker
###############################################################################

cuda_conf=/etc/ld.so.conf.d/cuda-${cuda_version_major_minor}.conf
sudo echo /usr/local/cuda-${cuda_version_major_minor}/lib64 > "${cuda_conf}"
echo /usr/lib/x86_64-linux-gnu >> "${cuda_conf}"

nvidia_conf=/etc/ld.so.conf.d/nvidia-${nvidia_version_major}.conf
echo /usr/lib/nvidia-${nvidia_version_major} > "${nvidia_conf}"

ldconfig

###############################################################################
# Install Python3 + packages
###############################################################################

apt install --yes --fix-broken --no-install-recommends --upgrade \
    python3 \
    python3-pip \
    python3-setuptools

python3 --version

pip3 install -U \
    numpy \
    torch \
    torchvision \
    tensorflow-gpu==1.12.0 \
    keras

pip3 list

python3 -c "import tensorflow as tf; tf.__version__"
python3 -c "import torch as th; th.__version__"
python3 -c "import keras as K; K.__version__"

############################################################################
# Clean
############################################################################

apt autoremove --yes
apt clean
apt autoclean

rm -rf /var/cache
rm -rf /var/log

rm -rf /var/lib/apt/lists/*

rm -rf /tmp/*
rm -rf /var/tmp/*
