<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Service\TokenService;
use Illuminate\Support\Facades\Http;

class AuthController extends Controller
{
    public function login(Request $request){
        $request->validate([
            'username' => 'required|string',
            'password' => 'required|string',
        ]);

        $response = Http::asForm()->post(env('MOODLE_LOGIN'), [
            'username' => $request->username,
            'password' => $request->password,
            'service' => env('MOODLE_SERVICE'),
            'moodlewsrestformat' => env('MOODLE_WSRESTFORMAT')
        ]);

        $token = $response->json();

        if (isset($token['error'])) {
            return response()->json(['error' => 'Invalid username or password'], 401);
        }

        return response()->json([
            'massage' => 'success',
            'token' => $token['token']
        ]);
    }
}

