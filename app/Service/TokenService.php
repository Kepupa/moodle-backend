<?php

namespace App\Service;

use GuzzleHttp\Client;
use Illuminate\Support\Facades\Cache;

class TokenService
{
    public function getToken(string $username, string $password)
    {
        $response = env('MOODLE_URL')->post('/login/token.php', [
            'form_params' => [
                'username' => $username,
                'password' => $password,
                'service'  => env('MOODLE_SERVICE'),
            ],
        ]);

        return json_decode($response->getBody(), true);
    }


}
