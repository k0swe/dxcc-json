# DXCC JSON

This repository contains a JSON reference for amateur radio
[DX Century Club (DXCC)](https://www.arrl.org/dxcc) entities as maintained by the
[Amateur Radio Relay League (ARRL)](https://www.arrl.org). This is intended for consumption by other
amateur radio software.

The reference data started from the
[ARRL Country Lists & Prefixes](https://www.arrl.org/country-lists-prefixes) page, specifically the
[February 2020 text listing](https://www.arrl.org/files/file/DXCC/2020%20Current_Deleted.txt). That
document was imported into a
[Google Spreadsheet](https://docs.google.com/spreadsheets/d/1N1eMxi54yTwvizOzVeugWtLxfXGfK92WOavEjnfIdFw/edit#gid=0)
for formatting and cleansing. I added country codes, unicode flag glyphs and callsign prefix regular
expressions (regexes), and exported the spreadsheet as the CSV contained in this repository.
Finally, the included python script generates the JSON file.

One simple way to generate a smaller file with just what you need is to use the `jq` utility.

```commandline
$ < dxcc.json jq -c '{dxcc: [ .dxcc[] | select( .deleted==false ) | 
    {id: .entityCode, name: .name, prefixRegex: .prefixRegex, flag: .flag} ]}' > dxcc-filter.json

{
  "dxcc": [
    {
      "id": 1,
      "name": "Canada",
      "prefixRegex": "^V[A-GOY][A-Z0-9/]*$",
      "flag": "🇨🇦"
    },
    {
      "id": 3,
      "name": "Afghanistan",
      "prefixRegex": "^(YA|T6)[A-Z0-9/]*$",
      "flag": "🇦🇫"
    },
...
    {
      "id": 522,
      "name": "Kosovo",
      "prefixRegex": "^Z6[A-Z0-9/]*$",
      "flag": "🇽🇰"
    }
  ]
}
```
