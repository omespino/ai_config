---
name: google-vrp-android
description: 'Google VRP / Mobile VRP techniques for Android, Chrome extensions, iOS, low-level exploits. Android intent redirects without BROWSABLE (Scene Viewer, Firebase Dynamic Links, Play Store market://); path traversal in attachment filenames (Drive, Gmail, Chats); confused-deputy via cross-user content:// URIs (INTERACT_ACROSS_USERS); Task hijacking via missing taskAffinity (StrandHogg); Chrome extension UXSS via chrome.runtime.sendMessage; Tag Assistant SOP bypass; Application Launcher for Drive RCE via native messaging; Linux kernel UAF via io_uring (kernelCTF $11.3M); v8CTF OOB write; Fuchsia/gVisor PRNG seed leak. Checklists: exported activities/providers, intent:// redirects, path traversal, StrandHogg, Chrome extension externally_connectable. Source: 202 public HoF reports. Spanish triggers — "android google", "mobile vrp", "chrome extension", "intent android", "kernelctf", "v8ctf", "chrome xss", "aplicacion android google", "google play", "extension chrome".'
---

# Google VRP — Android / Chrome / Mobile / Kernel Techniques

Subset of 202-report public Hall-of-Fame. Focus: Android apps, Chrome browser extensions, mobile VRP, kernel/v8CTF, iOS, Google Fiber.
Use alongside `google-vrp-cloud` and `google-vrp-web`.

---

## Recurring patterns (mobile/chrome domain)

15. **Android intent redirects / BROWSABLE bypass** — Google App / Scene Viewer / Faceviewer / Firebase Dynamic Links forward `intent://` URIs without the `BROWSABLE` category, defeating Chromium's mitigation and choosing arbitrary browsers/apps.
16. **Path traversal in Android app downloads / Drive / Gmail** — filename `../../../foo` accepted by Google Chats, Gmail. Combined with TCC entitlement inheritance on macOS Drive (child injection) for permission escalation.
17. **Confused-deputy in Google Play Services** — `ACTION_PICK` with cross-user `content://10@media/external/images/media/<id>` URI; GMS reads with `INTERACT_ACROSS_USERS`.

---

## Per-report catalog

### #1 — $11,333,700 — David Bouman — kernelCTF — Linux Kernel io_uring (CVE-2022-2602)
UAF in `io_uring` registered files: `unix_scm_cycle_create` GC freed a fixed file still in use by a queued request. Cross-cache primitive: free victim slab, reallocate same pages via `__get_free_pages` from `io_mem_alloc()` (rings/sqes mmap-ed to userspace → freed object is live in user memory, no header pollution, no allocator races). `IORING_OP_RECVMSG` side-channel through provided buffers to leak `socket_file_operations` byte-by-byte; `IORING_OP_FADVISE → netdev_init` to leak controlled buffer address; `__io_commit_cqring` (32-bit write) + `bsg_get_command_q` (32-bit read) gadgets to flip cred/nsproxy. Reliability ~80–90%.

### #16 — $1,000,000 — madStacks — v8CTF — n-day v8 OOB write
Reproduced from public regression test of v8 commit 10b0e62e. R/W/AOF primitives in v8 sandbox, leaked WebAssembly RWX page address from WasmInstance object, ROP via `mov` constant gadgets, copied final shellcode to RWX page.

### #21 — $750,000 — Amit Klein et al. — Fuchsia/gVisor PRNG seed leak
Network-stack secrets predictable from observed TCP ISN, TCP timestamp, source ports, IPv4/IPv6 fragment IDs. Discloses internal IP behind NAT, enables DNS cache poisoning, TCP blind reset, IPv4 ID hash collision attacks, device tracking across networks. Files: `gvisor.dev/gvisor/pkg/tcpip/` and `golang/go/src/math/rand/rng.go`.

### #35 — $500,000 — NDevTK — Tag Assistant Legacy SOP bypass
On any site: `chrome.runtime.sendMessage({message:'LoadScript', url:'http://192.168.1.1'}, console.log)` — content script proxies arbitrary HTTP fetches and returns response; reads internal LAN pages.

