# Importar el módulo de compresión
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Obtener todos los archivos .mp3 en la carpeta actual
$mp3Files = Get-ChildItem -Path . -Filter *.mp3

foreach ($file in $mp3Files) {
    $bz2FileName = "$($file.FullName).bz2"
    
    # Comprimir el archivo .mp3 en formato .bz2
    Write-Output "Comprimiendo $($file.FullName) a $bz2FileName"
    $fileStream = [System.IO.File]::OpenRead($file.FullName)
    $bz2Stream = [System.IO.Compression.BrotliStream]::new([System.IO.File]::Create($bz2FileName), [System.IO.Compression.CompressionLevel]::Optimal)
    
    $fileStream.CopyTo($bz2Stream)
    $bz2Stream.Close()
    $fileStream.Close()
}
