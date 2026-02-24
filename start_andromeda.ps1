# =====================================================
# ANDROMEDA MASTER PLAN - Script de Inicio PowerShell
# Genesis MetaWorks | Puerto Rico 2025
# =====================================================

Write-Host "" -ForegroundColor Cyan
Write-Host "  ANDROMEDA - GENESIS METAWORKS" -ForegroundColor Cyan
Write-Host "  Sistema Multi-Agente con Ollama Local" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan

# Configuracion
$OLLAMA_HOST = "http://localhost:11434"
$REPO_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PYTHON = "python"

# Verificar Ollama
Write-Host "[1/5] Verificando Ollama..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$OLLAMA_HOST/api/tags" -Method GET -TimeoutSec 5
    Write-Host "Ollama ACTIVO en $OLLAMA_HOST" -ForegroundColor Green
} catch {
    Write-Host "Ollama no detectado. Iniciando..." -ForegroundColor Red
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "Ollama iniciado." -ForegroundColor Green
}

# Verificar modelo llama3
Write-Host "[2/5] Verificando modelo llama3..." -ForegroundColor Yellow
$models = ollama list 2>&1
if ($models -match "llama3") {
    Write-Host "Modelo llama3 disponible." -ForegroundColor Green
} else {
    Write-Host "Descargando llama3 (esto puede tomar varios minutos)..." -ForegroundColor Yellow
    ollama pull llama3
}

# Instalar dependencias Python
Write-Host "[3/5] Verificando dependencias Python..." -ForegroundColor Yellow
& $PYTHON -m pip install requests flask python-telegram-bot --quiet
Write-Host "Dependencias OK." -ForegroundColor Green

# Configurar variables de entorno
Write-Host "[4/5] Configurando entorno..." -ForegroundColor Yellow
$env:OLLAMA_HOST = $OLLAMA_HOST
Write-Host "OLLAMA_HOST = $OLLAMA_HOST" -ForegroundColor Green

# Ejecutar automatizaciones diarias
Write-Host "[5/5] Ejecutando ANDROMEDA Daily Automations..." -ForegroundColor Yellow
Set-Location $REPO_DIR
& $PYTHON -m bot.daily_automations

Write-Host "" 
Write-Host "ANDROMEDA ha completado su ciclo diario." -ForegroundColor Cyan
Write-Host "Revisa knowledge.json para ver los resultados." -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para salir"