### #45 — $500,000 — Jun Kokatsu — User-Agent Switcher extension UXSS
Compromised renderer: `chrome.extension.sendRequest({action:"add_ua", user_agent:"X'+alert(origin)+'"})`  injects UA into the content script's `Object.defineProperty` template → executes JS on every site that reads `navigator.userAgent`.

### #50 — $450,000 — Thrivikram Guruprasad — Mobile VRP — Google Chats Android path traversal
Attachment filename `../../../PathTraversal/code.txt` writes outside `/Download` to `/storage/emulated/0/PathTraversal`.

### #51 — $450,000 — NDevTK — Google App Faceviewer trusts gstatic
`<a href="faceviewer://arvr.google.com/faceviewer?arbi=1&wturl=https://ssl.gstatic.com/<reflected-xss-on-gstatic>">` then `faceViewerWebXBridge.postMessage(JSON.stringify({cmd: btoa(':\x0f\n\rtestintent://')}))` invokes a non-browsable intent from the web.

### #52 — $450,000 — NDevTK — Play Store `market://` intent bypass
`market://details?id=com.sec.android.app.sbrowser&url=https%3A%2F%2Fexample.org` opens Samsung Browser to attacker URL without prompting, bypassing Chromium's other-browser launch dialog.

### #59 — $313,370 — Khaled Elmasrey — Google Fiber `ubus` JSON-RPC unauth reboot
`POST /ubus` with `{"method":"call","params":["00000000…","session","login",{"username":"","password":""}]}` returns a session, then `system reboot` reboots the router. Also `assist` username on more locked-down hosts.

### #60 — $313,370 — NDevTK — Google App fullscreen spoof via Scene Viewer / Faceviewer
`faceviewer://` and `intent://arvr.google.com/scene-viewer/...` open in fullscreen without warning toast — full address-bar spoof.

### #62 — $313,370 — NDevTK — Application Launcher For Drive lax messaging
`externally_connectable.matches: ["*://*.google.com/*"]` lets any `google.com` subdomain (including `http://`) post to extension; `chrome.runtime.connect('lmjegmlicamnimmfhcmpkclmigmmcbeh',{name:'com.google.drive.nativeproxy'})` opens shared `.vbs` files via native messaging on Windows → RCE.

### #69 — $313,370 — Jun Kokatsu — Google Translate extension UXSS
Compromised renderer sets `chrome.storage.local.set({gtxTargetLang:"X'+alert(1)+'"})`; later code-injects into translated page.

### #78 — $187,500 — Jatin — Google Keep `VoiceActionActivity` exported
`adb shell am start-activity -a com.google.android.gms.actions.CREATE_NOTE --es android.intent.extra.TEXT testing com.google.android.keep/.activities.VoiceActionActivity` lets any 3rd-party app create / delete / update notes.

