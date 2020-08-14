Name:		proj
Version:	5.2.0
Release:	1%{?dist}
Summary:	Cartographic projection software (PROJ.4)

License:	MIT
URL:		https://proj4.org
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:	http://download.osgeo.org/%{name}/%{name}-datumgrid-1.8.zip
Patch0:		%{name}-4.8.0-removeinclude.patch

BuildRequires:	libtool


%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.


%package devel
Summary:	Development files for PROJ.4
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.


%package static
Summary:	Development files for PROJ.4
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains libproj static library.


%package nad
Summary:	US and Canadian datum shift grids for PROJ.4
Requires:	%{name} = %{version}-%{release}

%description nad
This package contains additional US and Canadian datum shift grids.


%package epsg
Summary:	EPSG dataset for PROJ.4
Requires:	%{name} = %{version}-%{release}

%description epsg
This package contains additional EPSG dataset.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

# Prepare nad
cd nad
unzip -o %{SOURCE1}
cd ..
# fix shebag header of scripts
for script in `find nad/ -type f -perm -a+x`; do
sed -i -e '1,1s|:|#!/bin/bash|' $script
done

%build
%configure --without-jni
# fix version info to respect new ABI
sed -i -e 's|5\:4\:5|6\:4\:6|' src/Makefile*

%configure
make OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -p -m 0644 nad/pj_out27.dist nad/pj_out83.dist nad/td_out.dist %{buildroot}%{_datadir}/%{name}
%{__install} -p -m 0755 nad/test27 nad/test83 nad/testvarious %{buildroot}%{_datadir}/%{name}
%{__install} -p -m 0644 nad/epsg %{buildroot}%{_datadir}/%{name}

# Install projects.h manually, per #830496:
%{__install} -p -m 0644 src/projects.h %{buildroot}%{_includedir}/

%check
pushd nad
# set test enviroment for porj
export PROJ_LIB=%{buildroot}%{_datadir}/%{name}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH%{buildroot}%{_libdir}
# run tests for proj
./test27      %{buildroot}%{_bindir}/%{name} || exit 0
./test83      %{buildroot}%{_bindir}/%{name} || exit 0
./testIGNF    %{buildroot}%{_bindir}/%{name} || exit 0
./testntv2    %{buildroot}%{_bindir}/%{name} || exit 0
./testvarious %{buildroot}%{_bindir}/%{name} || exit 0
popd

%ldconfig_scriptlets

%files
%doc NEWS AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/libproj.so.13*

%files devel
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_libdir}/libproj.so
%attr(0755,root,root) %{_libdir}/pkgconfig/%{name}.pc
%exclude %{_libdir}/libproj.a
%exclude %{_libdir}/libproj.la

%files static
%{_libdir}/libproj.a
%{_libdir}/libproj.la


%files nad
%doc nad/README
%attr(0755,root,root) %{_datadir}/%{name}/test27
%attr(0755,root,root) %{_datadir}/%{name}/test83
%attr(0755,root,root) %{_datadir}/%{name}/testvarious
%attr(0755,root,root) %{_libdir}/pkgconfig/%{name}.pc
%exclude %{_datadir}/%{name}/epsg
%{_datadir}/%{name}

%files epsg
%doc nad/README
%attr(0644,root,root) %{_datadir}/%{name}/epsg

%changelog
* Mon Feb 04 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-1
- Update to 5.2.0
- Update to new datumgrid (1.8)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Devrim Gündüz <devrim@gunduz.org> 4.9.3-1
- Update to 4.9.3
- Update to new datumgrid (1.6)
- Fix rpmlint warnings
- Cosmetic cleanup  in spec file.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Devrim Gündüz <devrim@gunduz.org> 4.9.2-1
- Update to 4.9.2, per bz # 1294604
- Update URLs.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-2
- track soname so bumps are not a suprise
- -devel: include .pc file here (left copy in -nad too)
- -static: Requires: -devel

