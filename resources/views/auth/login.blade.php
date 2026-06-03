<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login — SentimenAI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#08090c;--surface:#111318;--surface2:#181c24;
  --border:rgba(255,255,255,0.07);--border-hi:rgba(255,255,255,0.14);
  --text:#e8eaf0;--muted:#6b7385;
  --accent:#4f8eff;--accent2:#6ee7b7;
  --danger:#f87171;
  --radius:14px;--radius-sm:8px;
}
html{min-height:100%}
body{
  font-family:'DM Sans',sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px;
  position:relative;
  overflow:hidden;
}

/* Background glow effect */
body::before{
  content:'';
  position:fixed;
  top:-200px;left:-200px;
  width:600px;height:600px;
  background:radial-gradient(circle, rgba(79,142,255,0.08) 0%, transparent 70%);
  pointer-events:none;
}
body::after{
  content:'';
  position:fixed;
  bottom:-200px;right:-200px;
  width:500px;height:500px;
  background:radial-gradient(circle, rgba(110,231,183,0.06) 0%, transparent 70%);
  pointer-events:none;
}

/* Grid background */
.bg-grid{
  position:fixed;inset:0;
  background-image:linear-gradient(rgba(255,255,255,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.02) 1px,transparent 1px);
  background-size:40px 40px;
  pointer-events:none;
  z-index:0;
}

.auth-wrap{
  position:relative;z-index:1;
  width:100%;max-width:440px;
  animation:fade-up .4s ease both;
}
@keyframes fade-up{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

.auth-logo{
  display:flex;align-items:center;justify-content:center;gap:10px;
  margin-bottom:32px;
  font-family:'Syne',sans-serif;
  font-size:22px;font-weight:800;
  color:var(--text);
}
.auth-logo i{font-size:28px;color:var(--accent)}
.auth-logo span{color:var(--accent)}

.auth-card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:32px;
  box-shadow:0 24px 60px rgba(0,0,0,0.4);
}

.auth-title{
  font-family:'Syne',sans-serif;
  font-size:20px;font-weight:700;
  color:var(--text);
  margin-bottom:6px;
}
.auth-sub{
  font-size:13.5px;color:var(--muted);
  margin-bottom:28px;
  line-height:1.5;
}

