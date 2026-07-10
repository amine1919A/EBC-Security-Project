<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/users')]
class UserController
{
    #[Route('', methods: ['GET'])]
    public function list(Request $request): JsonResponse
    {
        $id = $request->query->get('id');

        if ($id && preg_match('/[\'";--]/', $id)) {
            return new JsonResponse(
                ['error' => 'Invalid input', 'code' => 'SECURITY_BLOCKED'],
                400
            );
        }

        return new JsonResponse([
            'users' => [],
            'message' => 'Authentification requise',
        ], 401);
    }

    #[Route('/{id}', methods: ['GET'])]
    public function show(int $id): JsonResponse
    {
        if ($id < 1) {
            return new JsonResponse(['error' => 'Invalid ID'], 400);
        }

        return new JsonResponse([
            'id' => $id,
            'message' => 'Authentification requise',
        ], 401);
    }
}
