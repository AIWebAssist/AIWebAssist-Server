######################
# Become a Certificate Authority
# Source https://stackoverflow.com/a/60516812
######################

# Generate private key
openssl genrsa -des3 -out ./ssl/myCA.key 2048
# Generate root certificate
openssl req -x509 -new -nodes -key ./ssl/myCA.key -sha256 -days 825 -out ./ssl/myCA.pem

######################
# Create CA-signed certs
######################

NAME=scrape_anything # Use your own domain name
# Generate a private key
openssl genrsa -out "./ssl/$NAME.key" 2048
# Create a certificate-signing request
openssl req -new -key "./ssl/$NAME.key" -out "./ssl/$NAME.csr"
# Create a config file for the extensions
>"./ssl/$NAME.ext" cat <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = $NAME # Be sure to include the domain name here because Common Name is not so commonly honoured by itself
DNS.2 = www.$NAME # Optionally, add additional domains (I've added a subdomain here)
IP.1 = 192.168.0.13 # Optionally, add an IP address (if the connection which you have planned requires it)
EOF
# Create the signed certificate
openssl x509 -req -in "./ssl/$NAME.csr" -CA ./ssl/myCA.pem -CAkey ./ssl/myCA.key -CAcreateserial -out "./ssl/$NAME.crt" -days 825 -sha256 -extfile "./ssl/$NAME.ext"

# chmod +x generate_certs.sh