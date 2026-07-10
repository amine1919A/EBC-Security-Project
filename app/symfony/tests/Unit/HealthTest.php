<?php

namespace App\Tests\Unit;

use App\Controller\Api\HealthController;
use PHPUnit\Framework\TestCase;

class HealthTest extends TestCase
{
    public function testHealthReturnsJson(): void
    {
        $controller = new HealthController();
        $response = $controller();

        $this->assertEquals(200, $response->getStatusCode());
        $data = json_decode($response->getContent(), true);
        $this->assertEquals('ok', $data['status']);
        $this->assertEquals('EBC Security Platform', $data['application']);
    }
}
