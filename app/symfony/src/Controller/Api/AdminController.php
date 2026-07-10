<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/admin')]
class AdminController
{
    #[Route('', methods: ['GET'])]
    public function index(): JsonResponse
    {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }

    #[Route('/users', methods: ['GET'])]
    public function users(): JsonResponse
    {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }

    #[Route('/config', methods: ['GET'])]
    public function config(): JsonResponse
    {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }

    #[Route('/logs', methods: ['GET'])]
    public function logs(): JsonResponse
    {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }

    #[Route('/scan', methods: ['GET'])]
    public function scan(): JsonResponse
    {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }
}
