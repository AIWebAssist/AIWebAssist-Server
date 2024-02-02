rm -f extension.crx

CRX_PATH=https://clients2.googleusercontent.com/crx/blobs/AeKPYww0O2oW6lOT9OY1OjOyixfZRGChttlgFdEFT0QAiOxHKM_QudcTxPHZBubP1jMQjG5rcz_nIwuUaU8n-ZP-mArbIbB0bZQil9ZBRLIfS75U3xNFAMZSmuXpvTfAtzEPC-zuhXnVNTYP2JbKOA/dicmckdpjpagngabbhhlbahoicjabmoe.crx
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