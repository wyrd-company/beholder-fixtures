#!/usr/bin/env python3
"""Generate or check THIRD-PARTY-NOTICES.md from the vendored packages.

Usage:
    third_party_notices.py            write THIRD-PARTY-NOTICES.md
    third_party_notices.py --check    exit 1 when the file is stale or a
                                      vendored package has no license

Only the Python standard library is used, and only tracked files are read.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "THIRD-PARTY-NOTICES.md"
FIRST_PARTY = ROOT / "scripts" / "first-party-packages.txt"

LICENSE_NAME = re.compile(r"^(licen[cs]e|copying|notice|third-?party-?notices?)", re.I)

TEXT_LICENSES = [
    ("MIT", "permission is hereby granted, free of charge"),
    ("Apache-2.0", "apache license"),
    ("BSD-3-Clause", "neither the name"),
    ("BSD-2-Clause", "redistributions in binary form"),
    ("0BSD", "permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted"),
    ("ISC", "permission to use, copy, modify, and/or distribute"),
    ("MPL-2.0", "mozilla public license"),
]


@dataclass
class Package:
    ecosystem: str
    name: str
    version: str
    license: str
    source: str
    license_files: set[str] = field(default_factory=set)
    locations: set[str] = field(default_factory=set)


def tracked() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def first_party() -> list[str]:
    if not FIRST_PARTY.exists():
        return []
    lines = FIRST_PARTY.read_text(encoding="utf-8").splitlines()
    return [l.split("#", 1)[0].strip() for l in lines if l.split("#", 1)[0].strip()]


def is_first_party(ecosystem: str, name: str, rules: list[str]) -> bool:
    key = f"{ecosystem}:{name}"
    for rule in rules:
        if rule.endswith("*") and key.startswith(rule[:-1]):
            return True
        if key == rule:
            return True
    return False


def text_license(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")[:6000].lower()
    text = re.sub(r"\s+", " ", text)
    for spdx, marker in TEXT_LICENSES:
        if marker in text:
            return spdx
    return "unknown"


def project_of(path: str) -> str:
    parts = PurePosixPath(path).parts
    return "/".join(parts[:4]) if len(parts) >= 4 else path


def license_files_in(directory: str, files: set[str]) -> set[str]:
    prefix = directory.rstrip("/") + "/"
    found = set()
    for f in files:
        if f.startswith(prefix) and "/" not in f[len(prefix):]:
            if LICENSE_NAME.match(PurePosixPath(f).name):
                found.add(f)
    return found


def add(packages: dict, pkg: Package, location: str, license_files: set[str]):
    key = (pkg.ecosystem, pkg.name, pkg.version)
    entry = packages.setdefault(key, pkg)
    entry.locations.add(location)
    entry.license_files.update(license_files)
    if entry.license == "unknown" and pkg.license != "unknown":
        entry.license = pkg.license


def scan() -> tuple[dict, list[str]]:
    files = tracked()
    fileset = set(files)
    rules = first_party()
    packages: dict = {}
    problems: list[str] = []

    for f in files:
        p = PurePosixPath(f)

        # Rust: one crate per directory directly under a project's vendor/.
        m = re.match(r"^(fixtures/rust/projects/[^/]+/vendor/[^/]+)/Cargo\.toml$", f)
        if m:
            text = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
            pkg_section = text.split("[package]", 1)[-1]
            name = re.search(r'^name\s*=\s*"([^"]+)"', pkg_section, re.M)
            version = re.search(r'^version\s*=\s*"([^"]+)"', pkg_section, re.M)
            lic = re.search(r'^license\s*=\s*"([^"]+)"', pkg_section, re.M)
            if not (name and version):
                continue
            n, v = name.group(1), version.group(1)
            if is_first_party("crate", n, rules):
                continue
            lfiles = license_files_in(m.group(1), fileset)
            spdx = lic.group(1).replace("/", " OR ") if lic else "unknown"
            if spdx == "unknown" and lfiles:
                spdx = text_license(ROOT / sorted(lfiles)[0])
            add(packages, Package("crate", n, v, spdx, f"https://crates.io/crates/{n}/{v}"), m.group(1), lfiles)
            continue

        # Dart: pub.dev packages in a project's vendored pub cache.
        m = re.match(r"^(fixtures/dart/projects/[^/]+/vendor/pub-cache/hosted/pub\.dev/([^/]+))/pubspec\.yaml$", f)
        if m:
            text = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
            name = re.search(r"^name:\s*['\"]?([^\s'\"]+)", text, re.M)
            version = re.search(r"^version:\s*['\"]?([^\s'\"]+)", text, re.M)
            if not name:
                continue
            n = name.group(1)
            v = version.group(1) if version else m.group(2).rsplit("-", 1)[-1]
            if is_first_party("pub", n, rules):
                continue
            lfiles = license_files_in(m.group(1), fileset)
            spdx = text_license(ROOT / sorted(lfiles)[0]) if lfiles else "unknown"
            add(packages, Package("pub", n, v, spdx, f"https://pub.dev/packages/{n}/versions/{v}"), m.group(1), lfiles)
            continue

        # npm: packages under node_modules/ or vendor/ in TypeScript projects.
        m = re.match(
            r"^(fixtures/typescript/projects/[^/]+/(?:.*/)?(?:node_modules|vendor)/(?:@[^/]+/)?[^/@][^/]*)/package\.json$",
            f,
        )
        if m:
            try:
                data = json.loads((ROOT / f).read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            n, v = data.get("name"), data.get("version") or "unversioned"
            if not n or data.get("private") is True or is_first_party("npm", n, rules):
                continue
            lic = data.get("license")
            if isinstance(lic, dict):
                lic = lic.get("type")
            lfiles = license_files_in(m.group(1), fileset)
            spdx = lic or (text_license(ROOT / sorted(lfiles)[0]) if lfiles else "unknown")
            add(packages, Package("npm", n, v, spdx, f"https://www.npmjs.com/package/{n}/v/{v}"), m.group(1), lfiles)
            continue

        # NuGet: package archives anywhere in a C# project.
        if f.endswith(".nupkg") and f.startswith("fixtures/csharp/"):
            try:
                z = zipfile.ZipFile(ROOT / f)
                spec = next(x for x in z.namelist() if x.endswith(".nuspec"))
                text = z.read(spec).decode("utf-8", errors="ignore")
                inner = [x for x in z.namelist() if LICENSE_NAME.match(PurePosixPath(x).name)]
            except (zipfile.BadZipFile, StopIteration, OSError):
                problems.append(f"{f}: not a readable NuGet package")
                continue
            n = re.search(r"<id>([^<]+)</id>", text).group(1)
            v = re.search(r"<version>([^<]+)</version>", text).group(1)
            if is_first_party("nuget", n, rules):
                continue
            expr = re.search(r"<license[^>]*type=\"expression\"[^>]*>([^<]+)<", text)
            url = re.search(r"<licenseUrl>([^<]+)<", text)
            spdx = expr.group(1) if expr else "unknown"
            lfiles = {f"{f}!{x}" for x in inner}
            # License texts copied beside the archives, named after the package.
            vendor = str(PurePosixPath(f).parent)
            prefix = n.lower() + "."
            for g in fileset:
                in_project = g.startswith(project_of(f) + "/")
                if not (in_project and ("/licenses/" in g or g.startswith(vendor + "/"))):
                    continue
                base = PurePosixPath(g).name.lower()
                rest = base[len(prefix):].lstrip("0123456789.") if base.startswith(prefix) else ""
                if rest and LICENSE_NAME.match(rest):
                    lfiles.add(g)
            if spdx == "unknown" and url:
                u = url.group(1)
                spdx = "MIT" if re.search(r"dotnet/(corefx|standard|core-setup)/", u) else "Microsoft .NET Library License" if "LinkId=329770" in u else (
                    "Apache-2.0" if "xunit" in u else f"see {u}")
            add(packages, Package("nuget", n, v, spdx, f"https://www.nuget.org/packages/{n}/{v}"), f, lfiles)
            continue

        # Go: vendored modules listed in vendor/modules.txt.
        if re.match(r"^fixtures/go/projects/[^/]+/vendor/modules\.txt$", f):
            for line in (ROOT / f).read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "#" and not parts[2].startswith("=>"):
                    n, v = parts[1], parts[2]
                    if is_first_party("go", n, rules):
                        continue
                    d = str(PurePosixPath(f).parent / n)
                    lfiles = license_files_in(d, fileset)
                    spdx = text_license(ROOT / sorted(lfiles)[0]) if lfiles else "unknown"
                    add(packages, Package("go", n, v, spdx, f"https://pkg.go.dev/{n}@{v}"), d, lfiles)

    for pkg in packages.values():
        label = f"{pkg.ecosystem} {pkg.name} {pkg.version}"
        if pkg.license == "unknown" or pkg.license.startswith("see "):
            if not pkg.license_files:
                problems.append(f"{label}: no license identified and no license file")
        if not pkg.license_files:
            pkg.license_files.add("")
    return packages, problems


ECOSYSTEMS = [
    ("crate", "Rust crates"),
    ("pub", "Dart packages"),
    ("npm", "npm packages"),
    ("nuget", "NuGet packages"),
    ("go", "Go modules"),
]

NOTES = {
    ("nuget", "Microsoft.NETCore.Platforms", "1.1.0"): (
        "Licensed under the Microsoft .NET Library license, not MIT. It permits "
        "distribution as part of a program, with conditions on distributors. "
        "Later versions of this package are MIT."
    ),
}


def render(packages: dict) -> str:
    out = [
        "<!-- rumdl-disable MD013 -->",
        "",
        "# Third-party notices",
        "",
        "This repository contains copies of third-party packages, kept so that",
        "every fixture project builds offline. Each package is licensed by its",
        "owners under the license listed here, not under this repository's",
        "`LICENSE`. Each package's own license and notice files stay beside it;",
        "the **License file** column names one of them.",
        "",
        "This file is generated by `task notices`. Do not edit it by hand.",
        "",
    ]
    for eco, title in ECOSYSTEMS:
        rows = sorted((p for p in packages.values() if p.ecosystem == eco), key=lambda p: (p.name.lower(), p.version))
        if not rows:
            continue
        out += [f"## {title}", "", "| Package | Version | License | License file | Copies |", "| --- | --- | --- | --- | --- |"]
        for p in rows:
            lf = sorted(x for x in p.license_files if x)
            lfile = f"`{lf[0]}`" if lf else "none"
            name = f"[{p.name}]({p.source})"
            out.append(f"| {name} | {p.version} | {p.license} | {lfile} | {len(p.locations)} |")
        out.append("")
    notes = [(k, v) for k, v in NOTES.items() if k in packages]
    if notes:
        out += ["## Notes", ""]
        for (eco, n, v), text in notes:
            out.append(f"- **{n} {v}**: {text}")
        out.append("")
    out += ["## Locations", ""]
    for eco, title in ECOSYSTEMS:
        for p in sorted((p for p in packages.values() if p.ecosystem == eco), key=lambda p: (p.name.lower(), p.version)):
            locs = ", ".join(f"`{project_of(l)}`" for l in sorted(p.locations))
            out.append(f"- {eco} {p.name} {p.version}: {locs}")
    out.append("")
    return "\n".join(out)


def main() -> int:
    packages, problems = scan()
    text = render(packages)
    check = "--check" in sys.argv[1:]
    for problem in sorted(problems):
        print(f"error: {problem}", file=sys.stderr)
    if check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != text:
            print("error: THIRD-PARTY-NOTICES.md is out of date; run `task notices`", file=sys.stderr)
            return 1
        return 1 if problems else 0
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.name}: {len(packages)} packages")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
