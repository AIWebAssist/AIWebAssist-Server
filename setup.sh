rm -f extension.crx

CRX_PATH=https://clients2.googleusercontent.com/crx/blobs/AeKPYwwIqwbhw-_kDPnAAu2t5sv92Ssbj3HTsEh4ixHmCJQFowO1yuw3sSkHatdDT-3HUsyfQ1SX9hEnPFG2-gSnQajHhvzouiL4Xv42tmeQCqMnkolpAMZSmuW000Hg1hFgMsxTr2QZUJvYMPSsqA/pacicdjgganecekjpopincedecpdajae.crx
wget $CRX_PATH -O extension.crx

# Check the operating system
if [[ "$(uname)" == "Linux" ]]; then
    # Linux
    apt update && apt install ffmpeg libsm6 libxext6 -y
elif [[ "$(uname)" == "Darwin" ]]; then
    # macOS
    brew install ffmpeg
else
    echo "Unsupported operating system"
    exit 1
fi