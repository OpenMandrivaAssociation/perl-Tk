%define	modname	Tk
%define	modver	804.029

Name:		perl-%{modname}
Version:	%{perl_convert_version %{modver}}
Release:	13

Summary:	Tk modules for Perl
License:	GPL+ or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{modname}
Source0:	http://www.cpan.org/modules/by-module/Tk/%{modname}-%{modver}.tar.gz
# modified version of http://ftp.de.debian.org/debian/pool/main/p/perl-tk/perl-tk_804.027-8.diff.gz
Patch1:		perl-Tk-debian.patch
# fix segfaults as in #235666 because of broken cashing code
Patch2:		perl-Tk-seg.patch
Patch3:		Tk-804.029-xlib.patch

BuildRequires:	perl-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(fontconfig)
Provides:	perl(Tk::TextReindex)
Provides:	perl(Tk::LabRadio)
Provides:	perl-Tie-Watch

%package	devel
Summary:	Tk modules for Perl (development package)
Group:		Development/C
Requires:	perl-Tk = %{version}-%{release}

%package	doc
Summary:	Tk modules for Perl (documentation package)
Group:		Development/Perl
Requires:	perl-Tk = %{version}-%{release}

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
%setup -q -n %{modname}-%{modver}
chmod -x pod/Popup.pod Tixish/lib/Tk/balArrow.xbm
# debian patch
%patch1 -p1
# patch to fix #235666 ... seems like caching code is broken
%patch2 -p0
%patch3 -p0

find . -type f | xargs perl -pi -e 's|^#!.*/bin/perl\S*|#!/usr/bin/perl|'
# Make it lib64 aware, avoid patch
perl -pi -e "s,(/usr/X11(R6|\\*)|\\\$X11|\(\?:)/lib,\1/%{_lib},g" \
  myConfig pTk/mTk/{unix,tixUnix/{itcl2.0,tk4.0}}/configure
#(peroyvind) --center does no longer seem to be working, obsoleted by -c
perl -pi -e "s#--center#-c#" ./Tk/MMutil.pm

%build
perl Makefile.PL INSTALLDIRS=vendor XFT=1
%make OPTIMIZE="%{optflags}" LD_RUN_PATH=""

%install
%makeinstall_std
chmod 644 %{buildroot}%{_mandir}/man3*/*

# Remove unpackaged files, add them if you find a use
# Tie::Watch is packaged separately
rm %{buildroot}%{perl_vendorarch}/Tk/prolog.ps
rm %{buildroot}%{_mandir}/man1/{ptk{ed,sh},widget}.1*

## compress all .pm files (as using perl-PerlIO-gzip).
#find %{buildroot} -name "*.pm" | xargs gzip -9

%files
%doc COPYING ToDo Changes README README.linux
%{_bindir}/*
%{_mandir}/man*/*
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


%changelog
* Fri Dec 21 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 804.29.0-11
- rebuild for perl-5.16.2
- cleanups

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 804.29.0-9mdv2012.0
+ Revision: 765793
- rebuilt for perl-5.14.2

* Sat Jan 21 2012 Oden Eriksson <oeriksson@mandriva.com> 804.29.0-8
+ Revision: 764298
- rebuilt for perl-5.14.x

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 804.29.0-7
+ Revision: 702789
- rebuilt against libpng-1.5.x

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 804.29.0-6
+ Revision: 667403
- mass rebuild

* Sat Jan 01 2011 Funda Wang <fwang@mandriva.org> 804.29.0-5mdv2011.0
+ Revision: 626994
- fix build with latest xlib

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 804.29.0-4mdv2011.0
+ Revision: 564587
- rebuild for perl 5.12.1

* Tue Jul 20 2010 Sandro Cazzaniga <kharec@mandriva.org> 804.29.0-3mdv2011.0
+ Revision: 555296
- rebuild

* Wed Jul 14 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 804.29.0-2mdv2011.0
+ Revision: 553268
- tie::watch no longer distributed in its own dist - using & shipping the one embedded in tk dist

* Tue Jul 13 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 804.29.0-1mdv2011.0
+ Revision: 552709
- update to 804.029

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 804.28.0-15mdv2010.1
+ Revision: 488794
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 804.28.0-14mdv2010.0
+ Revision: 416663
- rebuilt against libjpeg v7

* Fri Jul 24 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 804.28.0-13mdv2010.0
+ Revision: 399401
- update seg patch from fedora: our (old) version was preventing menus to
  appear.
  see https://bugzilla.redhat.com/show_bug.cgi?id=431330

* Sun Jun 21 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 804.28.0-12mdv2010.0
+ Revision: 387686
- fix bug 40359: removing broken patch that prevents 'widget' demo from working
- using %%perl_convert_version
- fix license tag

* Sun May 10 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 804.028-11mdv2010.0
+ Revision: 373948
- fix #50751

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 804.028-10mdv2009.1
+ Revision: 366103
- fix str fmt

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 804.028-9mdv2009.0
+ Revision: 224581
- rebuild

* Wed Mar 19 2008 Oden Eriksson <oeriksson@mandriva.com> 804.028-8mdv2008.1
+ Revision: 188810
- fix #38879 (fixes CVE-2006-4484, CVE-2007-6697)

* Sun Feb 03 2008 David Walluck <walluck@mandriva.org> 804.028-7mdv2008.1
+ Revision: 161620
- fix perl-Tk Requires
- add BuildRequires on jpeg-devel and png-devel
- add patches from Fedora
- rebuild

  + Nicolas LÃ©cureuil <nlecureuil@mandriva.com>
    - Rebuild for new perl

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 804.028-1mdv2008.1
+ Revision: 133606
- update to new version 804.028

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Tue Nov 06 2007 Guillaume Rousse <guillomovitch@mandriva.org> 804.027-8mdv2008.1
+ Revision: 106542
-enable XFT support (jq)
-spec cleanup
-original sources format


* Thu Jun 22 2006 Michael Scherer <misc@mandriva.org> 804.027-7mdv2007.0
- add a Obsoletes on perl-Tk-PNG as it is now included in the source

* Sun Jun 18 2006 Stefan van der Eijk <stefan@eijk.nu> 804.027-6
- rebuild for png
- %%mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 804.027-5mdk
- Rebuild

* Wed Feb 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 804.027-4mdk
- Require Tie::Watch

* Mon Nov 15 2004 Götz Waschk <waschk@linux-mandrake.com> 804.027-3mdk
- rebuild for new perl

* Thu May 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 804.027-2mdk
- Remove the manpage for Tie::Watch (which is packaged separately)

* Thu Apr 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 804.027-1mdk
- 804.027

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 800.024-4mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- fix no longer working --center option to pod2man

