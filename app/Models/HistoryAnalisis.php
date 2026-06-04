<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class HistoryAnalisis extends Model
{
    protected $table = 'history_analisis';

    protected $fillable = [
        'user_id',           // ← DITAMBAHKAN: agar data tersimpan per user
        'judul_berita',
        'konten',
        'hasil_sentimen',
        'confidence_score',
    ];

    /**
     * Relasi ke User pemilik history ini.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}