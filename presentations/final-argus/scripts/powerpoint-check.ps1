param([string]$PresentationRoot = (Split-Path $PSScriptRoot -Parent))
# Actual installed PowerPoint, following the OS image-slide COM precedent.
$ErrorActionPreference = 'Stop'
$out = Join-Path $PresentationRoot 'evidence\powerpoint'
New-Item -ItemType Directory -Force $out | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$existingCount = $app.Presentations.Count
$report = [ordered]@{status='RUNNING'; application='Microsoft PowerPoint desktop'; version=$app.Version; existingPresentations=$existingCount; slides=@(); errors=@(); interactiveDialogs='No claim from unattended COM; open/export errors are recorded.'}
$deck = $null
$verificationCopy = Join-Path $out ('verify-' + [guid]::NewGuid().ToString() + '.pptx')
try {
  Copy-Item (Join-Path $PresentationRoot 'exports\ARGUS_Final_Skeleton.pptx') $verificationCopy
  $deck = $app.Presentations.Open($verificationCopy,-1,0,0)
  $report.slideCount = $deck.Slides.Count
  $report.widthPoints = $deck.PageSetup.SlideWidth
  $report.heightPoints = $deck.PageSetup.SlideHeight
  if ($deck.Slides.Count -ne 8) { throw 'Expected eight slides' }
  foreach ($slide in $deck.Slides) {
    $id = '{0:D2}' -f $slide.SlideIndex
    $slide.Export((Join-Path $out ('slide-'+$id+'.png')),'PNG',1920,1080)
    $notes = @()
    foreach ($shape in $slide.NotesPage.Shapes) {
      if ($shape.HasTextFrame -and $shape.TextFrame.HasText) { $notes += $shape.TextFrame.TextRange.Text }
    }
    $report.slides += [ordered]@{index=$slide.SlideIndex; shapes=$slide.Shapes.Count; notes=($notes -join "`n"); export=('slide-'+$id+'.png')}
  }
  $deck.SaveAs((Join-Path $out 'powerpoint-export.pdf'),32)
  $report.pdfExport='PASS'
  $report.status='PASS'
} catch {
  $report.status='FAIL'
  $report.errors += $_.Exception.Message
  throw
} finally {
  if ($null -ne $deck) { $deck.Close() }
  if (Test-Path $verificationCopy) { Remove-Item $verificationCopy }
  if ($existingCount -eq 0) { $app.Quit() }
  $report | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 (Join-Path $out 'report.json')
}
