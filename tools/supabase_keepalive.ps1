$ErrorActionPreference = 'Stop'

$projectUrl = 'https://kqmshtjzosiurntxldrj.supabase.co'
$publishableKey = 'sb_publishable_13WIeVf-SOo9T5xIkBfMPQ_9YybQG-l'
$endpoint = "$projectUrl/rest/v1/quiz_scores?select=id&limit=1"
$statusDirectory = Join-Path $env:LOCALAPPDATA 'SupabaseKeepalive'
$statusFile = Join-Path $statusDirectory 'piliwu01-status.json'

$status = [ordered]@{
    project = 'piliwu01'
    checked_at_taipei = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId(
        [DateTimeOffset]::UtcNow,
        'Taipei Standard Time'
    ).ToString('yyyy-MM-dd HH:mm:ss zzz')
    success = $false
    http_status = $null
    message = ''
}

try {
    $response = Invoke-WebRequest `
        -Uri $endpoint `
        -Method Get `
        -Headers @{
            apikey = $publishableKey
            Authorization = "Bearer $publishableKey"
        } `
        -TimeoutSec 30 `
        -UseBasicParsing

    $status.http_status = [int]$response.StatusCode
    $status.success = $response.StatusCode -ge 200 -and $response.StatusCode -lt 300
    $status.message = if ($status.success) { 'Supabase read request succeeded.' } else { 'Supabase returned a non-success status.' }
}
catch {
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
        $status.http_status = [int]$_.Exception.Response.StatusCode
    }
    $status.message = 'Supabase read request failed.'
}

New-Item -ItemType Directory -Path $statusDirectory -Force | Out-Null
$status | ConvertTo-Json | Set-Content -LiteralPath $statusFile -Encoding utf8

if (-not $status.success) {
    exit 1
}

