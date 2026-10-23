# Download checksums (SHA-256)

Fingerprints of the current release downloads of each app (taken from the Mac-Apps release. Ludus is the current 1.10.0 build; Memo, Nox and Awayke are the last published builds: Memo v1.1, Nox v1.0.0, Awayke v1.4.0).

```
Ludus (1.10.0):
ba73aa086e5187052f9d4ec578ce71da76ed9cac1b82c5a920f925e4409db420  Ludus-mac.zip
b509c6ff9942c323f79011b5074c7f0a8389d576d8d5743591ab5f171c1cb9b0  Ludus-windows.zip
4e3753e0bc85ac58381045e2ffefdc759019a2a780c620839aee429628d4ddb5  Ludus.dmg

Memo:
41df5c8f62660687a4e35e898a9c079866b01893ec6e432847997c55e2734b7d  Memo-mac.zip
0de1566489bdede6fab1c0269b6fcd550eb057e84248f4131565b6ee72e144b7  Memo-windows.zip

Nox:
2d5c2ce5c9abd75e05b7ef01c69239f53cd76e032fe17ae16d4ecc38174775c8  Nox-mac.zip
8512c4b2defac25fffda87de9491837c233e5c96b0120eee135f79031a4d8337  Nox-windows.zip
b65b8912e82f709e157af754c0dbd30db923154e7c85c96ab53b92ba6087e13b  Nox.dmg

Awayke:
3a4d2d538ed71ae196c7d8b75a498c84e9ff846ed6be1c678e4367530d33b7a9  Awayke-1.4.0.zip
eb209e71a33540924c6f958eaaa191c642a8f4bdb5e29808b7a81fdc158082e2  Awayke.dmg
```

Memo 1.1.1, Nox 1.0.1 and Awayke 1.4.1 are the current versions. Their downloads are not published yet, so their fingerprints are added when they are released.

Check on Mac: `shasum -a 256 <file>`. Check on Windows: `certutil -hashfile <file> SHA256`.
