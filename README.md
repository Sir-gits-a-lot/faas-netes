# faas-netes
A beginners guide to using openfaas and run serverless functions on Kubernetes

# Open FaaS (Run Serverless on Kubernetes)



PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

echo -n $PASSWORD | faas-cli login --username admin --password-stdin

faas-cli up -f api.yml

kubectl port-forward -n openfaas svc/gateway 8080:8080

curl 127.0.0.1:8080/function/api --data-binary '{"name": "Jill"}'

# Watchdog for brownfield Development

export OPENFAAS_PREFIX=yourRegistryPrefix
faas-cli template store pull python3-flask-debian
faas-cli new --lang python3-flask-debian http-api

curl -sLS ht‌tps://upload.wikimedia.org/wikipedia/commons/8/85/The_Golden_Gate_Bridge_and_Comet_C2020_F3_NEOWISE_and.jpg -o /tmp/golden-gate.jpg

curl --data-binary @/tmp/golden-gate.jpg 127.0.0.1:8080/function/bw-api > bw.jpg

# Website

faas-cli template store pull python3-http

faas-cli new --lang python3-http homepage --prefix containerRegistryPrefix


# Troubleshooting

arkade info openfaas

faas-cli logs NAME
kubectl logs -n openfaas-fn deploy/NAME

kubectl get events --sort-by=.metadata.creationTimestamp -n openfaas-fn


kubectl logs -n openfaas deploy/gateway -c gateway
kubectl logs -n openfaas deploy/gateway -c faas-netes

# Secure TLS API


faas-cli new --lang python3-http-debian bw-api-protected

echo YqzKzSJw51K9zPpQ3R3N > bw-api-key.txt

faas-cli secret create bw-api-key --from-file=bw-api-key.txt



faas-cli up -f bw-api-protected.yml

curl --data-binary @/tmp/golden-gate.jpg ht‌tp://127.0.0.1:8080/function/bw-api-protected

curl --data-binary @/tmp/golden-gate.jpg --header "api-key=$(cat ./bw-api-key.txt)" 127.0.0.1:8080/function/bw-api-protected > bw.jpg


# It asyncronous by design

time curl -s --data-binary @/tmp/golden-gate.jpg --header "api-key=$(cat ./bw-api-key.txt)" 127.0.0.1:8080/function/bw-api-protected > /dev/null

 Call asynchronously
 
time curl -s --data-binary @/tmp/golden-gate.jpg --header "api-key=$(cat ./bw-api-key.txt)" 127.0.0.1:8080/async-function/bw-api-protected

# Reciever Function

faas-cli new --lang python3-http-debian receive-photo

curl -sLS ht‌tps://upload.wikimedia.org/wikipedia/commons/thumb/7/71/2010-kodiak-bear-1.jpg/640px-2010-kodiak-bear-1.jpg -o /tmp/bear.jpg

time curl -s --data-binary @/tmp/bear.jpg \
  --header "api-key=$(cat ./bw-api-key.txt)"\
  --header "X-Callback-Url: ht‌tp://gateway.openfaas:8080/function/receive-photo" \
127.0.0.1:8080/async-function/bw-api-protected