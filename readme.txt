1. Los archivos *.yaml tienen que compartirse aparte de la imagen docker del proyecto python.
2. Estos tendrán que agregarse como recursos en kubernetes (en orden) usando:
	kubectl apply -f namespace.yaml
	kubectl apply -f secret.yaml -n python-arq
	kubectl apply -f deployment.yaml -n python-arq
	kubectl apply -f service.yaml -n python-arq
	kubectl apply -f ingress.yaml -n python-arq
