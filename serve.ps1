$root = $PSScriptRoot
$l = [System.Net.HttpListener]::new()
$l.Prefixes.Add('http://localhost:8765/')
$l.Start()
Write-Output "Serving $root on http://localhost:8765/"
$types = @{ '.html'='text/html; charset=utf-8'; '.json'='application/json'; '.md'='text/plain; charset=utf-8'; '.js'='text/javascript'; '.css'='text/css' }
while ($l.IsListening) {
  $c = $l.GetContext()
  $p = [Uri]::UnescapeDataString($c.Request.Url.AbsolutePath.TrimStart('/'))
  if (-not $p) { $p = 'index.html' }
  $f = Join-Path $root $p
  if ((Test-Path $f -PathType Leaf) -and ((Resolve-Path $f).Path.StartsWith($root))) {
    $b = [IO.File]::ReadAllBytes($f)
    $t = $types[[IO.Path]::GetExtension($f)]; if (-not $t) { $t = 'application/octet-stream' }
    $c.Response.ContentType = $t
    $c.Response.OutputStream.Write($b, 0, $b.Length)
  } else { $c.Response.StatusCode = 404 }
  $c.Response.Close()
}
