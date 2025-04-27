# AeoB dumps

ACPI tables on Windows devices are typically incomplete, as vendor drivers instead bring definitions in their own package. It appears that on Qualcomm WoA devices, these are provided as ACPI extensions in the form of AeoB files. [AeoBUtils project](https://github.com/WOA-Project/AeoBUtils) helps with decompiling AeoB files to dsl-like readable format.

This repo servers as an archive of _decompiled_ dumps for various Qualcomm Snapdragon laptops.


## How To Use

1. Download and compile AeoBUtils from [source](https://github.com/WOA-Project/AeoBUtils), or downlaod compiled version with arm64 from releases page of this repo.

2. Extract all `.bin` files to a folder. Either copy it over from Windows partition, or download BSP driver(s) from device support page, extract and flatten.

3. Run `AeoBUtils.exe` tools on every file of interest. Sample usage in PowerShell:

```powershell
$inputFolder = "C:\Users\...\folder-with-bins-here\"
$exePath = ".\AeoBUtils.exe"

Get-ChildItem -Path $inputFolder -Filter "*.bin" | ForEach-Object {
     $inputFile = $_.FullName
     $outputFile = [System.IO.Path]::ChangeExtension($inputFile, ".json")

     & $exePath aeob2aeobsl -p $inputFile -o $outputFile
}
```

Not all `.bin` files are AeoB files, it appears only CAPITALIZEDFILES.bin are the latter. Command above will fail on non-support files and simply continue the loop.

4. PRs to this repo are appreaciated.
