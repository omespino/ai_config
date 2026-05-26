# Google Web Designer Attack Surfaces

This reference summarizes public Google Web Designer client-side RCE research by Bálint Magyar and CVE records. Use it for authorized bug bounty analysis and safe reproductions only.

## Sources

- Bálint Magyar, "Client-side RCE via CSS Injection in Google Web Designer for Windows", published August 30, 2025: https://balintmagyar.com/articles/google-web-designer-css-injection-client-rce
- Bálint Magyar, "Client-side RCE via Improper URL Parsing in Google Web Designer for Windows: CVE-2025-4613", published May 22, 2025: https://balintmagyar.com/articles/google-web-designer-path-traversal-client-side-rce-cve-2025-4613
- Bálint Magyar, "Client-side RCE via symlink following in Google Web Designer for macOS/Linux: CVE-2025-1079": https://balintmagyar.com/articles/google-web-designer-symlink-client-side-rce-cve-2025-1079
- NVD CVE-2025-1079: https://nvd.nist.gov/vuln/detail/CVE-2025-1079
- NVD CVE-2025-4613: https://nvd.nist.gov/vuln/detail/CVE-2025-4613

## Known Issue Matrix

| Issue | Platforms | Affected versions | Fixed version | Root cause | Main user action |
| --- | --- | --- | --- | --- | --- |
| CVE-2025-1079 | macOS, Linux | before 16.2.0.0128 | 16.2.0.0128 | Improper symlink/link resolution in preview | Open malicious source package and preview it |
| CVE-2025-4613 | Windows | before 16.3.0.0407 | 16.3.0.0407 | Improper URL parsing and path traversal in template `remoteAssets` | Use/edit malicious template |
| CSS injection RCE | Windows | before 16.4.0.0711 | 16.4.0.0711 | CSS injection from `gwd_workspace.json` reaching Chrome/CEF command-line behavior | Open malicious ad and use Swatches UI |

## CVE-2025-4613: Template `remoteAssets` Path Traversal

Key primitive: template HTML can include JSON metadata in:

```html
<script id="gwd-template-data" type="application/json">
{
  "remoteAssets": [
    "https://example.test/assets/image.jpg"
  ]
}
</script>
```

Known vulnerable behavior:

- Google Web Designer fetched URLs from `remoteAssets` when using or editing templates.
- The local destination filename was derived from the substring after the last `/` in the full URL.
- URL fragments or query strings could influence the derived filename differently from what a web server receives.
- On Windows, backslash traversal sequences could escape the intended `assets/` directory.

Safe test approach:

1. Use an owned HTTP server that serves a harmless text file with `Access-Control-Allow-Origin: *` if needed.
2. Add a `remoteAssets` entry whose fragment-derived filename contains a traversal marker.
3. Aim the write at a controlled, disposable directory or harmless marker path in a lab VM, not Startup, user profile persistence locations, or sensitive files.
4. Confirm whether the downloaded file lands outside the template `assets/` directory.
5. Report arbitrary file write as the core issue; only demonstrate code execution with benign local action if the bounty rules require and permit it.

Report facts:

- Public CVE description: path traversal in Google Web Designer template handling before 16.3.0.0407 on Windows can lead to RCE via malicious ad templates.
- NVD lists CWE-22 and CWE-20, CVSS 3.1 score 8.8 high, vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H`.

## CVE-2025-1079: Symlink Following In Preview

Key primitive: a malicious source package on macOS/Linux could include symbolic links that Google Web Designer's preview feature resolved outside the intended project boundary.

Safe test approach:

1. Build the package in a disposable macOS/Linux lab user account.
2. Include a symlink that points to a harmless local marker target or test-only executable/script.
3. Open the source package in the vulnerable version and use built-in preview.
4. Observe whether preview follows the symlink and crosses the package boundary.
5. Keep evidence focused on link resolution, boundary escape, and user interaction.

Report facts:

- Public CVE description: client RCE on macOS and Linux via improper symbolic link resolution in Google Web Designer's preview feature.
- Affected versions are before 16.2.0.0128.
- NVD/CNA list CWE-61 and NVD also lists CWE-59; CVSS 3.1 score 7.8 high, vector `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H`.

## CSS Injection RCE: `gwd_workspace.json` Swatches

Key primitive: `gwd_workspace.json` can store custom color palette data:

```json
{
  "color.customColorPalettes": [
    {
      "name": "documentSwatches",
      "color_data": [
        { "css": "rgba(110,110,255,1)" }
      ]
    }
  ]
}
```

Known vulnerable behavior:

- Google Web Designer is a Chromium Embedded Framework app with HTML/CSS/JS UI surfaces.
- Custom swatch CSS from `gwd_workspace.json` was used in a CSS `background` rule for color tiles.
- The public write-up chains CSS injection to an exposed internal API and then to command injection via Chrome executable arguments on Windows.
- The published impact required the victim to open a malicious ad document and interact with the color picker Swatches UI.
- The issue was fixed in 16.4.0.0711.

Safe test approach:

1. Mutate only the `css` field in `color.customColorPalettes`.
2. Start with visual-only injection probes that make a tile visibly distinct.
3. Check whether CSS values can break expected declaration context or load remote/local resources.
4. If an internal bridge/API is exposed, demonstrate reachability with a harmless proof, not arbitrary command payloads.
5. Verify whether Windows-only behavior exists; do not assume macOS/Linux exploitability because subprocess argument handling differs.

## Regression Ideas

- Validate all file writes remain under the intended template/project root after URL normalization.
- Normalize URLs before deriving filenames, then reject path separators, drive letters, UNC prefixes, control chars, fragments, and traversal.
- Resolve symlinks before preview access and enforce canonical path containment.
- Treat project configuration as untrusted input, especially CSS inserted into app UI.
- Search for similar fields: `localAssets`, `assets`, `components`, `preview`, `template`, `style`, `css`, `url`, `path`, and any JSON-in-HTML metadata.

## Report Checklist

- Title: include product, platform, primitive, and impact.
- Scope: state authorization and tested version.
- Summary: one paragraph that names the trust boundary crossed.
- Steps: minimal package tree and deterministic UI actions.
- Impact: explain arbitrary file write, path escape, symlink escape, CSS injection, or command execution separately.
- Evidence: screenshots, filesystem before/after, network logs, and process launch only when allowed.
- Fix guidance: canonical path containment, strict URL parsing, deny symlink escapes, CSS sanitization, and platform-specific tests.
- Regression comparison: explain how the candidate differs from or bypasses CVE-2025-1079, CVE-2025-4613, or the CSS injection fix.
