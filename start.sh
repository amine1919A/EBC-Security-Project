#!/bin/bash
echo "🚀 Démarrage des services EBC..."
docker-compose up -d 2>/dev/null || docker compose up -d
echo "✅ Services démarrés"
echo ""
echo "   Application EBC:  http://localhost:8080"
echo "   SonarQube:       http://localhost:9000"
echo "   Grafana:         http://localhost:3000"
echo "   Prometheus:      http://localhost:9090"
