# DXCC JSON

This repository contains a JSON reference for amateur radio
[DX Century Club (DXCC)](https://www.arrl.org/dxcc) entities as maintained by the
[Amateur Radio Relay League (ARRL)](https://www.arrl.org). This is intended for consumption by other
amateur radio software.

The reference data started from the
[ARRL Country Lists & Prefixes](https://www.arrl.org/country-lists-prefixes) page, specifically the
[January 2026 text listing](https://www.arrl.org/files/file/DXCC/Current_Deleted.txt). That
document was imported into a
[Google Spreadsheet](https://docs.google.com/spreadsheets/d/1N1eMxi54yTwvizOzVeugWtLxfXGfK92WOavEjnfIdFw/edit#gid=0)
for formatting and cleansing. I added country codes, unicode flag glyphs and callsign prefix regular
expressions (regexes), and exported the spreadsheet as the CSV contained in this repository. The DXCC entity fields (name, continent, ITU zone, CQ zone, and current/deleted status) were reconciled to ARRL's January 2026 listing; the manually maintained country codes, flags, and callsign regexes were retained.
Finally, the included python script generates the JSON file. Its top-level `metadata.sources`
array identifies the source documents and their editions, so consumers can determine the
data version without relying on a repository commit or file timestamp. The array permits
supplementary sources when a field is more accurately maintained outside ARRL's DXCC list.

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

## FAQ

### Can a callsign prefix uniquely identify a DXCC entity? Are they mutually exclusive?

No. The `prefixRegex` fields are useful for identifying candidate entities, but
some DXCC entities share callsign allocations. Applications should use an
operator's reported location, a QSL record, or other operation metadata when a
callsign matches more than one entity.

For example:

- `3D2R` was used for a [Rotuma Island DXpedition](http://www.yt1ad.info/3d2r/),
  but `3D2` is also used for Fiji and Conway Reef.
- `VP6DX` was the [2008 Ducie Island DXpedition](https://www.onallbands.com/qsl-review-a-look-back-at-the-qsl-card-from-ducie-island-vp6dx-2008/),
  while `VP6` is also used for Pitcairn Islands.
- `FO/VA7YM` has been used from the
  [Marquesas Islands](https://www.dx-world.net/fo-va7ym-marquesas-islands/),
  while `FO` also appears in the allocations for French Polynesia, Austral
  Islands, and Clipperton Island.
- `VP0SG` is a [South Georgia DXpedition callsign](https://dxnews.com/vp0sg/),
  but `VP0` also occurs in the allocations for South Orkney, South Sandwich,
  and South Shetland Islands.

Some regexes are deliberately broader than their associated DXCC entity to
represent these shared allocations. A regex match is therefore not, by itself,
proof of an entity.