### #89 — $133,700 — sithi — GMS confused-deputy across Android users
`ACTION_PICK` returns `content://10@media/external/images/media/<id>` (cross-user URI). GMS reads with `INTERACT_ACROSS_USERS` and shows the image (another user's photos / contact pics) in the profile-photo crop.

### #92 — $112,500 — NDevTK — Google App webapp install spoof via intent
`location.href='intent://search.app.goo.gl/?link=…name=Chrome…icon=…&query=https://attacker#Intent;package=com.google.android.googlequicksearchbox;end&apn=…#Intent;package=com.google.android.gms;…'` shows install prompt without origin and with attacker-chosen icon; can also bypass home-screen step.

### #101 — $50,000 — GMS in-app browser exposes JS bridge `mm`
Long click-trail leads to a "private" browser without parental controls, exposing `addEncryptionRecoveryMethod`, `setVaultSharedKeys`, `closeView` — a pinned-app bypass surface.

### #116 — $50,000 — Jatin — `GmsSubscribedFeedsProvider` exported with no permission
`adb shell content query --uri content://com.google.android.gms.subscribedfeeds/accounts` returns Google account list and sync feeds without any Android permission.

---

## Recent additions (2023–2025, from public writeups)

### Pixel lock screen bypass — CVE-2022-20465 ($70k)
Pixel phones running Android 13 before the November 2022 patch could bypass the lock screen by inserting a SIM card from a carrier that triggers a SIM-PUK flow. The SIM unlock screen allowed launching the Emergency Dialer, then accessing the Recent Calls list and opening contacts — defeating the lock screen without the PIN. Root cause: SIM-PUK dialog rendered on top of keyguard without proper `FLAG_SHOW_WHEN_LOCKED` restrictions. Reporter: David Schutz.

### Google Home wiretap chain — $107,500
Chain of two bugs found in Google Home mini: (1) An unauthenticated API endpoint (`/setup/eureka_info`) exposed the device's local cloud device ID and certificate. (2) A `routines` API accepted new device links without verifying that the linker was the device owner — anyone on the LAN could link a "spy routine" that triggered the microphone remotely. Effectively a zero-click LAN wiretap. Reporter: Matt Kunze.

### CVE-2024-0044 — Android app installer signature bypass ($8k)
Android's `PackageInstaller` in versions before the March 2024 patch allowed a pre-installed app with `INSTALL_PACKAGES` to install a package update that changed the signing certificate without the user's consent. A system app (e.g., a carrier bloatware) could silently "upgrade" itself to a version signed by a different key, effectively impersonating any installed app. Root cause: `PackageManagerService.checkUpgradeKeySetLP()` not enforced in the silent-install path.

### ChromeOS File Manager XSS via `filesystem:` URL — CVE-2023-4369 ($10k)
The ChromeOS Files app (`chrome://file-manager`) opened user-selected files using `filesystem:chrome-extension://...` URLs. An HTML file with a crafted `Content-Type` or an SVG with embedded `<script>` rendered in the extension origin, allowing XSS within the file manager extension's privilege level (access to `chrome.fileSystem`, `chrome.fileBrowserHandler`).

### Chrome Extensions multi-bug chain — $18,833
Three bugs chained across separate Chrome extensions shipped by Google:
1. **Application Launcher for Drive** (`lmjegmlicamnimmfhcmpkclmigmmcbeh`): lax `externally_connectable` + native messaging proxy → arbitrary file open/RCE (see existing #62).
2. **Perfetto UI** extension: `chrome.devtools.network.getHAR` accessible via compromised renderer → exfiltrates all network traffic including OAuth tokens.
3. **Screen Reader** (ChromeVox): `chrome.accessibilityFeatures.spokenFeedback` writable by any `*.google.com` page → enables screenreader, then intercepts `chrome.tts.speak` events to extract page content.
Reporter: NDevTK.

### Google Assistant voice injection via Web Speech API ($3,133)
`assistant.google.com` used the Web Speech API for voice input. The `SpeechRecognition` result was directly appended to the assistant query string without sanitization. An attacker page embedding the assistant in an iframe with appropriate permissions could call `speechSynthesis.speak()` to produce audio that the microphone picked up and was transcribed, injecting arbitrary commands into the assistant session.

### Wear OS CVE-2025-12080 — intent abuse
Wear OS companion app exported activity `com.google.android.gms.wearable.BIND_LISTENER` accepted `intent://` deep links from the watch face context without validating the package origin. A malicious watch face could send `intent://...#Intent;package=com.android.settings;...` launching sensitive Settings screens on the paired phone.

### Chrome Gemini side panel hijack ($7k)
Chrome's built-in Gemini side panel (`chrome://side-panel/`) communicated with the active tab via `chrome.tabs.sendMessage`. A page injecting a content script (e.g., via a Chrome extension with broad permissions, or a compromised renderer) could intercept or spoof these messages, injecting content into the Gemini conversation or reading Gemini's responses to the user.

### IDX VSCode Worker XSS — $22,500
Project IDX's embedded VS Code worker ran as a Web Worker on `*.idx.cloudworkstations.dev`. The extension host iframe (`webWorkerExtensionHostIframe.html`) read `parentOrigin` from the URL query string and used it as the `targetOrigin` for `postMessage`. An XSS on any `*.cloudworkstations.googleusercontent.com` subdomain (e.g., from an uploaded `.ipynb` notebook) could frame the IDE and send spoofed messages, reaching the worker context → Login-CSRF → full IDE takeover. (Related to #4 in the web skill.)

### Android web attack surface — Firebase, Clock, Faceviewer ($14k)
Three separate mobile VRP reports bundled:
- **Firebase Dynamic Links** (`goo.gl`/`page.link` resolver): forwards `intent://` URIs including non-BROWSABLE ones, allowing arbitrary app launch from a web link.
- **Google Clock** Android app: exported `AlarmActivity` accepted `ACTION_SET_ALARM` intents from third-party apps without permission, allowing silent alarm creation (calendar/time awareness).
- **Faceviewer** (AR mode in Google App): deep link `faceviewer://arvr.google.com/faceviewer?wturl=<gstatic-xss>` reflected a gstatic-hosted XSS into a WebView and triggered a non-BROWSABLE intent from web context.

---

## $0 reports (one-liners)
- **#159** `mkto-sj380051.com` (CNAME from `email.mandiant.com`) HTTPS certificate mismatch.
- **#167** Google App Scene Viewer launches arbitrary `intent://` (BROWSABLE bypass).
- **#172** Calendar deeplink RSVP without consent — `adb shell am start-activity -d 'https://calendar.google.com/calendar/event?eid=<base64_event_id_email>&action=RESPOND&rst=2'` responds Yes/No/Maybe. `eid` is base64 `<event_id> <email>@m`.
- **#175** Firebase Dynamic Links opens arbitrary intents (e.g. Samsung Browser) bypassing Chromium's non-default-browser prompt.
- **#188** YouTube Studio Android task hijacking via missing `taskAffinity` (StrandHogg v1).
- **#190** `ads-resources-legacy.waze.com` outdated nginx 1.4.6 (potentially CVE-2014-0133 SPDY).
- **#196** Android Google Password Autofill biometric requirement disabled without authentication.
- **#200** Nearby Connections WiFi pivot — P2P_STAR: malicious advertiser switches discoverer's WiFi to attacker AP, sets default route via DHCP → captures all victim Internet traffic.

---

## Checklists

### Android Google apps:
- `android:exported=true` activities/providers/services without permission.
- `intent://` redirects without `CATEGORY_BROWSABLE` enforcement (Scene Viewer, Faceviewer, Firebase Dynamic Links, Google App, Play Store `market://`).
- path traversal in attachment filenames (Drive, Gmail, Chats) — `../../../foo`.
- `taskAffinity` collisions for task hijacking (StrandHogg v1).
- `content://<userId>@…` cross-user URI confused-deputy on apps with `INTERACT_ACROSS_USERS`.
- TCC entitlement inheritance via child injection on macOS desktop builds (`--debugger_command`).
- exported content providers missing permission checks (e.g. `GmsSubscribedFeedsProvider`).

### Browser extensions Google ships:
- `externally_connectable.matches` containing `*://*.google.com/*` and `http://` (allows any http google.com subdomain).
- background scripts trusting `chrome.storage.local.set` from content scripts on arbitrary sites.
- helpers that proxy fetches without origin checks (arbitrary LAN page reads).
- compromised-renderer threat model: `chrome.runtime.sendMessage` from a content script of any URL.
- native messaging handlers opening files/executables without path validation.

### Lock screen / physical security (Pixel / Android):
- SIM-PUK unlock flow rendering above keyguard without `FLAG_DISMISS_KEYGUARD` enforcement.
- Emergency Dialer reachable from lock screen → Recent Calls → Contacts chain.
- `PackageInstaller` silent-upgrade path skipping signing key verification (`checkUpgradeKeySetLP`).
- Biometric bypass via fallback credential (PIN/pattern) accessible without device lock on some flows.

### Wearables and companion apps:
- Exported `BIND_LISTENER` activities on Wear OS companion accepting `intent://` from watch face context.
- Watch face context treated as trusted sender without package origin validation.

### Chrome AI features (side panel, extensions):
- Gemini side panel `chrome.tabs.sendMessage` interceptable by content scripts with broad match patterns.
- VS Code worker iframe reading `parentOrigin` from query string (IDX / Cloud Workstations pattern).
- Extension devtools APIs (`chrome.devtools.network.getHAR`) accessible from compromised renderers → OAuth token exfil.

### IoT / local network:
- LAN-accessible setup APIs without authentication (Google Home `/setup/eureka_info`, Google Fiber `/ubus`).
- Device-linking APIs that don't verify requester is the device owner.
- DHCP-based MITM on GCE VMs / local LAN devices — intercepts metadata token requests.
