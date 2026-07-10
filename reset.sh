#!/bin/bash
echo "⚠️  Réinitialisation complète des services EBC..."
docker-compose down -v 2>/dev/null || docker compose down -v
echo "✅ Volumes supprimés, services arrêtés"
echo "🔁 Relancez avec ./start.sh"
