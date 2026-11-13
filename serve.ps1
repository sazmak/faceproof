# Local server for FaceProof. Run:  powershell -ExecutionPolicy Bypass -File serve.ps1
# Then open http://localhost:8765 in Chrome or Edge.
$root = $PSScriptRoot
$l = [System.Net.HttpListener]::new()
$l.Prefixes.Add('http://localhost:8765/')
$l.Start()
Write-Output "Serving $root on http://localhost:8765/"
$types = @{ '.html'='text/html; charset=utf-8'; '.json'='application/json'; '.md'='text/plain; charset=utf-8'; '.js'='text/javascript'; '.css'='text/css'; '.jpg'='image/jpeg'; '.jpeg'='image/jpeg'; '.png'='image/png'; '.webp'='image/webp' }
while ($l.IsListening) {
  $c = $l.GetContext()
  try {
    $p = [Uri]::UnescapeDataString($c.Request.Url.AbsolutePath.TrimStart('/'))
    if (-not $p) { $p = 'index.html' }
    if ($c.Request.HttpMethod -eq 'PUT') {
      # The page saves experiment output here. Only JSON files directly inside results/ are accepted.
      if ($p -match '^results/[A-Za-z0-9_.-]+\.json$') {
        $ms = New-Object IO.MemoryStream
        $c.Request.InputStream.CopyTo($ms)
        [IO.File]::WriteAllBytes((Join-Path $root $p), $ms.ToArray())
        $c.Response.StatusCode = 204
      } else { $c.Response.StatusCode = 403 }
    } else {
      $f = Join-Path $root $p
      if ((Test-Path -LiteralPath $f -PathType Leaf) -and ((Resolve-Path -LiteralPath $f).Path.StartsWith($root))) {
        $b = [IO.File]::ReadAllBytes($f)
        $t = $types[[IO.Path]::GetExtension($f).ToLower()]; if (-not $t) { $t = 'application/octet-stream' }
        $c.Response.ContentType = $t
        $c.Response.Headers.Add('Cache-Control', 'no-store')
        $c.Response.OutputStream.Write($b, 0, $b.Length)
      } else { $c.Response.StatusCode = 404 }
    }
  } catch { try { $c.Response.StatusCode = 500 } catch {} }
  try { $c.Response.Close() } catch {}
}
