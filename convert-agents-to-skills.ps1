<#
.SYNOPSIS
    Converts agent .md files into skill folder structures.

.DESCRIPTION
    Takes each agent in the source directory, parses its YAML frontmatter,
    and creates a corresponding skill folder with a SKILL.md file.

    Agent format:                          Skill format:
    ---                                    ---
    description: <trigger>                 name: <name>
    mode: all                              description: <trigger>
    [name: <name>]                         ---
    [temperature: 0.2]                     <body unchanged>
    [permission: ...]
    ---
    <body>

.PARAMETER SourceDir
    Path to the directory containing agent .md files.
    Defaults to ./agent

.PARAMETER OutputDir
    Path to the directory where skill folders will be created.
    Defaults to ./skills

.PARAMETER DryRun
    If set, shows what would be created without writing anything.

.EXAMPLE
    .\convert-agents-to-skills.ps1
    .\convert-agents-to-skills.ps1 -SourceDir ./agent -OutputDir ./skills
    .\convert-agents-to-skills.ps1 -DryRun
#>

param(
    [string]$SourceDir = (Join-Path $PSScriptRoot "agent"),
    [string]$OutputDir = (Join-Path $PSScriptRoot "skills"),
    [switch]$DryRun
)

# ─── Helpers ────────────────────────────────────────────────────────────────

function Parse-AgentFile {
    param([string]$FilePath)

    $content = Get-Content -Path $FilePath -Raw -Encoding UTF8
    $lines = $content -split "`n", 2

    # Find frontmatter delimiters
    # Format: ---\n<yaml>\n---\n<body>
    if ($content -notmatch '(?s)^---\s*\r?\n(.+?)\r?\n---\s*\r?\n(.*)$') {
        Write-Warning "  Skipping $($FilePath): no valid frontmatter found"
        return $null
    }

    $yamlBlock = $Matches[1]
    $body = $Matches[2]

    # Parse YAML fields manually (robust for our known schema)
    $fields = @{}
    $currentKey = $null
    $currentValue = @()

    foreach ($line in ($yamlBlock -split "`n")) {
        # Top-level key: value
        if ($line -match '^(\w[\w_]*)\s*:\s*(.*)$') {
            if ($currentKey) {
                $fields[$currentKey] = ($currentValue -join "`n").Trim()
            }
            $currentKey = $Matches[1]
            $currentValue = @($Matches[2])
        }
        elseif ($currentKey) {
            # Continuation line (indented YAML)
            $currentValue += $line
        }
    }
    if ($currentKey) {
        $fields[$currentKey] = ($currentValue -join "`n").Trim()
    }

    return @{
        Fields = $fields
        Body   = $body
    }
}

function Get-AgentName {
    param(
        [hashtable]$Fields,
        [string]$FileName
    )

    # Prefer explicit name field, fall back to filename without extension
    if ($Fields.ContainsKey('name') -and $Fields['name']) {
        return $Fields['name'].Trim()
    }
    return [System.IO.Path]::GetFileNameWithoutExtension($FileName)
}

function Get-Description {
    param([hashtable]$Fields)

    if ($Fields.ContainsKey('description') -and $Fields['description']) {
        return $Fields['description'].Trim()
    }
    return ""
}

# ─── Main ───────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Agent → Skill Converter" -ForegroundColor Cyan
Write-Host "  Source: $SourceDir" -ForegroundColor Gray
Write-Host "  Output: $OutputDir" -ForegroundColor Gray
if ($DryRun) {
    Write-Host "  Mode:   DRY RUN" -ForegroundColor Yellow
}
Write-Host ""

if (-not (Test-Path $SourceDir)) {
    Write-Error "Source directory not found: $SourceDir"
    exit 1
}

$agentFiles = Get-ChildItem -Path $SourceDir -Filter "*.md" -File
if ($agentFiles.Count -eq 0) {
    Write-Warning "No .md files found in $SourceDir"
    exit 0
}

Write-Host "Found $($agentFiles.Count) agent files:" -ForegroundColor Green
foreach ($f in $agentFiles) {
    Write-Host "  - $($f.Name)" -ForegroundColor Gray
}
Write-Host ""

$converted = 0
$skipped = 0

foreach ($agentFile in $agentFiles) {
    $parsed = Parse-AgentFile -FilePath $agentFile.FullName
    if (-not $parsed) {
        $skipped++
        continue
    }

    $name = Get-AgentName -Fields $parsed.Fields -FileName $agentFile.Name
    $description = Get-Description -Fields $parsed.Fields
    $body = $parsed.Body

    Write-Host "  [$name]" -ForegroundColor White -NoNewline
    Write-Host "  ← $($agentFile.Name)" -ForegroundColor DarkGray

    # Build SKILL.md content
    # YAML frontmatter: only name + description (drop mode, temperature, permission, tools)
    $skillFrontmatter = @"
---
name: $name
description: "$($description -replace '"', '\"')"
---
"@

    $skillContent = "$skillFrontmatter`n$body"

    if ($DryRun) {
        Write-Host "    → Would create: skills/$name/SKILL.md" -ForegroundColor Yellow
        Write-Host "    → Description: $($description.Substring(0, [Math]::Min(80, $description.Length)))..." -ForegroundColor DarkGray
    }
    else {
        $skillDir = Join-Path $OutputDir $name
        if (-not (Test-Path $skillDir)) {
            New-Item -ItemType Directory -Path $skillDir -Force | Out-Null
        }

        $skillPath = Join-Path $skillDir "SKILL.md"
        [System.IO.File]::WriteAllText($skillPath, $skillContent, (New-Object System.Text.UTF8Encoding $false))
        Write-Host "    → Created: $skillPath" -ForegroundColor Green
    }

    $converted++
}

Write-Host ""
Write-Host "Done: $converted converted, $skipped skipped" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "(Dry run - nothing was written)" -ForegroundColor Yellow
}
Write-Host ""
