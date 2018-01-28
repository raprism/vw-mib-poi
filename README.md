# vw-mib-poi
Python scripts for POI import in Volkswagen Discover systems (MIB)

## intro
Custom installable POI collections for VW Discover Pro and Discover Media can be generated with Volkswagen's [Nav Companion](http://www.volkswagen-nav-companion.de/mib/ppoi/) site.

Small fixes like names, icons or e.g. 'warnable' settings can be done directly
for installable package files, but if might require correction of given
checksums or file length parameters.

A script checks these values to assist proper editing.

## usage
This script is implemented with Python 3.6, and should work well with version
\>=3.4. With some minor issues in print formatting it works also with recent
Python 2.7 releases.

```shell
> python check_POI_package.py -h

usage: check_POI_package.py [-h] <hashes.txt path>

positional arguments:
  <hashes.txt path>  Specify path of 'hashes.txt'. Typically:
                     PersonalPOI/Package/0/default/hashes.txt

optional arguments:
  -h, --help         show this help message and exit

> python check_POI_package.py PersonalPOI/Package/0/default/hashes.txt

bitmaps.xml                  passed      CheckSum = "1039cf6bc7bff0c844222d9aac97121bbf937db1"
bitmaps.xml                  passed      FileSize = "1144"
lang_map.xml                 passed      CheckSum = "f8a8295ab9b0b1451347dc80207c450f100ec632"
lang_map.xml                 passed      FileSize = "215"
versions.xml                 passed      CheckSum = "bc38aa443735d2395cd685a252db6bf746a34351"
versions.xml                 passed      FileSize = "496"
poidata.db                   passed      CheckSum = "e527399e33eef1c411150679022184e8b88b758f"
poidata.db                   passed      FileSize = "13153280"
bitmaps/001_image.png        passed      CheckSum = "7c586f9fc84ac11ea7be846f8e1e96d011b00ced"
bitmaps/001_image.png        passed      FileSize = "1922"
[...]

hashes.txt                   CheckSum = "de89ac79fc2d643905418a73974513705b69e030"
hashes.txt                   FileSize = "3164"

```

## disclaimer

No warranty at all.

Have fun! :penguin::sunglasses:

