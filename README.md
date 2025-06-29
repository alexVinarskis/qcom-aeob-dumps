# AeoB dumps

ACPI tables on Windows devices are typically incomplete, as vendor drivers instead bring definitions in their own package. It appears that on Qualcomm WoA devices, these are provided as ACPI extensions in the form of AeoB files. [AeoBUtils project](https://github.com/WOA-Project/AeoBUtils) helps with decompiling AeoB files to dsl-like readable format.

This repo serves as an archive of _decompiled_ dumps for various Qualcomm Snapdragon laptops.


## How To Use

1. Download from the releases page in this repo, or compile AeoBUtils from [source](https://github.com/WOA-Project/AeoBUtils). If you want to compile it yourself, these steps might be instructional:
   - (Note: the project is written in C# and requires .NET SDK to build. Use `dotnet build` command in the root of the project to compile it.  The source code references .Net 6.0 in the `AeoBUtils.csproj` file, so you will need to have .NET 6.0 SDK installed, or change the source code to reference a newer version; e.g. .NET 8.0, which seems to work)
   - The binary will be available in `AeoBUtils\bin\Debug\netX.0\AeoBUtils.exe` after compilation, where `X` is the version of .NET you used to compile it.

2. Get access to all binary files present. Either mount/boot into Windows partition (binaries to be found in `C:\Windows\System32\DriverStore\FileRepository`), or download BSP driver(s) from device support page, extract and flatten.

3. Extract all AeoB files from `.bin`. Run the `extract-binaries.py` script from this repo to find all files containing one or more AeoB files. Combination binaries require splitting into individual AeoB files"
```powershell
python extract-binaries.py \
     "C:\Windows\System32\DriverStore\FileRepository" \
     "C:\Users\...\folder-with-bins-here" \
```

1. Run `AeoBUtils.exe` tools on every file of interest. Sample usage in PowerShell:

```powershell
$inputFolder = "C:\Users\...\folder-with-bins-here\"
$exePath = ".\AeoBUtils.exe"

Get-ChildItem -Path $inputFolder -Filter "*.bin" | ForEach-Object {
     $inputFile = $_.FullName
     $outputFile = [System.IO.Path]::ChangeExtension($inputFile, ".json")

     & $exePath aeob2aeobsl -p $inputFile -o $outputFile
}
```

Command above will fail on non-support files and simply continue the loop.

1. PRs to this repo are appreaciated.
