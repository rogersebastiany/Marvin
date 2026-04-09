Scan images for software vulnerabilities in Amazon ECR - Amazon ECR 

Scan images for software vulnerabilities in Amazon ECR - Amazon ECR
{
"@context" : "https://schema.org",
"@type" : "BreadcrumbList",
"itemListElement" : [
{
"@type" : "ListItem",
"position" : 1,
"name" : "AWS",
"item" : "https://aws.amazon.com"
},
{
"@type" : "ListItem",
"position" : 2,
"name" : "Amazon ECR",
"item" : "https://docs.aws.amazon.com/ecr/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/AmazonECR/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Scan images for software vulnerabilities in Amazon ECR",
"item" : "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html"
}
]
}

[Documentation](/index.html)[Amazon ECR](/ecr/index.html)[User Guide](what-is-ecr.html)

# Scan images for software vulnerabilities in Amazon ECR

Amazon ECR image scanning helps to identify software vulnerabilities in your container images.
The following scanning types are offered.

###### Important

Switching between **Enhanced scanning** and **Basic
scanning** will cause previously established scans to no longer be available. You will have to set
up your scans again. However, if you switch back to your previous scanning type the
established scans will be available.

###### Note

Archived images cannot be scanned. Archived images must be restored before they can be
scanned. For more information about archiving and restoring images, see [Archiving an image in Amazon ECR](./archive_restore_image.html).

* **Enhanced scanning** – Amazon ECR integrates with Amazon Inspector to
  provide automated, continuous scanning of your repositories. Your container images
  are scanned for both operating systems and programming language package
  vulnerabilities. As new vulnerabilities appear, the scan results are updated and
  Amazon Inspector emits an event to EventBridge to notify you. Enhanced scanning provides the
  following:

  + OS and programming languages package vulnerabilities
  + Two scanning frequencies: Scan on push and continuous scan
* **Basic scanning** – Amazon ECR uses AWS native technology
  with the Common Vulnerabilities and Exposures (CVEs) database to scan for operating
  system vulnerabilities.

  With basic scanning, you configure your repositories to scan on push or you can
  perform manual scans and
  Amazon ECR provides a list of scan findings. Basic scanning provides the
  following:

  + OS scans
  + Two scanning frequencies: Manual and scan on push

  ###### Important

  The new version of Amazon ECR Basic Scanning doesn't use the `imageScanFindingsSummary` and `imageScanStatus` attributes from
  the `DescribeImages` API response to return scan results. Use the `DescribeImageScanFindings` API instead. For more information, see [`DescribeImageScanFindings`](https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_DescribeImageScanFindings.html).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Manual signing

Filters for repositories

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.