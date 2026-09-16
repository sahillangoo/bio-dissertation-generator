# deploy_github.ps1 - Automated Git Initialization and GitHub Repository Deployment
# Milestone 5 automation script for sahillangoo/bio-dissertation-generator

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Biology & Zoology Dissertation Suite - GitHub Repository Deployment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Clean build intermediates
Write-Host "`n[Step 1/6] Cleaning build intermediates..." -ForegroundColor Yellow
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run python build.py --clean
} else {
    python build.py --clean
}

# 2. Stage required files
Write-Host "`n[Step 2/6] Staging project repository files..." -ForegroundColor Yellow
git add .gitignore pyproject.toml build.py verify.py dissertation.tex preamble.tex references.bib frontmatter/ chapters/ appendices/ figures/ research_sources/ .agents/skills/ tests/ TEST_INFRA.md TEST_READY.md README.md ORIGINAL_REQUEST.md PROJECT.md deploy_github.ps1

# 3. Create clean signed commit
Write-Host "`n[Step 3/6] Creating signed initial commit via active SSH agent..." -ForegroundColor Yellow
git branch -M main
$staged = git status --porcelain
if ($staged) {
    git commit -m "feat: initialize biology and zoology dissertation skills suite and automated latex generator"
} else {
    Write-Host "No unstaged/staged changes to commit (working tree clean)." -ForegroundColor Green
}

# 4. Extract token from Git Credential Manager
Write-Host "`n[Step 4/6] Retrieving verified GitHub token from Git Credential Manager..." -ForegroundColor Yellow
try {
    $token = (@"
protocol=https
host=github.com
"@ | git credential fill | Select-String "password=").ToString().Replace("password=","").Trim()
    if ($token) {
        $env:GH_TOKEN = $token
        Write-Host "GH_TOKEN loaded successfully (length: $($token.Length))." -ForegroundColor Green
    }
} catch {
    Write-Warning "Could not extract token automatically from git credential manager. Proceeding with existing gh auth environment..."
}

# 5. Create public repository on GitHub (or configure remote if existing)
Write-Host "`n[Step 5/6] Ensuring public GitHub repository sahillangoo/bio-dissertation-generator..." -ForegroundColor Yellow
$repoExists = $false
try {
    $repoCheck = gh repo view sahillangoo/bio-dissertation-generator --json nameWithOwner 2>$null
    if ($LASTEXITCODE -eq 0 -and $repoCheck) {
        $repoExists = $true
        Write-Host "Repository sahillangoo/bio-dissertation-generator already exists on GitHub." -ForegroundColor Green
    }
} catch {
    $repoExists = $false
}

if (-not $repoExists) {
    Write-Host "Creating public repository sahillangoo/bio-dissertation-generator..." -ForegroundColor Cyan
    gh repo create sahillangoo/bio-dissertation-generator --public --description "Specialized biology and zoology dissertation skill suite and automated LaTeX dissertation generator" --source . --remote origin
} else {
    # Ensure remote origin is configured
    $remotes = git remote
    if ($remotes -contains "origin") {
        git remote set-url origin https://github.com/sahillangoo/bio-dissertation-generator.git
    } else {
        git remote add origin https://github.com/sahillangoo/bio-dissertation-generator.git
    }
}

# 6. Push to origin main
Write-Host "`n[Step 6/6] Pushing main branch to remote origin..." -ForegroundColor Yellow
git push -u origin main

# 7. Verification
Write-Host "`n=== Verification Summary ===" -ForegroundColor Green
git status
git remote -v
gh repo view sahillangoo/bio-dissertation-generator --web=false
Write-Host "`n[SUCCESS] GitHub deployment complete!" -ForegroundColor Green

