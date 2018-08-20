Name:      libgeotiff
Version:   1.4.2
Release:   1%{?dist}
Summary:   GeoTIFF format library
Group:     System Environment/Libraries
License:   MIT
URL:       http://trac.osgeo.org/geotiff/
Source:    http://download.osgeo.org/geotiff/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtiff-devel libjpeg-devel proj-devel zlib-devel

%description
GeoTIFF represents an effort by over 160 different remote sensing, 
GIS, cartographic, and surveying related companies and organizations 
to establish a TIFF based interchange format for georeferenced 
raster imagery.

%package devel
Summary: Development library and header for the GeoTIFF file format library
Group: Development/Libraries
Requires: pkgconfig libtiff-devel
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

%prep
%setup -q -n %{name}-%{version}

# fix wrongly encoded files from tarball
set +x
for f in `find . -type f` ; do
   if file $f | grep -q ISO-8859 ; then
      set -x
      iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
         mv -f ${f}.tmp $f
      set +x
   fi
   if file $f | grep -q CRLF ; then
      set -x
      sed -i -e 's|\r||g' $f
      set +x
   fi
done
set -x


%build
%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}/ \
        --with-proj               \
        --with-jpeg               \
        --with-zip                \
        --enable-debug            \
        --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -fv %{buildroot}%{_libdir}/lib*.la
echo  >> %{buildroot}%{_datadir}/epsg_csv/codes.csv

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%doc ChangeLog LICENSE README
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_libdir}/%{name}.so.2*
%{_mandir}/man1/listgeo.1.gz
%{_mandir}/man1/applygeo.1.gz
%{_mandir}/man1/geotifcp.1.gz
%dir %{_datadir}/epsg_csv
%{_datadir}/epsg_csv/*.p*
%attr(0644,root,root) %{_datadir}/epsg_csv/*.csv

%files devel
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/*.inc
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Aug 10 2018 Ketan Patel <k2patel@live.com> - 1.4.2-1
- Updating 1.4.2
- Removing makegeo as suggested by Even Rouault / 2016-08-16 # Check ChangeLog
- Fixing man pages

* Thu Oct 29 2015 Volker Fröhlich <volker27@gmx.at> - 1.4.0-6
- Install the real makegeo binary, also solving BZ #1235027
- Re-enable multiple compiler workers
- Actually build with -O2
- Remove outdated prep-section changes
- Remove rpaths

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-4
- Rebuild for Proj 4.9.1

* Wed Jan 07 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-3
- move patching to %%prep section
- explicitly track lib soname so bumps aren't a surprise
- exclude libgeotiff.la file from packaging
- %%configure --disable-static

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0
- Removed patches. No longer applicable.
- Update URL
- Update download URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Volker Fröhlich <volker27@gmx.at> - 1.2.5-14
- Support aarch64 (BZ #925739)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.2.5-11
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.2.5-10
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Volker Fröhlich <volker27@gmx.at> - 1.2.5-8
- Add isa macro
- Harmonize buildroot/RPM_BUILD_ROOT
- Replace install macro, use name macro where suitable
- Improve devel sub-package description
- Remove defattr
- Rebuild for libtiff 4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.2.5-4
- Fix FTBFS: use gcc -shared instead of ld -shared to compile with -fstack-protector

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-2
- disable smp build for koji

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-1
- new bugfix release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-2
- Fix multilib issue by removal of datetime in doxygen footers

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-1
- Rebuild for final release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.4-0.5.rc1
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 1.2.4-0.4.rc1
- Rebuild for RH #249435

* Tue Jul 24 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.3.rc1
- codes are under MIT
- pkg-config cflags return fix
- epsg_csv ownership

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.2.rc1
- fix debuginfo usability
- move header files to the subdirectory
- specify the full URL of the source
- leave *.inc headers included
- libgeotiff-devel should require libtiff-devel
- works to keep timestamps on the header files installed
- docs proper triage

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.1.rc1
- initial pack for fedora
- add pkgconfig file
- add soname versioning patch
