%define	modname	Tk
%undefine _debugsource_packages

Summary:	Tk modules for Perl

Name:		perl-%{modname}
Version:	804.036
Release:	12
License:	GPLv2+ or Artistic
Group:		Development/Perl
Url:		https://metacpan.org/pod/Tk
Source0:	http://www.cpan.org/modules/by-module/%{modname}/%{modname}-%{version}.tar.gz
Patch0:	perl-Tk-widget.patch
# modified version of http://ftp.de.debian.org/debian/pool/main/p/perl-tk/perl-tk_804.027-8.diff.gz
Patch1:	perl-Tk-debian.patch
# fix segfaults as in #235666 because of broken cashing code
Patch2:	perl-Tk-seg.patch
Patch3:		perl-Tk-compile.patch
Patch4:	91.patch

# From Fedora rawhide - perl 5.38+ / clang 16
Patch11: perl-Tk-Fix-STRLEN-vs-int-pointer-confusion-in-Tcl_GetByteAr.patch
Patch13: perl-Tk-pregcomp2.c-Avoid-using-incompatible-pointer-type.patch
Patch14: perl-Tk-Avoid-using-incompatible-pointer-type-for-old_warn.patch
Patch15: perl-Tk-Fix-incompatible-pointer-type-in-function-GetTextIndex.patch

BuildRequires:	make
BuildRequires:	perl(open)
BuildRequires:	perl-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(fontconfig)
Provides:	perl(Tk::TextReindex)
Provides:	perl(Tk::LabRadio)
Provides:	perl-Tie-Watch

%description
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

%package	devel
Summary:	Tk modules for Perl (development package)

Group:		Development/C
Requires:	perl-Tk = %{version}-%{release}

%description	devel
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

This is the development package.

%package	doc
Summary:	Tk modules for Perl (documentation package)

Group:		Development/Perl
Requires:	perl-Tk = %{version}-%{release}

%description	doc
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

This is the documentation package.

%prep
%setup -q -n %{modname}-%{version}
# widget patch paths are demos/widget (needs -p0)
%patch -P0 -p0 -b .widget
%patch -P1 -p1 -b .debian -F2
%patch -P2 -p1 -b .seg -F2
%patch -P3 -p1 -b .compile -F2
%patch -P4 -p1 -b .pr91 -F2
%patch -P11 -p1 -b .strlen -F2
%patch -P13 -p1 -b .pregcomp -F2
%patch -P14 -p1 -b .oldwarn -F2
%patch -P15 -p1 -b .gettext -F2

chmod -x pod/Popup.pod Tixish/lib/Tk/balArrow.xbm

find . -type f | xargs sed -i -e 's|^#!.*/bin/perl[[:space:]]+|#!/usr/bin/perl |;s|^#!.*/bin/perl$|#!/usr/bin/perl|'
# Make it lib64 aware, avoid patch
for f in myConfig pTk/mTk/unix/configure \
         pTk/mTk/tixUnix/itcl2.0/configure pTk/mTk/tixUnix/tk4.0/configure; do
  [ -f "$f" ] || continue
  perl -pi -e "s,(/usr/X11(R6|\\*)|\\\$X11|\\(\\?:)/lib,\\1/%{_lib},g" "$f"
done
#(peroyvind) --center does no longer seem to be working, obsoleted by -c
perl -pi -e "s#--center#-c#" ./Tk/MMutil.pm

%build
# Allow residual pointer-sign noise if any remain after patches
export CFLAGS="${CFLAGS:-} -Wno-error=incompatible-pointer-types -Wno-error=int-conversion"
export CXXFLAGS="${CXXFLAGS:-} -Wno-error=incompatible-pointer-types"
%{__perl} Makefile.PL INSTALLDIRS=vendor X11LIB=%{_libdir} XFT=1
find . -name Makefile | xargs %{__perl} -pi -e 's/^\tLD_RUN_PATH=[^\s]+\s*/\t/'
%make_build

%install
%make_install
chmod 644 %{buildroot}%{_mandir}/man3*/*

# Remove unpackaged files, add them if you find a use
# Tie::Watch is packaged separately
rm -f %{buildroot}%{perl_vendorarch}/Tk/prolog.ps
rm -f %{buildroot}%{_mandir}/man1/{ptk{ed,sh},widget}.1*

## compress all .pm files (as using perl-PerlIO-gzip).
#find %{buildroot} -name "*.pm" | xargs gzip -9

%files
%doc COPYING ToDo Changes README README.linux
%{_bindir}/*
%{perl_vendorarch}/Tk.pm*
%dir %{perl_vendorarch}/Tk
%{perl_vendorarch}/Tie/Watch.pm
%{perl_vendorarch}/Tk/*.pm*
%{perl_vendorarch}/Tk/*.gif
%{perl_vendorarch}/Tk/*.xbm
%{perl_vendorarch}/Tk/*.xpm
%{perl_vendorarch}/Tk/license.terms
%{perl_vendorarch}/Tk/Credits
%{perl_vendorarch}/Tk/DragDrop
%{perl_vendorarch}/Tk/Event
%{perl_vendorarch}/Tk/Menu
%{perl_vendorarch}/Tk/Text
%{perl_vendorarch}/Tk/demos
%{perl_vendorarch}/auto/Tk
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%doc COPYING Funcs.doc INSTALL
%{perl_vendorarch}/Tk/pTk
%{perl_vendorarch}/Tk/*.def
%{perl_vendorarch}/Tk/*.h
%{perl_vendorarch}/Tk/*.m
%{perl_vendorarch}/Tk/*.t
%{perl_vendorarch}/Tk/typemap

%files doc
%doc COPYING
%{perl_vendorarch}/Tk.pod
%{perl_vendorarch}/Tk/*.pod
%{perl_vendorarch}/Tk/README.Adjust
