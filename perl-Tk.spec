%define	module	Tk
%define	name	perl-%{module}
%define	version	804.027
%define release	%mkrel 8

Summary:	Tk modules for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/Perl
License:	GPL or Artistic
URL:            http://search.cpan.org/dist/%{module}
Source:         http://www.cpan.org/modules/by-module/Tk/%{module}-%{version}.tar.gz
Provides:	perl(Tk::TextReindex)
Provides:	perl(Tk::LabRadio)
# to remove on upgrade ( misc)
Obsoletes:  perl-Tk-PNG
BuildRequires:	perl-devel
BuildRequires:	pwlib-devel
BuildRequires:	X11-devel
BuildRequires:	libxft-devel
BuildRequires:	libxrender-devel
Buildroot:	%{_tmppath}/%{name}-%{version}

%package	devel
Summary:	Tk modules for Perl (development package)
Group:		Development/C
Requires:	perl-Tk = %{version}

%package	doc
Summary:	Tk modules for Perl (documentation package)
Group:		Development/Perl
Requires:	perl-Tk = %{version}

%description
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

%description	devel
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

This is the development package.

%description	doc
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

This is the documentation package.

%prep
%setup -q -n %{module}-%{version}
find . -type f | xargs perl -pi -e 's|^#!.*/bin/perl\S*|#!/usr/bin/perl|'
# Make it lib64 aware, avoid patch
perl -pi -e "s,(/usr/X11(R6|\\*)|\\\$X11|\(\?:)/lib,\1/%{_lib},g" \
  myConfig pTk/mTk/{unix,tixUnix/{itcl2.0,tk4.0}}/configure
#(peroyvind) --center does no longer seem to be working, obsoleted by -c
perl -pi -e "s#--center#-c#" ./Tk/MMutil.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor XFT=1
%make OPTIMIZE="$RPM_OPT_FLAGS" LD_RUN_PATH=""

%install
rm -rf %{buildroot}
%makeinstall_std
%{__chmod} 644 %{buildroot}%{_mandir}/man3*/*

# Remove unpackaged files, add them if you find a use
# Tie::Watch is packaged separately
rm -f %{buildroot}%{perl_vendorarch}/{Tie/Watch.pm,Tk/prolog.ps}
rm -f %{buildroot}%{_mandir}/man1/{ptk{ed,sh},widget}.1*
rm -f %{buildroot}%{_mandir}/man3/Tie::Watch.3pm*

## compress all .pm files (as using perl-PerlIO-gzip).
#find %{buildroot} -name "*.pm" | xargs gzip -9

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ToDo Changes README README.linux
%{_bindir}/*
%{_mandir}/man*/*
%{perl_vendorarch}/Tk.pm*
%dir %{perl_vendorarch}/Tk
%{perl_vendorarch}/Tk/*.pm*
%{perl_vendorarch}/Tk/*.pl
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
%{perl_vendorarch}/fix_4_os2.pl

%files devel
%defattr(-,root,root)
%doc COPYING Funcs.doc INSTALL
%{perl_vendorarch}/Tk/pTk
%{perl_vendorarch}/Tk/*.def
%{perl_vendorarch}/Tk/*.h
%{perl_vendorarch}/Tk/*.m
%{perl_vendorarch}/Tk/*.t
%{perl_vendorarch}/Tk/typemap

%files doc
%defattr(-,root,root)
%doc COPYING
%{perl_vendorarch}/Tk.pod
%{perl_vendorarch}/Tk/*.pod
%{perl_vendorarch}/Tk/README.Adjust


