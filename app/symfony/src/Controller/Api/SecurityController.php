<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/security')]
class SecurityController
{
    #[Route('/scan', methods: ['POST'])]
    public function triggerScan(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        $tool = $data['tool'] ?? 'all';

        return new JsonResponse([
            'status' => 'scan_triggered',
            'tool' => $tool,
            'message' => 'Scan lancé, consultez le pipeline CI/CD pour les résultats',
        ]);
    }

    #[Route('/results/{tool}', methods: ['GET'])]
    public function getResults(string $tool): JsonResponse
    {
        $results = match ($tool) {
            'sonarqube' => ['tool' => 'SonarQube', 'status' => 'pending'],
            'zap' => ['tool' => 'OWASP ZAP', 'status' => 'pending'],
            'trivy' => ['tool' => 'Trivy', 'status' => 'pending'],
            'gitleaks' => ['tool' => 'Gitleaks', 'status' => 'pending'],
            default => ['error' => 'Outil inconnu'],
        };

        return new JsonResponse($results);
    }

    #[Route('/status', methods: ['GET'])]
    public function status(): JsonResponse
    {
        return new JsonResponse([
            'sast' => ['sonarqube' => 'configured', 'phpstan' => 'configured'],
            'sca' => ['trivy' => 'configured'],
            'secrets' => ['gitleaks' => 'configured'],
            'dast' => ['zap' => 'configured', 'nikto' => 'configured'],
            'monitoring' => ['prometheus' => 'configured', 'grafana' => 'configured'],
        ]);
    }
}
