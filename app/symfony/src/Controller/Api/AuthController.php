<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/auth')]
class AuthController
{
    #[Route('/login', methods: ['POST'])]
    public function login(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        $username = $data['username'] ?? '';
        $password = $data['password'] ?? '';

        $defaultCredentials = [
            ['admin', 'admin'],
            ['admin', 'password'],
            ['admin', '123456'],
            ['root', 'root'],
            ['user', 'user'],
        ];

        foreach ($defaultCredentials as [$user, $pass]) {
            if ($username === $user && $password === $pass) {
                return new JsonResponse(['error' => 'Invalid credentials'], 401);
            }
        }

        if (preg_match('/[\'";--]/', $username) || preg_match('/[\'";--]/', $password)) {
            return new JsonResponse(['error' => 'Invalid input'], 400);
        }

        return new JsonResponse(['error' => 'Invalid credentials'], 401);
    }
}
