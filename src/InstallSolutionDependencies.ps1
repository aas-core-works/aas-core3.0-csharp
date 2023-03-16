<#
.SYNOPSIS
This script runs all the pre-merge checks locally.
#>

$ErrorActionPreference = "Stop"

Import-Module (Join-Path $PSScriptRoot Common.psm1) -Function `
    AssertDotnet

function Main
{
    Set-Location $PSScriptRoot

    AssertDotnet
    Write-Host "Restoring the dependcies..."
    dotnet restore

    Write-Host "Restoring the tools..."
    dotnet tool restore
}

$previousLocation = Get-Location; try
{
    Main
}
finally
{
    Set-Location $previousLocation
}
