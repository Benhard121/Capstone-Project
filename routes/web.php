<?php

use App\Http\Controllers\ProfileController;
use App\Http\Controllers\SentimenController;
use Illuminate\Support\Facades\Route;

// ── Redirect root ke home jika sudah login ──
Route::get('/', function () {
    return redirect()->route('home');
});

// ── Halaman utama aplikasi ──
Route::get('/home', [SentimenController::class, 'index'])
    ->middleware(['auth'])
    ->name('home');

// ── API endpoints (butuh auth) ──
Route::middleware(['auth'])->prefix('api/v1')->group(function () {
    Route::post('/analyze',  [SentimenController::class, 'analyze']);
    Route::get('/history',   [SentimenController::class, 'historyApi']);
    Route::get('/stats',     [SentimenController::class, 'stats']);
    Route::get('/news',      [SentimenController::class, 'news']);
});

// ── Profile routes ──
Route::middleware('auth')->group(function () {
    Route::get('/profile',    [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile',  [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

require __DIR__.'/auth.php';