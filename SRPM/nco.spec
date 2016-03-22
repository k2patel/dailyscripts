Name:           nco
Version:        4.5.3
Release:        1%{?dist}
Summary:        Suite of programs for manipulating NetCDF/HDF4 files
Group:          Applications/Engineering
License:        GPLv3
URL:            http://nco.sourceforge.net/

Source0:        http://nco.sourceforge.net/src/nco-%{version}.tar.gz
#Patch0:         nco-4.0.3-install_C_headers.patch
#%if 0%{?rhel} && 0%{?rhel} <= 5
#Patch out variables from in.cdl that earlier versioins of netcdf complain about
#Patch1:         nco-4.0.5-fillvalue.patch
#%endif

BuildRequires:  bison, flex, gawk
BuildRequires:  netcdf-devel
%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires:  libnc-dap-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  antlr-C++
%else
BuildRequires:  antlr
%endif
BuildRequires:  chrpath
BuildRequires:  gsl-devel
BuildRequires:  texinfo
BuildRequires:  udunits2-devel

%package devel
Summary:        Development files for NCO
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%package static
Summary:        Static libraries for NCO
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description
The netCDF Operators, NCO, are a suite of command line programs known
as operators.  The operators facilitate manipulation and analysis of
self-describing data stored in the freely available netCDF and HDF
formats (http://www.unidata.ucar.edu/packages/netcdf and
http://hdf.ncsa.uiuc.edu, respectively).  Each NCO operator (e.g.,
ncks) takes netCDF or HDF input file(s), performs an operation (e.g.,
averaging, hyperslabbing, or renaming), and outputs a processed netCDF
file.  Although most users of netCDF and HDF data are involved in
scientific research, these data formats, and thus NCO, are generic and
are equally useful in fields from agriculture to zoology.  The NCO
User's Guide illustrates NCO use with examples from the field of
climate modeling and analysis.  The NCO homepage is
http://nco.sourceforge.net/.

%description devel
This package contains the NCO header and development files.

%description static
This package contains the NCO static libs.

%prep
%setup -q
#%patch0 -p1 -b .install_C_headers
#%if 0%{?rhel} && 0%{?rhel} <= 5
#%patch1 -p1 -b .fillvalue
#%endif


%build
export CPPFLAGS="-I%{_includedir}/udunits2"
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fpermissive -fPIC"
%configure \
  HAVE_ANTLR=yes \
  --disable-dependency-tracking --includedir=%{_includedir}/nco 
make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT%{_includedir}/nco
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/nco.info \
    %{_infodir}/dir 2>/dev/null || :

%postun
/sbin/ldconfig
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/nco.info \
    %{_infodir}/dir 2>/dev/null || :
fi


