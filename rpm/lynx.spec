# $LynxId: lynx.spec,v 1.91 2024/05/31 22:09:16 tom Exp $
Summary: A text-based Web browser
Name: lynx
Version: 2.9.2
Release: 1
License: GPLv2
Group: Applications/Internet
# Source: https://invisible-island.net/archives/lynx/lynx%%{version}.tgz
Source: %{name}-%{version}.tgz
URL: https://lynx.invisible-island.net
Provides: webclient >= 0.0
Provides: text-www-browser >= 0.0
Packager: Peter Leinchen (for SFOS) <peterleinchen@t-online.de>

# Fedora:
BuildRequires: pkgconfig, ncurses-devel >= 5.3-5,
BuildRequires: zlib-devel, gettext
## BuildRequires: libidn-devel
BuildRequires: openssl-devel
BuildRequires: bzip2-devel

# SuSE:
# BuildRequires: libbz2-devel
# BuildRequires: libopenssl-1_1-devel, or
# BuildRequires: libopenssl-3-devel                   

Requires: brotli, gzip, bzip2, tar, zip, unzip

%description
Lynx is a fully-featured World Wide Web (WWW) client for users running cursor-addressable, \
character-cell display devices. 
It is very fast and easy to use. 
It will display HTML documents containing links to files residing on the local system, \
as well as files residing on remote systems running Gopher, HTTP, FTP, WAIS, \
and NNTP servers.

%package doc
Summary:    Help files and documentation for the lynx text browser
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
This package contains the interactive HTML help files, user guides, 
man pages, and sample configurations for the Lynx web browser.

%define lynx_doc %{_defaultdocdir}/%{name}
%define lynx_etc %{_sysconfdir}/%{name}
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
%configure \
        --target %{_target_platform} \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{lynx_doc} \
        --libdir=%{lynx_etc} \
        --mandir=%{_mandir} \
        --sysconfdir=%{lynx_etc} \
        --with-cfg-path=%{lynx_etc}:%{lynx_doc}/samples \
        --with-textdomain=%{name} \
        --enable-cgi-links \
        --enable-change-exec \
        --enable-charset-choice \
        --enable-default-colors \
        --enable-exec-links \
        --enable-exec-scripts \
        --enable-externs \
        --enable-font-switch \
        --enable-gzip-help \
        --enable-htmlized-cfg \
        --enable-internal-links \
        --enable-ipv6 \
        --enable-kbd-layout \
        --enable-local-docs \
        --enable-nested-tables \
        --enable-nls \
        --enable-nsl-fork \
        --enable-syslog \
        --enable-warnings \
        --with-screen=ncursesw \
        --with-ssl \
    --without-idn \
    --disable-idna
make \
        docdir=%{lynx_doc}

%install
rm -rf $RPM_BUILD_ROOT
chmod -x samples/mailto-form.pl

make install-full \
        DESTDIR=$RPM_BUILD_ROOT \
        docdir=%{lynx_doc}

cat >>$RPM_BUILD_ROOT%{lynx_etc}/lynx.cfg <<EOF
DEFAULT_INDEX_FILE:http://www.google.com/
LOCALE_CHARSET:TRUE
EOF

strip $RPM_BUILD_ROOT%{_bindir}/%{name}

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/%{name}
%config(noreplace) %{lynx_etc}/*.cfg
%config(noreplace) %{lynx_etc}/*.lss

%files doc
%defattr(-,root,root,-)
%{_mandir}/*/*
%dir %{lynx_doc}

# Use wildcards to safely pull in whatever documentation files actually exist
%{lynx_doc}/CHANGES*
%{lynx_doc}/COPYHEADER*
%{lynx_doc}/COPYING*
%{lynx_doc}/PROBLEM*
%{lynx_doc}/README*

# Directories containing help layout frameworks
%{lynx_doc}/docs/
%{lynx_doc}/lynx_help/
%{lynx_doc}/samples/
%{lynx_doc}/test/


%changelog
* Mon May 18 2026 Peter Leinchen (for SFOS) <peterleinchen@t-online.de>
- Split out large help files, test suites, and man pages into a separate doc package for SFOS.

* Thu Mar 14 2024 Thomas E. Dickey
- trim redundant options

* Mon Jan 15 2024 Thomas E. Dickey
- simplified tarball name

* Sun Jan 07 2024 Thomas E. Dickey
- use rpm #find_lang macro for configuring language files
- use noreplace flag for *.cfg and *.lss config files
- remove obsolete #clean section

* Tue Mar 29 2022 Thomas E. Dickey
- add brotli compression

* Sat Jul 31 2021 Thomas E. Dickey
- align configure-options with Debian package, removing some which are not
  needed because they correspond to the default settings.

* Thu May 17 2018 Thomas E. Dickey
- use "ncursesw6dev", reflecting renaming of ncurses test-packages to avoid
  conflict with new packages in Fedora.

* Mon Mar 12 2018 Thomas E. Dickey
- rename to "lynx-dev", add a few dependencies where package names are same.

* Fri Sep 17 2010 Thomas E. Dickey
- initial version.
