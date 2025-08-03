#!/bin/bash
kubectl port-forward svc/api-service 8080:80 &
PF_PID=$!

hey -z 3m -q 100 -c 10 http://localhost:8080/docs

kill $PF_PID