.form-group{margin-bottom:18px}
.form-label{
  display:block;
  font-size:12px;font-weight:600;
  text-transform:uppercase;letter-spacing:.8px;
  color:var(--muted);
  margin-bottom:8px;
}
.form-input{
  width:100%;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:var(--radius-sm);
  padding:12px 14px;
  color:var(--text);
  font-size:14px;
  font-family:'DM Sans',sans-serif;
  outline:none;
  transition:.2s;
}
.form-input:focus{border-color:var(--accent);background:#1a1f2e;box-shadow:0 0 0 3px rgba(79,142,255,0.12)}
.form-input::placeholder{color:var(--muted)}
.form-input.error{border-color:var(--danger)}

.input-wrap{position:relative}
.input-wrap .form-input{padding-right:44px}
.input-icon{
  position:absolute;right:14px;top:50%;transform:translateY(-50%);
  color:var(--muted);font-size:18px;cursor:pointer;
  transition:.2s;
}
.input-icon:hover{color:var(--text)}

.form-error{font-size:12px;color:var(--danger);margin-top:6px;display:flex;align-items:center;gap:5px}
.form-error i{font-size:13px}

.remember-row{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:22px;
}
.checkbox-label{
  display:flex;align-items:center;gap:8px;
  font-size:13px;color:var(--muted);cursor:pointer;
}
.checkbox-label input[type=checkbox]{
  width:15px;height:15px;
  accent-color:var(--accent);cursor:pointer;
}
.forgot-link{
  font-size:13px;color:var(--accent);
  text-decoration:none;transition:.15s;
}
.forgot-link:hover{color:#6ea8ff;text-decoration:underline}

.btn-primary{
  width:100%;
  background:var(--accent);
  color:#fff;
  border:none;
  border-radius:var(--radius-sm);
  padding:13px 20px;
  font-size:14.5px;
  font-family:'Syne',sans-serif;
  font-weight:700;
  cursor:pointer;
  transition:.2s;
  display:flex;align-items:center;justify-content:center;gap:8px;
  letter-spacing:.3px;
}
.btn-primary:hover{background:#3a7ae8;transform:translateY(-1px);box-shadow:0 8px 24px rgba(79,142,255,0.3)}
.btn-primary:active{transform:translateY(0)}
.btn-primary:disabled{opacity:.6;cursor:not-allowed;transform:none;box-shadow:none}

.divider{
  display:flex;align-items:center;gap:12px;
  margin:22px 0;
  font-size:12px;color:var(--muted);
}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:var(--border)}

.auth-footer{
  text-align:center;margin-top:22px;
  font-size:13.5px;color:var(--muted);
}
.auth-footer a{color:var(--accent);text-decoration:none;font-weight:500}
.auth-footer a:hover{text-decoration:underline}

/* Alert */
.alert{
  border-radius:var(--radius-sm);
  padding:12px 16px;
  margin-bottom:20px;
  font-size:13px;
  display:flex;align-items:flex-start;gap:10px;
}
.alert.danger{background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);color:#fca5a5}
.alert.success{background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);color:#6ee7b7}
.alert i{font-size:16px;flex-shrink:0;margin-top:1px}

.spinner{width:16px;height:16px;border:2px solid rgba(255,255,255,0.3);border-top:2px solid #fff;border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg-grid"></div>

<div class="auth-wrap">
  <div class="auth-logo">
    <i class="ti ti-robot"></i>
    Sentimen<span>AI</span>
  </div>

  <div class="auth-card">
    <h1 class="auth-title">Selamat Datang Kembali</h1>
    <p class="auth-sub">Masuk untuk melanjutkan analisis sentimen berita ekonomi Anda</p>

    {{-- Session Status --}}
    @if (session('status'))
      <div class="alert success">
        <i class="ti ti-circle-check"></i>
        {{ session('status') }}
      </div>
    @endif

    <form method="POST" action="{{ route('login') }}" id="loginForm">
      @csrf

      {{-- Email --}}
      <div class="form-group">
        <label class="form-label" for="email">Email</label>
        <div class="input-wrap">
          <input
            id="email"
            type="email"
            name="email"
            class="form-input {{ $errors->has('email') ? 'error' : '' }}"
            value="{{ old('email') }}"
            placeholder="nama@email.com"
            required
            autofocus
            autocomplete="username"
          >
          <i class="ti ti-mail input-icon"></i>
        </div>
        @error('email')
          <div class="form-error"><i class="ti ti-alert-circle"></i>{{ $message }}</div>
        @enderror
      </div>

      {{-- Password --}}
      <div class="form-group">
        <label class="form-label" for="password">Password</label>
        <div class="input-wrap">
          <input
            id="password"
            type="password"
            name="password"
            class="form-input {{ $errors->has('password') ? 'error' : '' }}"
            placeholder="Masukkan password Anda"
            required
            autocomplete="current-password"
          >
          <i class="ti ti-eye input-icon" id="toggle-pw" onclick="togglePassword('password','toggle-pw')"></i>
        </div>
        @error('password')
          <div class="form-error"><i class="ti ti-alert-circle"></i>{{ $message }}</div>
        @enderror
      </div>

      {{-- Remember & Forgot --}}
      <div class="remember-row">
        <label class="checkbox-label">
          <input type="checkbox" name="remember"> Ingat saya
        </label>
      </div>

      <button type="submit" class="btn-primary" id="loginBtn">
        <i class="ti ti-login"></i> Masuk
      </button>
    </form>

    @if (Route::has('register'))
      <div class="auth-footer">
        Belum punya akun? <a href="{{ route('register') }}">Daftar sekarang</a>
      </div>
    @endif
  </div>
</div>

<script>
function togglePassword(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  if (input.type === 'password') {
    input.type = 'text';
    icon.classList.replace('ti-eye', 'ti-eye-off');
  } else {
    input.type = 'password';
    icon.classList.replace('ti-eye-off', 'ti-eye');
  }
}

document.getElementById('loginForm').addEventListener('submit', function() {
  const btn = document.getElementById('loginBtn');
  btn.disabled = true;
  btn.innerHTML = '<div class="spinner"></div> Memproses...';
});
</script>
</body>
</html>
