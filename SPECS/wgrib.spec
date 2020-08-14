Name:           wgrib
Version:        1.8.1.2c
Release:        3%{?dist}
Summary:        Manipulate, inventory and decode GRIB files

Group:          Applications/Engineering
License:        Public Domain
URL:            http://www.cpc.ncep.noaa.gov/products/wesley/wgrib.html
Source0:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/wgrib.c.v%{version}
Source1:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/Changes
Source2:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/NOTICE
Source3:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/double_prec.txt
Source4:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/formats.txt
Source5:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/formats_update.txt
Source6:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/grib2ieee.txt
Source7:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/misc.txt
Source8:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/porting.txt
Source9:        ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/usertables.txt
Source10:       ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/tricks.wgrib
Source11:       ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/land.grb
Source12:       ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/testbin.c
Source13:       ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/testbin.f
Source14:       testbin.out
Patch1:         testbin.c.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
WGRIB is a program to manipulate, inventory and decode GRIB files.


%prep
%setup -q -c -T
cp %SOURCE0 wgrib.c
cp %SOURCE1 .
cp %SOURCE2 .
cp %SOURCE3 .
cp %SOURCE4 .
cp %SOURCE5 .
cp %SOURCE6 .
cp %SOURCE7 .
cp %SOURCE8 .
cp %SOURCE9 .
cp %SOURCE10 .
cp %SOURCE11 .
cp %SOURCE12 .
cp %SOURCE13 .
%patch1 -p0


%build
gcc $RPM_OPT_FLAGS -o wgrib wgrib.c


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 wgrib $RPM_BUILD_ROOT%{_bindir}/


%check
./wgrib land.grb -d 1
gcc $RPM_OPT_FLAGS -o testbin testbin.c -lm
./testbin > testbin.out && diff %SOURCE14 testbin.out


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc Changes *.txt tricks.wgrib testbin.[cf] land.grb
%{_bindir}/wgrib


%changelog
* Fri Nov 15 2013 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.2c-1
- Update to 1.8.1.2c

* Wed Oct 16 2013 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.2b-1
- Update to 1.8.1.2b

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.2a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.2a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.2a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.2a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.2a-1
- Update to 1.8.1.2a

* Thu May 26 2011 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.0h-1
- Update to 1.8.1.0h

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1.0d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 2 2010 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.0d-1
- Update to 1.8.1.0d

* Mon May 17 2010 - Orion Poplawski <orion@cora.nwra.com> - 1.8.1.0b-1
- Update to 1.8.1.0b

* Tue Mar 30 2010 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.13f-1
- Update to 1.8.0.13f

* Wed Feb 24 2010 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.13e-1
- Update to 1.8.0.13e

* Thu Sep 24 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.13d-1
- Update to 1.8.0.13d

* Mon Aug 24 2009 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.13b-1
- Update to 1.8.0.13b

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0.12u-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0.12u-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12u-1
- Update to 1.8.0.12u

* Fri Feb  8 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12q-1
- Update to 1.8.0.12q

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12o-2
- Rebuild for BuildID

* Wed Aug  8 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12o-1
- Update to 1.8.0.12o

* Tue Dec  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12g-2
- Compile testbin with -lm, needed on x86_64

* Fri Nov 17 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12g-1
- Update to 1.8.0.12g
- Ship testbin.c, testbin.f, and lang.grb for local testing

* Thu Nov 16 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12b-2
- Add check

* Wed Nov 15 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.8.0.12b-1
- Initial version
