Name:           ncview
Version:        2.1.7
Release:        5%{?dist}
Summary:        A visual browser for netCDF format files
Group:          Applications/Engineering
License:        GPLv1
URL:            http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Source0:        ftp://cirrus.ucsd.edu/pub/ncview/ncview-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  xorg-x11-proto-devel libXaw-devel libXt-devel libXext-devel
BuildRequires:  libXmu-devel libICE-devel libSM-devel libX11-devel
BuildRequires:  libpng-devel
BuildRequires:  netcdf-mpich-devel netcdf-devel udunits2-devel netpbm-devel
BUildRequires:  expat-devel

Requires: netcdf-mpich

%description
Ncview is a visual browser for netCDF format files.  Typically you
would use ncview to get a quick and easy, push-button look at your
netCDF files.  You can view simple movies of the data, view along
various dimensions, take a look at the actual data values, change
color maps, invert the data, etc.

%prep
%setup -q


%build
%configure \
 --with-nc-config=/usr/bin/nc-config \
 --with-ppm_incdir=%{_includedir}/netpbm \
 --with-udunits2_incdir=%{_includedir}/udunits2 \
 --x-libraries=%{_libdir} --datadir=%{_datadir}/ncview 

#  WARNING!
#  The parallel build was tested and it does NOT work.
#  make %{?_smp_mflags}
make
sed s=NCVIEW_LIB_DIR=%{_datadir}/ncview= < data/ncview.1.sed > data/ncview.1


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults
cp -p Ncview-appdefaults ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults/Ncview
%makeinstall NCVIEW_LIB_DIR=${RPM_BUILD_ROOT}%{_datadir}/ncview BINDIR=${RPM_BUILD_ROOT}%{_bindir} MANDIR=${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir ${RPM_BUILD_ROOT}%{_datadir}/ncview/
install -m0644 -p *.ncmap ${RPM_BUILD_ROOT}%{_datadir}/ncview/
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/X11/app-defaults/Ncview
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
install -m0644 -p data/ncview.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/*
%{_datadir}/ncview/
%{_datadir}/X11/app-defaults/Ncview
%{_mandir}/man1/*


%changelog
* Mon Aug 20 2018 Ketan Patel <patelkr@ornl.gov> - 2.1.7-2
- Updating to 2.1.7
- Updating all required libraries

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Orion Poplawski <orion@cora.nwra.com> - 2.1.2-1
- Update to 2.1.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.1.1-2
- Rebuild for new libpng

* Wed Aug 3 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-1
- Update to 2.1.1
- Drop cflags patch fixed upstream
- Add BR libpng-devel

* Thu Apr 14 2011 Orion Poplawski <orion@cora.nwra.com> - 2.0-0.2.beta4
- Add patch to use RPM_OPT_FLAGS (bug #696739)

* Wed Apr 6 2011 Orion Poplawski <orion@cora.nwra.com> - 2.0-0.1.beta4
- Update to 2.0beta4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.93c-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.93c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.93c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Adam Jackson <ajax@redhat.com> 1.93c-4
- Drop Requires: xorg-x11-server-Xorg.

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.93c-3
- fix patch to apply with fuzz=0

* Thu Apr 10 2008 Patrice Dumas <pertusus@free.fr> - 1.93c-2
- update to 1.93c

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.92e-13
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 1.92e-12
- add BR: netcdf-static

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 1.92e-11
- rebuild for BuildID

* Tue Nov 14 2006 Ed Hill <ed@eh3.com> - 1.92e-10
- more cleanups for check-buildroot

* Tue Nov 14 2006 Ed Hill <ed@eh3.com> - 1.92e-9
- bz 215632

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 1.92e-8
- rebuild for imminent FC-6 release

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 1.92e-7
- rebuild for new gcc

* Sun Nov 20 2005 Ed Hill <ed@eh3.com> - 1.92e-6
- update for the new modular xorg-x11

* Wed Aug  3 2005 Ed Hill <ed@eh3.com> - 1.92e-5
- fix dist tag

* Wed Jul  6 2005 Ed Hill <ed@eh3.com> - 1.92e-4
- mkstemp() security fix and more cleanups

* Wed Jul  6 2005 Ed Hill <ed@eh3.com> - 1.92e-3
- move the data files to %%{_datadir} and add COPYING
- added xorg-x11 Requires and BuildRequires

* Tue Jul  5 2005 Ed Hill <ed@eh3.com> - 1.92e-2
- fix permissions, remove fortran dependency, and small cleanups

* Tue Jul  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 1.92e-1
- Fedora Extras cleanups

* Sun Dec  5 2004 Ed Hill <eh3@mit.edu> - 0:1.92e-0.fdr.0
- Initial version