%files
%doc doc/README doc/LICENSE doc/rtfm.txt 
%{_bindir}/ncap
%{_bindir}/ncap2
%{_bindir}/ncatted
%{_bindir}/ncbo
%{_bindir}/ncdiff
%{_bindir}/ncea
%{_bindir}/ncecat
%{_bindir}/nces
%{_bindir}/ncflint
%{_bindir}/ncks
%{_bindir}/ncpdq
%{_bindir}/ncra
%{_bindir}/ncrcat
%{_bindir}/ncrename
%{_bindir}/ncwa
%{_mandir}/man1/ncap.1*
%{_mandir}/man1/ncap2.1*
%{_mandir}/man1/ncatted.1*
%{_mandir}/man1/ncbo.1*
%{_mandir}/man1/ncdiff.1*
%{_mandir}/man1/ncea.1*
%{_mandir}/man1/ncecat.1*
%{_mandir}/man1/nces.1*
%{_mandir}/man1/ncflint.1*
%{_mandir}/man1/ncks.1*
%{_mandir}/man1/nco.1*
%{_mandir}/man1/ncpdq.1*
%{_mandir}/man1/ncra.1*
%{_mandir}/man1/ncrcat.1*
%{_mandir}/man1/ncrename.1*
%{_mandir}/man1/ncwa.1*
%{_infodir}/*
%{_libdir}/libnco*[0-9]*.so

%files devel
%{_includedir}/nco/
%{_libdir}/libnco.so
%{_libdir}/libnco_c++.so

%files static
%{_libdir}/libnco*.a


%changelog
* Wed Jul 23 2014 Orion Poplawski <orion@cora.nwra.com> 4.4.4-1
- Update to 4.4.4
- Strip rpaths

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 2 2014 Orion Poplawski <orion@cora.nwra.com> 4.4.3-1
- Update to 4.4.3

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> 4.4.2-1
- Update to 4.4.2

* Wed Jan 29 2014 Orion Poplawski <orion@cora.nwra.com> 4.4.1-1
- Update to 4.4.1

* Thu Dec 19 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.9-1
- Update to 4.3.9
- Fix build with -Werror=format-security

* Tue Oct 22 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.7-2
- No need to build docs
- Drop BR version requirement for netcdf-devel, all up to date

* Fri Oct 18 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.7-1
- Update to 4.3.7

* Mon Sep 30 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.6-1
- Update to 4.3.6

* Wed Sep 25 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.5-1
- Update to 4.3.5

* Thu Aug 1 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.4-1
- Update to 4.3.4

* Sun Jul 28 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.3-1
- Update to 4.3.3

* Tue Jul 9 2013 Orion Poplawski <orion@cora.nwra.com> 4.3.2-1
- Update to 4.3.2

* Sun Mar 31 2013 - Orion Poplawski <orion@cora.nwra.com> - 4.3.0-1
- Update to 4.3.0

* Wed Jan 30 2013 - Orion Poplawski <orion@cora.nwra.com> - 4.2.5-1
- Update to 4.2.5

* Thu Nov 15 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.2.3-1
- Update to 4.2.3

* Mon Oct 29 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.2.2-1
- Update to 4.2.2

* Fri Aug 3 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.2.1-1
- Update to 4.2.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.2.0-1
- Update to 4.2.0

* Tue Apr 3 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.1.0-1
- Update to 4.1.0

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.9-2
- Rebuilt for c++ ABI breakage

* Tue Feb 14 2012 - Orion Poplawski <orion@cora.nwra.com> - 4.0.9-1
- Update to 4.0.9

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.8-2
- Really enable netcdf4 support

* Tue May 17 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.8-1
- Update to 4.0.8
- Rebuild for hdf5 1.8.7

* Wed Apr 6 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.7-1
- Update to 4.0.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 6 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.6-3
- Rebuild with fixed hdf5 for netcdf4 support

* Sat Feb 5 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.6-2
- Fixup more EL5 tests

* Sat Feb 5 2011 - Orion Poplawski <orion@cora.nwra.com> - 4.0.6-1
- Update to 4.0.6
- Really only use libnc-dap for EL5

* Thu Dec 16 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.5-3
- BR antlr-C++ on Fedora 14+

* Mon Dec 13 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.5-2
- Use libnc-dap only for EL5
- Other EL5 fixes

* Fri Dec 10 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.5-1
- Update to 4.0.5

* Fri Oct 1 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.4-1
- Update to 4.0.4

* Tue Sep 7 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.3-1
- Update to 4.0.3
- Rebase install_C_headers patch

* Mon Jun 28 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.2-1
- Update to 4.0.2

* Tue Apr 20 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.1-1
- Update to 4.0.1

* Wed Jan 6 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.0-4
- Enable netcdf4 support

* Wed Jan 6 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.0-3
- Enable udunits2 support - add proper include path

* Wed Jan 6 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.0-2
- Enable udunits2 support
- Updated 4.0.0 tarball

* Wed Jan 6 2010 - Orion Poplawski <orion@cora.nwra.com> - 4.0.0-1
- Update to 4.0.0

* Thu Nov 12 2009 - Orion Poplawski <orion@cora.nwra.com> - 3.9.9-2
- Drop LIBS, linkage fixed in netcdf package

* Wed Nov 11 2009 - Orion Poplawski <orion@cora.nwra.com> - 3.9.9-1
- Update to 3.9.9
- Build against netcdf 4.1.0
- Add needed netcdf libraries to LIBS

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 30 2009 - Orion Poplawski <orion@cora.nwra.com> - 3.9.8-1
- Update to 3.9.8
- Update install headers patch

* Mon Mar 30 2009 - Orion Poplawski <orion@cora.nwra.com> - 3.9.7-2
- Drop include patch fixed in antlr 2.7.7-5

* Wed Mar 25 2009 - Orion Poplawski <orion@cora.nwra.com> - 3.9.7-1
- Update to 3.9.7 - download tarball from nco site
- Add BR on gsl-devel to enable GSL support
- Force antlr detection to override bad configure test
- Rework install_C_headers patch to not require autotool run
- Report include patch upstream

* Fri Mar 06 2009 - Caolán McNamara <caolanm@redhat.com> - 3.9.5-5
- include cstdio for EOF

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 - Patrice Dumas <pertusus@free.fr> - 3.9.5-3
- call libtoolize
- remove unneeded dependencies on curl-devel, libxml2-devel, librx-devel
- ship more documentation

* Thu Sep 11 2008 - Patrice Dumas <pertusus@free.fr> - 3.9.5-2
- rebuild for newer libnc-dap

* Thu Jul 10 2008 - Patrice Dumas <pertusus@free.fr> - 3.9.5-1
- update to 3.9.5

* Sat Mar  1 2008 - Patrice Dumas <pertusus@free.fr> - 3.9.3-1
- update to 3.9.3
- separate static sub-package 

* Mon Aug 27 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.9.1-1
- Update to 3.9.1
- Drop udunits patch no longer needed
- Add BR libnc-dap-devel to enable DAP support
- Add BR antlr
- Add BR gawk

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.1.5-3
- br bison as well

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.1.5-2
- buildrequire flex

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.1.5-1
- new upstream 3.1.5

* Fri Apr 21 2006 Ed Hill <ed@eh3.com> - 3.1.2-1
- update to new upstream 3.1.2

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 3.0.2-2
- rebuild for new gcc

* Mon Sep  5 2005 Ed Hill <ed@eh3.com> - 3.0.2-1
- update to new upstream 3.0.2

* Wed Aug  3 2005 Ed Hill <ed@eh3.com> - 3.0.1-4
- remove (hopefully only temporarily) opendap support

* Thu Jul 21 2005 Ed Hill <ed@eh3.com> - 3.0.1-3
- add LICENSE file

* Sat Jul  9 2005 Ed Hill <ed@eh3.com> - 3.0.1-2
- add BuildRequires: opendap-devel

* Sun Jun 19 2005 Ed Hill <ed@eh3.com> - 3.0.1-1
- update to upstream 3.0.1
- comment & fixes for BuildRequires

* Sat Apr 23 2005 Ed Hill <ed@eh3.com> - 3.0.0-2
- add BuildRequires and fix CXXFLAGS per Tom Callaway
- add udunits patch per Tom Callaway

* Sat Apr 16 2005 Ed Hill <ed@eh3.com> - 3.0.0-1
- update to ver 3.0.0
- devel package fixes per D.M. Kaplan and M. Schwendt
- fix info post/postun

* Sun Dec  5 2004 Ed Hill <eh3@mit.edu> - 0:2.9.9-0.fdr.4
- sync with netcdf-3.6.0beta6-0.fdr.0
- split into devel and non-devel

* Wed Dec  1 2004 Ed Hill <eh3@mit.edu> - 0:2.9.9-0.fdr.3
- sync with netcdf-0:3.5.1-0.fdr.11
- added '-fpermissive' for GCC 3.4.2 warnings
- added "Provides:nco-devel" for the headers and libs

* Mon Oct  4 2004 Ed Hill <eh3@mit.edu> - 0:2.9.9-0.fdr.2
- Add some of Michael Schwendt's suggested INC/LIB path fixes and 
  sync with the netcdf-3.5.1-0.fdr.10 dependency.

* Thu Sep 23 2004 Ed Hill <eh3@mit.edu> - 0:2.9.9-0.fdr.1
- add NETCDF_INC and NETCDF_LIB to work on systems where old
  versions of netcdf may exist in /usr/local

* Wed Sep  8 2004 Ed Hill <eh3@mit.edu> - 0:2.9.9-0.fdr.0
- updated to ver 2.9.9

* Sat Aug  7 2004 Ed Hill <eh3@mit.edu> - 0:2.9.8-0.fdr.0
- updated to ver 2.9.8

* Sat Jul 17 2004 Ed Hill <eh3@mit.edu> - 0:2.9.7-0.fdr.2
- removed unneeded %%ifarch

* Sat Jul 17 2004 Ed Hill <eh3@mit.edu> - 0:2.9.7-0.fdr.1
- Add %%post,%%postun

* Sat Jul 17 2004 Ed Hill <eh3@mit.edu> - 0:2.9.7-0.fdr.0
- Initial working version

