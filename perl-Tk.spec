%define	modname	Tk
%undefine _debugsource_packages

Summary:	Tk modules for Perl

Name:		perl-%{modname}
Version:	804.036
Release:	5
License:	GPLv2+ or Artistic
Group:		Development/Perl
Url:		https://metacpan.org/pod/Tk
Source0:	http://www.cpan.org/modules/by-module/%{modname}/%{modname}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/perl-Tk/raw/rawhide/f/perl-Tk-widget.patch
# modified version of http://ftp.de.debian.org/debian/pool/main/p/perl-tk/perl-tk_804.027-8.diff.gz
Patch1:		https://src.fedoraproject.org/rpms/perl-Tk/blob/rawhide/f/perl-Tk-debian.patch
# fix segfaults as in #235666 because of broken cashing code
Patch2:		https://src.fedoraproject.org/rpms/perl-Tk/raw/rawhide/f/perl-Tk-seg.patch
Patch3:		perl-Tk-compile.patch
Patch4:		https://github.com/eserte/perl-tk/pull/91.patch

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
%autosetup -p1 -n %{modname}-%{version}
chmod -x pod/Popup.pod Tixish/lib/Tk/balArrow.xbm

find . -type f | xargs sed -i -e 's|^#!.*/bin/perl[[:space:]]+|#!/usr/bin/perl |;s|^#!.*/bin/perl$|#!/usr/bin/perl|'
# Make it lib64 aware, avoid patch
perl -pi -e "s,(/usr/X11(R6|\\*)|\\\$X11|\(\?:)/lib,\1/%{_lib},g" \
  myConfig pTk/mTk/{unix,tixUnix/{itcl2.0,tk4.0}}/configure
#(peroyvind) --center does no longer seem to be working, obsoleted by -c
perl -pi -e "s#--center#-c#" ./Tk/MMutil.pm

%build
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