* Wed Mar 11 2015 Devrim Gündüz <devrim@gunduz.org> 4.9.1-1
- Update to 4.9.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Devrim Gündüz <devrim@gunduz.org> 4.8.0-3
- Install projects.h manually, per #830496.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Devrim Gündüz <devrim@gunduz.org> 4.8.0-1
- Update to 4.8.0, per bz #814851

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 18 2010 Balint Cristian <cristian.balint@gmail.com> - 4.7.0-3
- fix for bz#562671

* Thu Mar 18 2010 Balint Cristian <cristian.balint@gmail.com> - 4.7.0-2
- fix for bz#556091

* Fri Dec 4 2009 Devrim Gündüz <devrim@gunduz.org> 4.7.0-1
- Update to 4.7.0
- Update to new datumgrid (1.5)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 05 2008 Balint Cristian <rezso@rdsor.ro> - 4.6.1-1
- new stable upstream
- new nad datumgrids
- drop debian license patch
- change homepage URLs

* Sun Apr 20 2008 Balint Cristian <rezso@rdsor.ro> - 4.6.0-1
- new branch

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> - 4.5.0-4
- BuildRequire: libtool

* Thu Mar 27 2008 Balint Cristian <rezso@rdsor.ro> - 4.5.0-3
- enable EPSG dataset to be packed GRASS really needs it
- no more license issue over epsg dataset, proj didnt altered
  EPSG dataset in any way, so its fully EPSG license compliant
- add support for tests during buildtime
- disable hardcoded r-path from libs
- fix shebag for nad scripts

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.5.0-2
- Autorebuild for GCC 4.3

* Tue Jan   2 2007 Shawn McCann <mccann0011@hotmail.com> - 4.5.0-1
- Updated to proj-4.5.0 and datumgrid-1.3

* Sat Sep  16 2006 Shawn McCann <mccann0011@hotmail.com> - 4.4.9-4
- Rebuild for Fedora Extras 6

* Sat Mar  4 2006 Shawn McCann <mccann0011@hotmail.com> - 4.4.9-3
- Rebuild for Fedora Extras 5

* Sat Mar  4 2006 Shawn McCann <mccann0011@hotmail.com> - 4.4.9-2
- Rebuild for Fedora Extras 5

* Thu Jul  7 2005 Shawn McCann <mccann0011@hotmail.com> - 4.4.9-1
- Updated to proj-4.4.9 and to fix bugzilla reports 150013 and 161726. Patch2 can be removed once this package is upgraded to the next release of the source.

* Sun May 22 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 4.4.8-6
- rebuilt

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 4.4.8-5
- rebuilt

* Wed Dec 29 2004 David Kaplan <dmk@erizo.ucdavis.edu> - 0:4.4.8-4
- Added testvarious to nad distribution

* Wed Dec 29 2004 David Kaplan <dmk@erizo.ucdavis.edu> - 0:4.4.8-0.fdr.3
- Added patch for test scripts so that they will work in installed rpm

* Wed Dec 29 2004 David Kaplan <dmk@erizo.ucdavis.edu> - 0:4.4.8-0.fdr.2
- Fixed permissions on nad27 and nad83
- Included test27 and test83 in the nad rpm and made them executable

* Fri Aug 13 2004 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:4.4.8-0.fdr.1
- Updated to version 4.4.8 of library.
- Changed license file so that it agrees with Debian version.
- Updated web addresses of packages.

* Wed Aug 11 2004 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:4.4.7-0.fdr.3
- Removed the "Requires(post,postun)"

* Tue Dec 30 2003 David M. Kaplan <dmk@erizo.ucdavis.edu> 0:4.4.7-0.fdr.2
- proj-nad now owns %%{_datadir}/%%{name}

* Wed Oct 29 2003 Steve Arnold <sarnold@arnolds.dhs.org>
- Basically re-wrote previous spec file from scratch so as
- to comply with both Fedora and RedHat 9 packaging guidelines.
- Split files into proj, proj-devel, and proj-nad (additional grids)
- and adjusted the EXE path in the test scripts.
