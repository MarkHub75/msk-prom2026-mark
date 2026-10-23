param(
    [ValidateSet('Start', 'Stop', 'Status')][string]$Action = 'Start',
    [switch]$OpenBrowser
)
$ErrorActionPreference = 'Stop'
# Every LinQ service lives in 10.0.114.0/24 behind Matvey's OpenVPN: add new ports here,
# never try to reach that subnet directly from this machine.
$Forwards = @(
    '127.0.0.1:8888:hackathon.lin-q.ru:80',   # JupyterHub
    '127.0.0.1:5672:10.0.114.30:5672',        # RabbitMQ AMQP (TPU API)
    '127.0.0.1:15672:10.0.114.30:15672'       # RabbitMQ management UI/API
)
$Remote = if ($env:LINQ_TUNNEL_REMOTE) { $env:LINQ_TUNNEL_REMOTE } else { 'sl1m@192.168.1.31' }
$Key = Join-Path $env:USERPROFILE '.ssh\linq_matvey'
$Url = 'http://127.0.0.1:8888/'
$WorkDir = Join-Path $env:LOCALAPPDATA 'linq-tunnel'
$Log = Join-Path $WorkDir 'linq-tunnel-error.log'

function Get-LinQTunnel {
    @(Get-CimInstance Win32_Process -Filter "Name='ssh.exe'" | Where-Object {
        $_.CommandLine -and $_.CommandLine.Contains($Remote) -and $_.CommandLine.Contains('linq_matvey')
    })
}

function Test-LinQForwards($tunnel) {
    foreach ($f in $Forwards) { if (-not $tunnel.CommandLine.Contains($f)) { return $false } }
    return $true
}

function Test-LinQPage {
    try {
        $page = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 6
        return ($page.StatusCode -eq 200 -and $page.Content -match 'JupyterHub')
    } catch { return $false }
}

if ($Action -eq 'Stop') {
    foreach ($tunnel in (Get-LinQTunnel)) {
        Stop-Process -Id $tunnel.ProcessId -ErrorAction SilentlyContinue
    }
    Write-Host 'LinQ SSH tunnel stopped. Happ was not changed.'
    exit 0
}

if ($Action -eq 'Status') {
    if (@(Get-LinQTunnel).Count -gt 0 -and (Test-LinQPage)) {
        Write-Host "LinQ is available: $Url"
        exit 0
    }
    Write-Host 'LinQ tunnel is unavailable. Run Connect-LinQ.cmd.'
    exit 1
}

if (-not (Test-Path -LiteralPath $Key)) { throw "SSH key was not found: $Key" }
$tunnels = @(Get-LinQTunnel)
if ($tunnels.Count -gt 0 -and (-not (Test-LinQPage) -or @($tunnels | Where-Object { -not (Test-LinQForwards $_) }).Count -gt 0)) {
    foreach ($tunnel in $tunnels) { Stop-Process -Id $tunnel.ProcessId -ErrorAction SilentlyContinue }
    Start-Sleep -Milliseconds 500
    $tunnels = @()
}
if ($tunnels.Count -eq 0) {
    foreach ($f in $Forwards) {
        $port = [int]($f.Split(':')[1])
        if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
            throw "Port $port is used by another application. No processes were stopped."
        }
    }
    New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
    $sshArgs = @('-i', $Key, '-N', '-T')
    foreach ($f in $Forwards) { $sshArgs += @('-L', $f) }
    $sshArgs += @(
        '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
        '-o', 'ExitOnForwardFailure=yes', '-o', 'ConnectTimeout=8',
        '-o', 'ServerAliveInterval=15', '-o', 'ServerAliveCountMax=3', $Remote)
    $sshProcess = Start-Process -FilePath (Join-Path $env:WINDIR 'System32\OpenSSH\ssh.exe') `
        -ArgumentList $sshArgs -WindowStyle Hidden -PassThru -RedirectStandardError $Log
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        if (Get-NetTCPConnection -LocalPort 8888 -State Listen -ErrorAction SilentlyContinue) { break }
        if ($sshProcess.HasExited) { throw "SSH connection failed. Details: $Log" }
        Start-Sleep -Milliseconds 250
    }
}
if (-not (Test-LinQPage)) { throw "JupyterHub did not answer. Check Matvey's laptop and its OpenVPN connection. Details: $Log" }
Write-Host "LinQ is available: $Url"
Write-Host 'Happ stays connected to SAMARKAND. Keep Matvey connected to the local network and OpenVPN.'
if ($OpenBrowser) { Start-Process $Url }
