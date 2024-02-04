rm -f extension.crx

CRX_PATH=https://clients2.googleusercontent.com/crx/blobs/AeKPYww5dc4OE8GaMbi_i9Zz98PHS1C6InD8yzt29F_xfBwJDXDzXHCsKVjN-EIu0V_m60rjm7qFloHn1JAOCZJ6MPJXICwiduIjMxbNqE6ke9QpFMXXAMZSmuURF_0Fc-swTmo7vyKq7x8NnjzvoA/dicmckdpjpagngabbhhlbahoicjabmoe.crx
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