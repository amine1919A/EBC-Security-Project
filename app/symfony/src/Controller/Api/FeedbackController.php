<?php

namespace App\Controller\Api;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/feedback')]
class FeedbackController
{
    #[Route('', methods: ['POST'])]
    public function submit(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        $message = $data['message'] ?? '';

        $xss_patterns = [
            '/<script\b[^>]*>/i',
            '/onerror\s*=/i',
            '/onload\s*=/i',
            '/javascript\s*:/i',
            '/<svg\b[^>]*>/i',
            '/alert\s*\(/i',
        ];

        foreach ($xss_patterns as $pattern) {
            if (preg_match($pattern, $message)) {
                return new JsonResponse(
                    ['error' => 'Message rejected: XSS pattern detected'],
                    400
                );
            }
        }

        return new JsonResponse([
            'status' => 'received',
            'message' => htmlspecialchars($message, ENT_QUOTES, 'UTF-8'),
        ]);
    }
}
