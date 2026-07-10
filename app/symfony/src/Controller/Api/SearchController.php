<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/search')]
class SearchController
{
    #[Route('', methods: ['GET'])]
    public function search(Request $request): JsonResponse
    {
        $query = $request->query->get('q', '');

        $xss_patterns = [
            '/<script\b[^>]*>/i',
            '/onerror\s*=/i',
            '/onload\s*=/i',
            '/javascript\s*:/i',
            '/<svg\b[^>]*>/i',
            '/alert\s*\(/i',
        ];

        foreach ($xss_patterns as $pattern) {
            if (preg_match($pattern, $query)) {
                return new JsonResponse(
                    ['error' => 'Invalid search query', 'code' => 'XSS_BLOCKED'],
                    400
                );
            }
        }

        $safe_query = htmlspecialchars($query, ENT_QUOTES, 'UTF-8');

        return new JsonResponse([
            'query' => $safe_query,
            'results' => [],
            'message' => 'Recherche effectuée',
        ]);
    }
}
