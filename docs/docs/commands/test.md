---
layout: default
title: test
parent: Commands
---

# test
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## SMTP settings test

deemon provides two ways to verify email notifications.

### Plaintext test

Use `test --email` to confirm SMTP connectivity with a simple plaintext message:

```bash
$ deemon test --email
```

### HTML test

Use `test --email-html` to send a preview of the real new-release notification email, including sample album art and formatting:

```bash
$ deemon test --email-html
```

This is useful for confirming that HTML rendering and album cover images display correctly in your mail client.

If you don't receive either test email, confirm your SMTP settings with your mail provider and check the logs for additional information.

---
## Exclusions test
If you have opted to use exclusion patterns or keywords to filter out releases, you may test those exclusions against any release URL to identify if that URL will be appropriately filtered out:

```
Artist: Various Artists
Album: Broken Bow (Remix)

Checking for the following patterns:
  1.  (?i)\bremix\b   >>   ** MATCH **

Checking for the following keywords:
  1.  remix   >>   ** MATCH **
  2.  deluxe   >>   NO MATCH
  3.  bonus   >>   NO MATCH
  4.  special   >>   NO MATCH
  5.  live   >>   NO MATCH

Result: This release would be excluded
```
