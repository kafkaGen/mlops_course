run-docker-services:
	docker compose --env-file .env -f deployment/docker/docker-compose.yaml -p mlops_course up -d --build

stop-docker-services:
	docker compose -p mlops_course down

stress-test-endpoint:
	@echo "Testing Prompt Injection Classifier endpoint..."
	python help/stess_test_classification_endpoint.py --dataset data/prompt-injections_train.json

run-kubernetes-server:
	@echo "Creating Kind cluster..."	
	kind create cluster --config deployment/kubernetes/kind-config.yaml

	@echo "Installing NGINX Ingress Controller..."
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@echo "Waiting a few seconds for Ingress controller resources to be registered..."
	sleep 10
	kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
	
	@echo "Enabling metrics-server for autoscaling..."
	kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
	
	@echo "Patching metrics-server to work with Kind (insecure TLS)..."
	kubectl patch deployment metrics-server \
	  -n kube-system \
	  --type='json' \
	  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
	
	@echo "Cluster is ready!"

stop-kubernetes-server:
	@echo "Deleting Kind cluster..."
	kind delete cluster --name mlops-cluster
	@echo "Cluster deleted successfully!"

run-kubernetes-app:
	@echo "Building Docker image..."
	docker build -t prompt-injection-classifier-app:latest . -f deployment/docker/images/prompt-injection-classifier-app.Dockerfile

	@echo "Loading image into Kind cluster..."
	kind load docker-image prompt-injection-classifier-app:latest --name mlops-cluster

	@echo "Deploying Prompt Injection Classifier App..."
	kubectl apply -f deployment/kubernetes/configmap.yaml
	kubectl apply -f deployment/kubernetes/secrets.yaml
	kubectl apply -f deployment/kubernetes/ingress.yaml
	kubectl apply -f deployment/kubernetes/deployment.yaml
	kubectl apply -f deployment/kubernetes/service.yaml
	kubectl apply -f deployment/kubernetes/prompt-injection-classifier-hpa.yaml

	@echo "Application deployed successfully!"

monitor-kubernetes-app:
	@echo "Monitoring application..."
	kubectl get hpa prompt-injection-classifier-hpa
	kubectl get pods -l app=prompt-injection-classifier-app

test-kubernetes-app:
	@echo "Testing application autosacling..."
	hey -z 1m -c 50 'http://localhost/model/inference?prompt=This%20is%20the%20dummy%20prompt%20for%20testing'

stop-kubernetes-app:
	@echo "Removing Prompt Injection Classifier App..."
	kubectl delete -f deployment/kubernetes/configmap.yaml
	kubectl delete -f deployment/kubernetes/secrets.yaml
	kubectl delete -f deployment/kubernetes/ingress.yaml
	kubectl delete -f deployment/kubernetes/deployment.yaml
	kubectl delete -f deployment/kubernetes/service.yaml
	kubectl delete -f deployment/kubernetes/prompt-injection-classifier-hpa.yaml
	@echo "Application removed successfully!"
	