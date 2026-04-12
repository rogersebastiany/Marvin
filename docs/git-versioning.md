# Git and Versioning


---

## 1. Conventional Commits 1.0.0

## Summary

The Conventional Commits specification is a lightweight convention on top of commit messages.
It provides an easy set of rules for creating an explicit commit history;
which makes it easier to write automated tools on top of.
This convention dovetails with [SemVer](http://semver.org),
by describing the features, fixes, and breaking changes made in commit messages.

The commit message should be structured as follows:

---

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

---

The commit contains the following structural elements, to communicate intent to the
consumers of your library:

1. **fix:** a commit of the *type* `fix` patches a bug in your codebase (this correlates with [`PATCH`](http://semver.org/#summary) in Semantic Versioning).
2. **feat:** a commit of the *type* `feat` introduces a new feature to the codebase (this correlates with [`MINOR`](http://semver.org/#summary) in Semantic Versioning).
3. **BREAKING CHANGE:** a commit that has a footer `BREAKING CHANGE:`, or appends a `!` after the type/scope, introduces a breaking API change (correlating with [`MAJOR`](http://semver.org/#summary) in Semantic Versioning).
   A BREAKING CHANGE can be part of commits of any *type*.
4. *types* other than `fix:` and `feat:` are allowed, for example [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (based on the [Angular convention](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)) recommends `build:`, `chore:`,
   `ci:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others.
5. *footers* other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to
   [git trailer format](https://git-scm.com/docs/git-interpret-trailers).

Additional types are not mandated by the Conventional Commits specification, and have no implicit effect in Semantic Versioning (unless they include a BREAKING CHANGE).
A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., `feat(parser): add ability to parse arrays`.

## Examples

### Commit message with description and breaking change footer

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### Commit message with `!` to draw attention to breaking change

```
feat!: send an email to the customer when a product is shipped
```

### Commit message with scope and `!` to draw attention to breaking change

```
feat(api)!: send an email to the customer when a product is shipped
```

### Commit message with both `!` and BREAKING CHANGE footer

```
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

### Commit message with no body

```
docs: correct spelling of CHANGELOG
```

### Commit message with scope

```
feat(lang): add Polish language
```

### Commit message with multi-paragraph body and multiple footers

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

1. Commits MUST be prefixed with a type, which consists of a noun, `feat`, `fix`, etc., followed
   by the OPTIONAL scope, OPTIONAL `!`, and REQUIRED terminal colon and space.
2. The type `feat` MUST be used when a commit adds a new feature to your application or library.
3. The type `fix` MUST be used when a commit represents a bug fix for your application.
4. A scope MAY be provided after a type. A scope MUST consist of a noun describing a
   section of the codebase surrounded by parenthesis, e.g., `fix(parser):`
5. A description MUST immediately follow the colon and space after the type/scope prefix.
   The description is a short summary of the code changes, e.g., *fix: array parsing issue when multiple spaces were contained in string*.
6. A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
7. A commit body is free-form and MAY consist of any number of newline separated paragraphs.
8. One or more footers MAY be provided one blank line after the body. Each footer MUST consist of
   a word token, followed by either a `:<space>` or `<space>#` separator, followed by a string value (this is inspired by the
   [git trailer convention](https://git-scm.com/docs/git-interpret-trailers)).
9. A footer’s token MUST use `-` in place of whitespace characters, e.g., `Acked-by` (this helps differentiate
   the footer section from a multi-paragraph body). An exception is made for `BREAKING CHANGE`, which MAY also be used as a token.
10. A footer’s value MAY contain spaces and newlines, and parsing MUST terminate when the next valid footer
    token/separator pair is observed.
11. Breaking changes MUST be indicated in the type/scope prefix of a commit, or as an entry in the
    footer.
12. If included as a footer, a breaking change MUST consist of the uppercase text BREAKING CHANGE, followed by a colon, space, and description, e.g.,
    *BREAKING CHANGE: environment variables now take precedence over config files*.
13. If included in the type/scope prefix, breaking changes MUST be indicated by a
    `!` immediately before the `:`. If `!` is used, `BREAKING CHANGE:` MAY be omitted from the footer section,
    and the commit description SHALL be used to describe the breaking change.
14. Types other than `feat` and `fix` MAY be used in your commit messages, e.g., *docs: update ref docs.*
15. The units of information that make up Conventional Commits MUST NOT be treated as case-sensitive by implementors, with the exception of BREAKING CHANGE which MUST be uppercase.
16. BREAKING-CHANGE MUST be synonymous with BREAKING CHANGE, when used as a token in a footer.

## Why Use Conventional Commits

* Automatically generating CHANGELOGs.
* Automatically determining a semantic version bump (based on the types of commits landed).
* Communicating the nature of changes to teammates, the public, and other stakeholders.
* Triggering build and publish processes.
* Making it easier for people to contribute to your projects, by allowing them to explore
  a more structured commit history.

## FAQ

### How should I deal with commit messages in the initial development phase?

We recommend that you proceed as if you’ve already released the product. Typically *somebody*, even if it’s your fellow software developers, is using your software. They’ll want to know what’s fixed, what breaks etc.

### Are the types in the commit title uppercase or lowercase?

Any casing may be used, but it’s best to be consistent.

### What do I do if the commit conforms to more than one of the commit types?

Go back and make multiple commits whenever possible. Part of the benefit of Conventional Commits is its ability to drive us to make more organized commits and PRs.

### Doesn’t this discourage rapid development and fast iteration?

It discourages moving fast in a disorganized way. It helps you be able to move fast long term across multiple projects with varied contributors.

### Might Conventional Commits lead developers to limit the type of commits they make because they’ll be thinking in the types provided?

Conventional Commits encourages us to make more of certain types of commits such as fixes. Other than that, the flexibility of Conventional Commits allows your team to come up with their own types and change those types over time.

### How does this relate to SemVer?

`fix` type commits should be translated to `PATCH` releases. `feat` type commits should be translated to `MINOR` releases. Commits with `BREAKING CHANGE` in the commits, regardless of type, should be translated to `MAJOR` releases.

### How should I version my extensions to the Conventional Commits Specification, e.g. `@jameswomack/conventional-commit-spec`?

We recommend using SemVer to release your own extensions to this specification (and
encourage you to make these extensions!)

### What do I do if I accidentally use the wrong commit type?

#### When you used a type that’s of the spec but not the correct type, e.g. `fix` instead of `feat`

Prior to merging or releasing the mistake, we recommend using `git rebase -i` to edit the commit history. After release, the cleanup will be different according to what tools and processes you use.

#### When you used a type *not* of the spec, e.g. `feet` instead of `feat`

In a worst case scenario, it’s not the end of the world if a commit lands that does not meet the Conventional Commits specification. It simply means that commit will be missed by tools that are based on the spec.

### Do all my contributors need to use the Conventional Commits specification?

No! If you use a squash based workflow on Git lead maintainers can clean up the commit messages as they’re merged—adding no workload to casual committers.
A common workflow for this is to have your git system automatically squash commits from a pull request and present a form for the lead maintainer to enter the proper git commit message for the merge.

### How does Conventional Commits handle revert commits?

Reverting code can be complicated: are you reverting multiple commits? if you revert a feature, should the next release instead be a patch?

Conventional Commits does not make an explicit effort to define revert behavior. Instead we leave it to tooling
authors to use the flexibility of *types* and *footers* to develop their logic for handling reverts.

One recommendation is to use the `revert` type, and a footer that references the commit SHAs that are being reverted:

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

---

## 2. Semantic Versioning 2.0.0

## Summary

Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when you make incompatible API changes
2. MINOR version when you add functionality in a backward compatible
   manner
3. PATCH version when you make backward compatible bug fixes

Additional labels for pre-release and build metadata are available as extensions
to the MAJOR.MINOR.PATCH format.

## Introduction

In the world of software management there exists a dreaded place called
“dependency hell.” The bigger your system grows and the more packages you
integrate into your software, the more likely you are to find yourself, one
day, in this pit of despair.

In systems with many dependencies, releasing new package versions can quickly
become a nightmare. If the dependency specifications are too tight, you are in
danger of version lock (the inability to upgrade a package without having to
release new versions of every dependent package). If dependencies are
specified too loosely, you will inevitably be bitten by version promiscuity
(assuming compatibility with more future versions than is reasonable).
Dependency hell is where you are when version lock and/or version promiscuity
prevent you from easily and safely moving your project forward.

As a solution to this problem, we propose a simple set of rules and
requirements that dictate how version numbers are assigned and incremented.
These rules are based on but not necessarily limited to pre-existing
widespread common practices in use in both closed and open-source software.
For this system to work, you first need to declare a public API. This may
consist of documentation or be enforced by the code itself. Regardless, it is
important that this API be clear and precise. Once you identify your public
API, you communicate changes to it with specific increments to your version
number. Consider a version format of X.Y.Z (Major.Minor.Patch). Bug fixes not
affecting the API increment the patch version, backward compatible API
additions/changes increment the minor version, and backward incompatible API
changes increment the major version.

We call this system “Semantic Versioning.” Under this scheme, version numbers
and the way they change convey meaning about the underlying code and what has
been modified from one version to the next.

## Semantic Versioning Specification (SemVer)

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”,
“SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

1. Software using Semantic Versioning MUST declare a public API. This API
   could be declared in the code itself or exist strictly in documentation.
   However it is done, it SHOULD be precise and comprehensive.
2. A normal version number MUST take the form X.Y.Z where X, Y, and Z are
   non-negative integers, and MUST NOT contain leading zeroes. X is the
   major version, Y is the minor version, and Z is the patch version.
   Each element MUST increase numerically. For instance: 1.9.0 -> 1.10.0 -> 1.11.0.
3. Once a versioned package has been released, the contents of that version
   MUST NOT be modified. Any modifications MUST be released as a new version.
4. Major version zero (0.y.z) is for initial development. Anything MAY change
   at any time. The public API SHOULD NOT be considered stable.
5. Version 1.0.0 defines the public API. The way in which the version number
   is incremented after this release is dependent on this public API and how it
   changes.
6. Patch version Z (x.y.Z | x > 0) MUST be incremented if only backward
   compatible bug fixes are introduced. A bug fix is defined as an internal
   change that fixes incorrect behavior.
7. Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backward
   compatible functionality is introduced to the public API. It MUST be
   incremented if any public API functionality is marked as deprecated. It MAY be
   incremented if substantial new functionality or improvements are introduced
   within the private code. It MAY include patch level changes. Patch version
   MUST be reset to 0 when minor version is incremented.
8. Major version X (X.y.z | X > 0) MUST be incremented if any backward
   incompatible changes are introduced to the public API. It MAY also include minor
   and patch level changes. Patch and minor versions MUST be reset to 0 when major
   version is incremented.
9. A pre-release version MAY be denoted by appending a hyphen and a
   series of dot separated identifiers immediately following the patch
   version. Identifiers MUST comprise only ASCII alphanumerics and hyphens
   [0-9A-Za-z-]. Identifiers MUST NOT be empty. Numeric identifiers MUST
   NOT include leading zeroes. Pre-release versions have a lower
   precedence than the associated normal version. A pre-release version
   indicates that the version is unstable and might not satisfy the
   intended compatibility requirements as denoted by its associated
   normal version. Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7,
   1.0.0-x.7.z.92, 1.0.0-x-y-z.--.
10. Build metadata MAY be denoted by appending a plus sign and a series of dot
    separated identifiers immediately following the patch or pre-release version.
    Identifiers MUST comprise only ASCII alphanumerics and hyphens [0-9A-Za-z-].
    Identifiers MUST NOT be empty. Build metadata MUST be ignored when determining
    version precedence. Thus two versions that differ only in the build metadata,
    have the same precedence. Examples: 1.0.0-alpha+001, 1.0.0+20130313144700,
    1.0.0-beta+exp.sha.5114f85, 1.0.0+21AF26D3----117B344092BD.
11. Precedence refers to how versions are compared to each other when ordered.

    1. Precedence MUST be calculated by separating the version into major,
       minor, patch and pre-release identifiers in that order (Build metadata
       does not figure into precedence).
    2. Precedence is determined by the first difference when comparing each of
       these identifiers from left to right as follows: Major, minor, and patch
       versions are always compared numerically.

       Example: 1.0.0 < 2.0.0 < 2.1.0 < 2.1.1.
    3. When major, minor, and patch are equal, a pre-release version has lower
       precedence than a normal version:

       Example: 1.0.0-alpha < 1.0.0.
    4. Precedence for two pre-release versions with the same major, minor, and
       patch version MUST be determined by comparing each dot separated identifier
       from left to right until a difference is found as follows:

       1. Identifiers consisting of only digits are compared numerically.
       2. Identifiers with letters or hyphens are compared lexically in ASCII
          sort order.
       3. Numeric identifiers always have lower precedence than non-numeric
          identifiers.
       4. A larger set of pre-release fields has a higher precedence than a
          smaller set, if all of the preceding identifiers are equal.

       Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta <
       1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0.

## Backus–Naur Form Grammar for Valid SemVer Versions

```
<valid semver> ::= <version core>
                 | <version core> "-" <pre-release>
                 | <version core> "+" <build>
                 | <version core> "-" <pre-release> "+" <build>

<version core> ::= <major> "." <minor> "." <patch>

<major> ::= <numeric identifier>

<minor> ::= <numeric identifier>

<patch> ::= <numeric identifier>

<pre-release> ::= <dot-separated pre-release identifiers>

<dot-separated pre-release identifiers> ::= <pre-release identifier>
                                          | <pre-release identifier> "." <dot-separated pre-release identifiers>

<build> ::= <dot-separated build identifiers>

<dot-separated build identifiers> ::= <build identifier>
                                    | <build identifier> "." <dot-separated build identifiers>

<pre-release identifier> ::= <alphanumeric identifier>
                           | <numeric identifier>

<build identifier> ::= <alphanumeric identifier>
                     | <digits>

<alphanumeric identifier> ::= <non-digit>
                            | <non-digit> <identifier characters>
                            | <identifier characters> <non-digit>
                            | <identifier characters> <non-digit> <identifier characters>

<numeric identifier> ::= "0"
                       | <positive digit>
                       | <positive digit> <digits>

<identifier characters> ::= <identifier character>
                          | <identifier character> <identifier characters>

<identifier character> ::= <digit>
                         | <non-digit>

<non-digit> ::= <letter>
              | "-"

<digits> ::= <digit>
           | <digit> <digits>

<digit> ::= "0"
          | <positive digit>

<positive digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
           | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
           | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d"
           | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n"
           | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x"
           | "y" | "z"
```

## Why Use Semantic Versioning?

This is not a new or revolutionary idea. In fact, you probably do something
close to this already. The problem is that “close” isn’t good enough. Without
compliance to some sort of formal specification, version numbers are
essentially useless for dependency management. By giving a name and clear
definition to the above ideas, it becomes easy to communicate your intentions
to the users of your software. Once these intentions are clear, flexible (but
not too flexible) dependency specifications can finally be made.

A simple example will demonstrate how Semantic Versioning can make dependency
hell a thing of the past. Consider a library called “Firetruck.” It requires a
Semantically Versioned package named “Ladder.” At the time that Firetruck is
created, Ladder is at version 3.1.0. Since Firetruck uses some functionality
that was first introduced in 3.1.0, you can safely specify the Ladder
dependency as greater than or equal to 3.1.0 but less than 4.0.0. Now, when
Ladder version 3.1.1 and 3.2.0 become available, you can release them to your
package management system and know that they will be compatible with existing
dependent software.

As a responsible developer you will, of course, want to verify that any
package upgrades function as advertised. The real world is a messy place;
there’s nothing we can do about that but be vigilant. What you can do is let
Semantic Versioning provide you with a sane way to release and upgrade
packages without having to roll new versions of dependent packages, saving you
time and hassle.

If all of this sounds desirable, all you need to do to start using Semantic
Versioning is to declare that you are doing so and then follow the rules. Link
to this website from your README so others know the rules and can benefit from
them.

## FAQ

### How should I deal with revisions in the 0.y.z initial development phase?

The simplest thing to do is start your initial development release at 0.1.0
and then increment the minor version for each subsequent release.

### How do I know when to release 1.0.0?

If your software is being used in production, it should probably already be
1.0.0. If you have a stable API on which users have come to depend, you should
be 1.0.0. If you’re worrying a lot about backward compatibility, you should
probably already be 1.0.0.

### Doesn’t this discourage rapid development and fast iteration?

Major version zero is all about rapid development. If you’re changing the API
every day you should either still be in version 0.y.z or on a separate
development branch working on the next major version.

### If even the tiniest backward incompatible changes to the public API require a major version bump, won’t I end up at version 42.0.0 very rapidly?

This is a question of responsible development and foresight. Incompatible
changes should not be introduced lightly to software that has a lot of
dependent code. The cost that must be incurred to upgrade can be significant.
Having to bump major versions to release incompatible changes means you’ll
think through the impact of your changes, and evaluate the cost/benefit ratio
involved.

### Documenting the entire public API is too much work!

It is your responsibility as a professional developer to properly document
software that is intended for use by others. Managing software complexity is a
hugely important part of keeping a project efficient, and that’s hard to do if
nobody knows how to use your software, or what methods are safe to call. In
the long run, Semantic Versioning, and the insistence on a well defined public
API can keep everyone and everything running smoothly.

### What do I do if I accidentally release a backward incompatible change as a minor version?

As soon as you realize that you’ve broken the Semantic Versioning spec, fix
the problem and release a new minor version that corrects the problem and
restores backward compatibility. Even under this circumstance, it is
unacceptable to modify versioned releases. If it’s appropriate,
document the offending version and inform your users of the problem so that
they are aware of the offending version.

### What should I do if I update my own dependencies without changing the public API?

That would be considered compatible since it does not affect the public API.
Software that explicitly depends on the same dependencies as your package
should have their own dependency specifications and the author will notice any
conflicts. Determining whether the change is a patch level or minor level
modification depends on whether you updated your dependencies in order to fix
a bug or introduce new functionality. We would usually expect additional code
for the latter instance, in which case it’s obviously a minor level increment.

### What if I inadvertently alter the public API in a way that is not compliant with the version number change (i.e. the code incorrectly introduces a major breaking change in a patch release)?

Use your best judgment. If you have a huge audience that will be drastically
impacted by changing the behavior back to what the public API intended, then
it may be best to perform a major version release, even though the fix could
strictly be considered a patch release. Remember, Semantic Versioning is all
about conveying meaning by how the version number changes. If these changes
are important to your users, use the version number to inform them.

### How should I handle deprecating functionality?

Deprecating existing functionality is a normal part of software development and
is often required to make forward progress. When you deprecate part of your
public API, you should do two things: (1) update your documentation to let
users know about the change, (2) issue a new minor release with the deprecation
in place. Before you completely remove the functionality in a new major release
there should be at least one minor release that contains the deprecation so
that users can smoothly transition to the new API.

### Does SemVer have a size limit on the version string?

No, but use good judgment. A 255 character version string is probably overkill,
for example. Also, specific systems may impose their own limits on the size of
the string.

### Is “v1.2.3” a semantic version?

No, “v1.2.3” is not a semantic version. However, prefixing a semantic version
with a “v” is a common way (in English) to indicate it is a version number.
Abbreviating “version” as “v” is often seen with version control. Example:
`git tag v1.2.3 -m "Release version 1.2.3"`, in which case “v1.2.3” is a tag
name and the semantic version is “1.2.3”.

### Is there a suggested regular expression (RegEx) to check a SemVer string?

There are two. One with named groups for those systems that support them
(PCRE [Perl Compatible Regular Expressions, i.e. Perl, PHP and R], Python
and Go).

See: <https://regex101.com/r/Ly7O1x/3/>

```
^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
```

And one with numbered capture groups instead (so cg1 = major, cg2 = minor,
cg3 = patch, cg4 = prerelease and cg5 = buildmetadata) that is compatible
with ECMA Script (JavaScript), PCRE (Perl Compatible Regular Expressions,
i.e. Perl, PHP and R), Python and Go.

See: <https://regex101.com/r/vkijKf/1/>

```
^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
```

## About

The Semantic Versioning specification was originally authored by [Tom
Preston-Werner](https://tom.preston-werner.com), inventor of Gravatar and
cofounder of GitHub.

If you’d like to leave feedback, please [open an issue on
GitHub](https://github.com/semver/semver/issues).

## License

[Creative Commons ― CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

---

## 3. 3.2 Git Branching - Basic Branching and Merging

2nd Edition

# 3.2 Git Branching - Basic Branching and Merging

## Basic Branching and Merging

Let’s go through a simple example of branching and merging with a workflow that you might use in the real world.
You’ll follow these steps:

1. Do some work on a website.
2. Create a branch for a new user story you’re working on.
3. Do some work in that branch.

At this stage, you’ll receive a call that another issue is critical and you need a hotfix.
You’ll do the following:

1. Switch to your production branch.
2. Create a branch to add the hotfix.
3. After it’s tested, merge the hotfix branch, and push to production.
4. Switch back to your original user story and continue working.

### Basic Branching

First, let’s say you’re working on your project and have a couple of commits already on the `master` branch.

Figure 18. A simple commit history

You’ve decided that you’re going to work on issue #53 in whatever issue-tracking system your company uses.
To create a new branch and switch to it at the same time, you can run the `git checkout` command with the `-b` switch:

```
$ git checkout -b iss53
Switched to a new branch "iss53"
```

This is shorthand for:

```
$ git branch iss53
$ git checkout iss53
```

Figure 19. Creating a new branch pointer

You work on your website and do some commits.
Doing so moves the `iss53` branch forward, because you have it checked out (that is, your `HEAD` is pointing to it):

```
$ vim index.html
$ git commit -a -m 'Create new footer [issue 53]'
```

Figure 20. The `iss53` branch has moved forward with your work

Now you get the call that there is an issue with the website, and you need to fix it immediately.
With Git, you don’t have to deploy your fix along with the `iss53` changes you’ve made, and you don’t have to put a lot of effort into reverting those changes before you can work on applying your fix to what is in production.
All you have to do is switch back to your `master` branch.

However, before you do that, note that if your working directory or staging area has uncommitted changes that conflict with the branch you’re checking out, Git won’t let you switch branches.
It’s best to have a clean working state when you switch branches.
There are ways to get around this (namely, stashing and commit amending) that we’ll cover later on, in [Stashing and Cleaning](/book/en/v2/ch00/_git_stashing).
For now, let’s assume you’ve committed all your changes, so you can switch back to your `master` branch:

```
$ git checkout master
Switched to branch 'master'
```

At this point, your project working directory is exactly the way it was before you started working on issue #53, and you can concentrate on your hotfix.
This is an important point to remember: when you switch branches, Git resets your working directory to look like it did the last time you committed on that branch.
It adds, removes, and modifies files automatically to make sure your working copy is what the branch looked like on your last commit to it.

Next, you have a hotfix to make.
Let’s create a `hotfix` branch on which to work until it’s completed:

```
$ git checkout -b hotfix
Switched to a new branch 'hotfix'
$ vim index.html
$ git commit -a -m 'Fix broken email address'
[hotfix 1fb7853] Fix broken email address
 1 file changed, 2 insertions(+)
```

Figure 21. Hotfix branch based on `master`

You can run your tests, make sure the hotfix is what you want, and finally merge the `hotfix` branch back into your `master` branch to deploy to production.
You do this with the `git merge` command:

```
$ git checkout master
$ git merge hotfix
Updating f42c576..3a0874c
Fast-forward
 index.html | 2 ++
 1 file changed, 2 insertions(+)
```

You’ll notice the phrase “fast-forward” in that merge.
Because the commit `C4` pointed to by the branch `hotfix` you merged in was directly ahead of the commit `C2` you’re on, Git simply moves the pointer forward.
To phrase that another way, when you try to merge one commit with a commit that can be reached by following the first commit’s history, Git simplifies things by moving the pointer forward because there is no divergent work to merge together — this is called a “fast-forward.”

Your change is now in the snapshot of the commit pointed to by the `master` branch, and you can deploy the fix.

Figure 22. `master` is fast-forwarded to `hotfix`

After your super-important fix is deployed, you’re ready to switch back to the work you were doing before you were interrupted.
However, first you’ll delete the `hotfix` branch, because you no longer need it — the `master` branch points at the same place.
You can delete it with the `-d` option to `git branch`:

```
$ git branch -d hotfix
Deleted branch hotfix (3a0874c).
```

Now you can switch back to your work-in-progress branch on issue #53 and continue working on it.

```
$ git checkout iss53
Switched to branch "iss53"
$ vim index.html
$ git commit -a -m 'Finish the new footer [issue 53]'
[iss53 ad82d7a] Finish the new footer [issue 53]
1 file changed, 1 insertion(+)
```

Figure 23. Work continues on `iss53`

It’s worth noting here that the work you did in your `hotfix` branch is not contained in the files in your `iss53` branch.
If you need to pull it in, you can merge your `master` branch into your `iss53` branch by running `git merge master`, or you can wait to integrate those changes until you decide to pull the `iss53` branch back into `master` later.

### Basic Merging

Suppose you’ve decided that your issue #53 work is complete and ready to be merged into your `master` branch.
In order to do that, you’ll merge your `iss53` branch into `master`, much like you merged your `hotfix` branch earlier.
All you have to do is check out the branch you wish to merge into and then run the `git merge` command:

```
$ git checkout master
Switched to branch 'master'
$ git merge iss53
Merge made by the 'recursive' strategy.
index.html |    1 +
1 file changed, 1 insertion(+)
```

This looks a bit different than the `hotfix` merge you did earlier.
In this case, your development history has diverged from some older point.
Because the commit on the branch you’re on isn’t a direct ancestor of the branch you’re merging in, Git has to do some work.
In this case, Git does a simple three-way merge, using the two snapshots pointed to by the branch tips and the common ancestor of the two.

Figure 24. Three snapshots used in a typical merge

Instead of just moving the branch pointer forward, Git creates a new snapshot that results from this three-way merge and automatically creates a new commit that points to it.
This is referred to as a merge commit, and is special in that it has more than one parent.

Figure 25. A merge commit

Now that your work is merged in, you have no further need for the `iss53` branch.
You can close the issue in your issue-tracking system, and delete the branch:

```
$ git branch -d iss53
```

### Basic Merge Conflicts

Occasionally, this process doesn’t go smoothly.
If you changed the same part of the same file differently in the two branches you’re merging, Git won’t be able to merge them cleanly.
If your fix for issue #53 modified the same part of a file as the `hotfix` branch, you’ll get a merge conflict that looks something like this:

```
$ git merge iss53
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

Git hasn’t automatically created a new merge commit.
It has paused the process while you resolve the conflict.
If you want to see which files are unmerged at any point after a merge conflict, you can run `git status`:

```
$ git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)

    both modified:      index.html

no changes added to commit (use "git add" and/or "git commit -a")
```

Anything that has merge conflicts and hasn’t been resolved is listed as unmerged.
Git adds standard conflict-resolution markers to the files that have conflicts, so you can open them manually and resolve those conflicts.
Your file contains a section that looks something like this:

```
<<<<<<< HEAD:index.html
<div id="footer">contact : email.support@github.com</div>
=======
<div id="footer">
 please contact us at support@github.com
</div>
>>>>>>> iss53:index.html
```

This means the version in `HEAD` (your `master` branch, because that was what you had checked out when you ran your merge command) is the top part of that block (everything above the `=======`), while the version in your `iss53` branch looks like everything in the bottom part.
In order to resolve the conflict, you have to either choose one side or the other or merge the contents yourself.
For instance, you might resolve this conflict by replacing the entire block with this:

```
<div id="footer">
please contact us at email.support@github.com
</div>
```

This resolution has a little of each section, and the `<<<<<<<`, `=======`, and `>>>>>>>` lines have been completely removed.
After you’ve resolved each of these sections in each conflicted file, run `git add` on each file to mark it as resolved.
Staging the file marks it as resolved in Git.

If you want to use a graphical tool to resolve these issues, you can run `git mergetool`, which fires up an appropriate visual merge tool and walks you through the conflicts:

```
$ git mergetool

This message is displayed because 'merge.tool' is not configured.
See 'git mergetool --tool-help' or 'git help config' for more details.
'git mergetool' will now attempt to use one of the following tools:
opendiff kdiff3 tkdiff xxdiff meld tortoisemerge gvimdiff diffuse diffmerge ecmerge p4merge araxis bc3 codecompare vimdiff emerge
Merging:
index.html

Normal merge conflict for 'index.html':
  {local}: modified file
  {remote}: modified file
Hit return to start merge resolution tool (opendiff):
```

If you want to use a merge tool other than the default (Git chose `opendiff` in this case because the command was run on macOS), you can see all the supported tools listed at the top after “one of the following tools.”
Just type the name of the tool you’d rather use.

|  |  |
| --- | --- |
| Note | If you need more advanced tools for resolving tricky merge conflicts, we cover more on merging in [Advanced Merging](/book/en/v2/ch00/_advanced_merging). |

After you exit the merge tool, Git asks you if the merge was successful.
If you tell the script that it was, it stages the file to mark it as resolved for you.
You can run `git status` again to verify that all conflicts have been resolved:

```
$ git status
On branch master
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:

    modified:   index.html
```

If you’re happy with that, and you verify that everything that had conflicts has been staged, you can type `git commit` to finalize the merge commit.
The commit message by default looks something like this:

```
Merge branch 'iss53'

Conflicts:
    index.html
#
# It looks like you may be committing a merge.
# If this is not correct, please remove the file
#	.git/MERGE_HEAD
# and try again.

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
# On branch master
# All conflicts fixed but you are still merging.
#
# Changes to be committed:
#	modified:   index.html
#
```

If you think it would be helpful to others looking at this merge in the future, you can modify this commit message with details about how you resolved the merge and explain why you did the changes you made if these are not obvious.

---

## 4. git-rebase

```
git rebase [-i | --interactive] [<options>] [--exec <cmd>]
	[--onto <newbase> | --keep-base] [<upstream> [<branch>]]
git rebase [-i | --interactive] [<options>] [--exec <cmd>] [--onto <newbase>]
	--root [<branch>]
git rebase (--continue|--skip|--abort|--quit|--edit-todo|--show-current-patch)
```

---

## Bibliography

1. [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
2. [Semantic Versioning 2.0.0](https://semver.org/)
3. [3.2 Git Branching - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
4. [git-rebase](https://git-scm.com/docs/git-rebase)