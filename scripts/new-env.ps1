<#
.SYNOPSIS
    Gera o arquivo .env a partir do .env.example, trocando cada "change-me" por uma senha aleatória.

.DESCRIPTION
    As senhas são criadas localmente com gerador criptográfico e nunca aparecem na tela.
    Não sobrescreve um .env existente, a menos que -Force seja usado.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/new-env.ps1
#>
param(
    [switch]$Force,
    [string]$OutFile
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$example = Join-Path $root '.env.example'
if (-not $OutFile) { $OutFile = Join-Path $root '.env' }

if ((Test-Path $OutFile) -and -not $Force) {
    throw "$OutFile já existe. Use -Force para gerar novas senhas (o volume do banco precisará ser recriado)."
}

function New-Secret {
    param([int]$Length = 32)

    # Sem caracteres especiais nem ambíguos: evita problemas em URL, YAML e shell.
    $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'
    # Descarta bytes acima do maior múltiplo do alfabeto para não criar viés.
    $limit = 256 - (256 % $chars.Length)

    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $buffer = New-Object byte[] 1
    $secret = New-Object System.Text.StringBuilder
    try {
        while ($secret.Length -lt $Length) {
            $rng.GetBytes($buffer)
            if ($buffer[0] -lt $limit) {
                [void]$secret.Append($chars[$buffer[0] % $chars.Length])
            }
        }
    }
    finally {
        $rng.Dispose()
    }
    return $secret.ToString()
}

$lines = Get-Content $example -Encoding UTF8 | ForEach-Object {
    if ($_ -match '^\s*([A-Z0-9_]+)=change-me\s*$') {
        "$($Matches[1])=$(New-Secret)"
    }
    else {
        $_
    }
}

[System.IO.File]::WriteAllLines($OutFile, $lines, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Arquivo criado: $OutFile (senhas geradas e não exibidas)."
