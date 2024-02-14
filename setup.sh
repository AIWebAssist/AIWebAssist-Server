rm -f extension.crx

CRX_PATH=https://clients2.googleusercontent.com/crx/blobs/AeKPYwwAs2phlcREAaCG8fmfNI-XYqqjFTcii7oy-TLUZPR2rq0Cru7u_dWfTBkWxTqMRztauKwtbt_uZXhZHEZxl8yEELN2QLpJs5pTIVZo4Wfal0HXAMZSmuX6JifPLJ8K1TfDYJUo-IsG02V8xg/pacicdjgganecekjpopincedecpdajae.crx
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