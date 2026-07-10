#!/bin/bash
echo "🛑 Arrêt des services EBC..."
docker-compose down 2>/dev/null || docker compose down
echo "✅ Services arrêtés"
