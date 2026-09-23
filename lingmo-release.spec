# Lingmo OS release files.
# Replaces Fedora's fedora-release so the OS identity cannot be tampered with
# or left over from the base distribution.

Name:           lingmo-release
Version:        5
Release:        1%{?dist}
Summary:        Lingmo OS release files
License:        MIT
URL:            https://lingmo.org/
BuildArch:      noarch

Source1:        os-release
Source2:        issue
Source3:        issue.net
Source4:        LICENSE

# Provide the generic "system-release" capability used by tools (e.g. lorax,
# livecd-tools, anaconda) to detect the distribution.
# Version 45 matches the Fedora base so "Requires: system-release >= 23"
# (lvm2, systemd, etc.) resolve correctly.
Provides:       system-release = 45
Provides:       system-release(45) = 45

# Replace Fedora's release files so only Lingmo OS identity is present.
# Use version 45 (matching the Fedora base) so packages with
# "Requires: fedora-release >= 23" (e.g. systemd) resolve correctly.
Provides:       fedora-release = 45
Provides:       fedora-release-common = 45
Provides:       fedora-release-identity-basic = 45
Obsoletes:      fedora-release < 100
Obsoletes:      fedora-release-common < 100
Obsoletes:      fedora-release-identity-basic < 100
Obsoletes:      fedora-release-identity-wsl < 100

Requires:       filesystem

%description
Lingmo OS release files, defining the operating system identity
(/etc/os-release, /etc/issue, /etc/system-release and friends).

It obsoletes and replaces Fedora's fedora-release package so that the
system is always identified as Lingmo OS.

%prep
# No sources to unpack.

%build
# Nothing to build.

%install
# Base directories
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_prefix}/lib
install -d %{buildroot}%{_prefix}/lib/rpm/macros.d

# os-release (real file in /usr/lib, symlink from /etc)
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/os-release
ln -sf ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# issue / issue.net
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/issue
install -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/issue.net
ln -sf ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue
ln -sf ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Lingmo OS branded release file (analogous to /etc/fedora-release)
cat > %{buildroot}%{_prefix}/lib/lingmo-release <<'EOF'
Lingmo OS release 5 (Unstable)
EOF
ln -sf ../usr/lib/lingmo-release %{buildroot}%{_sysconfdir}/lingmo-release

# redhat-release for legacy tooling compatibility
ln -sf lingmo-release %{buildroot}%{_sysconfdir}/redhat-release

# system-release -> lingmo-release
ln -sf lingmo-release %{buildroot}%{_sysconfdir}/system-release

# CPE name
cat > %{buildroot}%{_prefix}/lib/system-release-cpe <<'EOF'
cpe:/o:lingmo:lingmo:5
EOF
ln -sf ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe

# RPM %dist macro so packages built against Lingmo OS are tagged correctly
cat > %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.dist <<'EOF'
# dist macros for Lingmo OS
%%dist %%{nil}.lingmo5
%%lingmo5 1
EOF

# License
install -d %{buildroot}%{_licensedir}/lingmo-release
install -m 0644 %{SOURCE4} %{buildroot}%{_licensedir}/lingmo-release/LICENSE

%files
%license %{_licensedir}/lingmo-release/LICENSE
%{_prefix}/lib/os-release
%{_prefix}/lib/issue
%{_prefix}/lib/issue.net
%{_prefix}/lib/lingmo-release
%{_prefix}/lib/system-release-cpe
%{_prefix}/lib/rpm/macros.d/macros.dist
%config %{_sysconfdir}/os-release
%{_sysconfdir}/issue
%{_sysconfdir}/issue.net
%{_sysconfdir}/lingmo-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe

%changelog
* Wed Sep 23 2026 Lingmo OS Team <team@lingmo.org> - 5-1
- Initial Lingmo OS release files
