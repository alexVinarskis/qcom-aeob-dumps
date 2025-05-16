# AeoB dumps

ACPI tables on Windows devices are typically incomplete, as vendor drivers instead bring definitions in their own package. It appears that on Qualcomm WoA devices, these are provided as ACPI extensions in the form of AeoB files. [AeoBUtils project](https://github.com/WOA-Project/AeoBUtils) helps with decompiling AeoB files to dsl-like readable format.

This repo servers as an archive of _decompiled_ dumps for various Qualcomm Snapdragon laptops.


## How To Use

1. Download and compile AeoBUtils from [source](https://github.com/WOA-Project/AeoBUtils), or downlaod compiled version with arm64 from releases page of this repo.

2. Get access to all binary files present. Either mount/boot into Windows partition (binaries to be found in `C:\Windows\Systeme32\DriverData\FilerRepository`), or download BSP driver(s) from device support page, extract and flatten.

3. Extract all AeoB files from `.bin`. Run `extract-binaries.py` to find all files containing one or more AeoB files. Combination binaries require splitting into individual AeoB files"
```powershell
python extract-binaries.py \
     "C:\Windows\System32\DriverStore\FileRepository" \
     "C:\Users\...\folder-with-bins-here" \
```

4. Run `AeoBUtils.exe` tools on every file of interest. Sample usage in PowerShell:

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

5. PRs to this repo are appreaciated.
