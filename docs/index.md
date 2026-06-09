---
layout: default
title: Home
nav_order: 1
description: "deemon is a monitoring utility for new artist releases that can provide email alerts and automate downloading via the deemix library"
permalink: /
---

# deemon 2.23 Documentation
{: .fs-9 }

deemon is a monitoring utility for new artist releases that can provide email alerts and automate downloading via the deemix library
{: .fs-6 .fw-300 }

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub]({{ site.github.repository_url | default: site.repository_url | default: "https://github.com/mon5termatt/deemon" }}){: .btn .fs-5 .mb-4 .mb-md-0 }

<small>Version 2.23</small>
---

## Disclaimer

deemon does not download anything by itself. It requires a third party library 
called *deemix* in order to do this and will be installed automatically when 
installed via pip. [deemix on PyPI](https://pypi.org/project/deemix/)

Deemix Development has been discontinued and is no longer being actively developed. I will attempt to keep deemon updated with the latest versions of deemix as long as I can. if this becomes an issue, please open an issue on the GitHub repository. 

the maintained fork of deemix is not compatible with deemon and is not recommended for use. I will link to [bambanah/deemix](https://github.com/bambanah/deemix) for those who are interested in using it.

---

## Getting started

### Dependencies

deemon depends on various python modules and libraries to perform all of its functions. Please refer to the `requirements.txt` file to see what those dependencies are.

### Installation & Configuration

When you're ready to install deemon, head on over to the 
[installation]({{ site.baseurl }}{% link docs/installation.md %}) page. Once 
you've installed deemon, it is important to 
[configure]({{ site.baseurl }}{% link docs/configuration.md %}) it properly to 
get the best experience.


---

## About the project

deemon (**dee**zer **mon**itor) is an open source project that came from the need to stay on top of new 
releases by some of my favorite artists.

### License

deemon is distributed by a [GPL-3.0 license]({{ site.github.repository_url | default: site.repository_url | default: "https://github.com/mon5termatt/deemon" }}/blob/main/LICENSE).
