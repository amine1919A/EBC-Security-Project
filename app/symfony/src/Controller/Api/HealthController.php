<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/health')]
class HealthController
{
    #[Route('', methods: ['GET'])]
    public function __invoke(): JsonResponse
    {
        return new JsonResponse([
            'status' => 'ok',
            'application' => 'EBC Security Platform',
            'version' => '1.0.0',
            'timestamp' => (new \DateTime())->format('c'),
        ]);
    }
}
