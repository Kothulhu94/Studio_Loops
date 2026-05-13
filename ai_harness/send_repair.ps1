$body = '{"command":"repair","payload":""}'
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
$req = [System.Net.WebRequest]::Create("http://127.0.0.1:8765/api/orchestrator/command")
$req.Method = "POST"
$req.ContentType = "application/json; charset=utf-8"
$req.ContentLength = $bytes.Length
$stream = $req.GetRequestStream()
$stream.Write($bytes, 0, $bytes.Length)
$stream.Close()
try {
    $resp = $req.GetResponse()
    $reader = New-Object System.IO.StreamReader($resp.GetResponseStream())
    Write-Host "Response: $($reader.ReadToEnd())"
} catch [System.Net.WebException] {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    Write-Host "Error: $($reader.ReadToEnd())"
}
