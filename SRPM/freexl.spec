Name:      freexl
Version:   1.0.5
Release:   1%{?dist}
Summary:   Library to extract data from within an Excel spreadsheet 
Group:     System Environment/Libraries
License:   MPLv1.1 or GPLv2+ or LGPLv2+
URL:       http://www.gaia-gis.it/FreeXL
Source0:   http://www.gaia-gis.it/gaia-sins/%{name}-sources/%{name}-%{version}.tar.gz 
BuildRequires: doxygen

%description
FreeXL is a library to extract valid data
from within an Excel spreadsheet (.xls)

Design goals:
    * simple and lightweight
    * stable, robust and efficient
    * easily and universally portable
    * completely ignore any GUI-related oddity

%package devel
Summary:  Development Libraries for FreeXL
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --enable-gcov=no --disable-static
make %{?_smp_mflags}

# Mailed the author on Dec 5th 2011
# Preserve date of header file
sed -i 's/^INSTALL_HEADER = \$(INSTALL_DATA)/& -p/' headers/Makefile.in

# Generate HTML documentation and clean unused installdox script
doxygen
rm -f html/installdox


%check
make check

# Clean up
pushd examples
  make clean
popd


%install
make install DESTDIR=%{buildroot}

# Delete undesired libtool archives
rm -f %{buildroot}%{_libdir}/lib%{name}.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%doc COPYING AUTHORS README
%{_libdir}/lib%{name}.so.*

%files devel
%doc examples html
%{_includedir}/freexl.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/freexl.pc


%changelog
* Tue Jul 28 2015 Volker Froehlich <volker27@gmx.at> - 1.0.2-2
- Release bump to work around the f23 build being wrongly tagged for f24

* Wed Jul 15 2015 Volker Fröhlich <volker27@gmx.at> 1.0.2-1
- New release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Volker Fröhlich <volker27@gmx.at> 1.0.1-1
- New release

* Fri Mar  6 2015 Volker Fröhlich <volker27@gmx.at> 1.0.0i-1
- New release with security fixes

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0f-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 30 2013 Volker Fröhlich <volker27@gmx.at> 1.0.0f-1
- Drop obsolete patch for aarch64

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  2 2013 Volker Fröhlich <volker27@gmx.at> 1.0.0d-4
- Add patch for aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0d-1
- New upstream bugfix release

* Fri Jan 13 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-3
- Remove coverage tests and BR for lcov (fail in Rawhide)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 08 2012 Volker Fröhlich <volker27@gmx.at> 1.0.0a-1
- Correct versioning scheme to post-release
- Correct Source and setup macro accordingly

* Fri Nov 18 2011 Volker Fröhlich <volker27@gmx.at> 1.0.0-0.1.a
- Move development lib symlink to devel
- Don't build static lib
- Add README
- Build with enable-gcov
- BR lcov and doxygen
- Shorten description and summary
- Use macros in Source tag
- Add check section
- Change version and release
- Correct URL
- Correct to multiple licensing scenario
- Drop defattr
- Add pkgconfig and isa macro to devel's BR
- Use upstream tarball, as file size is different
- Remove EPEL 5 specific elements

* Fri Nov 26 2010 Peter Hopfgartber <peter.hopfgartner@r3-gis.com> 1.0.0a-0.1
- Initial packaging
