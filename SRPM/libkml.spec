%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           libkml
Version:        1.3.0
Release:        99_1.erma%{?dist}
Summary:        A KML library written in C++ with bindings to other languagues

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/%{name}/
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        libkml.conf
#Patch0:         libkml-third_party_removal.diff
#Patch1:         libkml-0.6.1.configure_ac.patch
#Patch2:         libkml-fix-gcc-warning.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# requires swig >= 1.3.35
BuildRequires:  cppunit, swig >= 1.3.35
BuildRequires:  libcurl-devel, expat-devel, python-devel, chrpath
BuildRequires:  minizip-devel, zlib-devel,  boost-devel
BuildRequires:  autoconf, libtool
Requires:       python

%description
Libkml is an implementation of the OGC KML 2.2 standard. is written in
C++ and bindings are available via SWIG to other languages. It can be
used in applications that want to parse, generate and operate on KML.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
#rm -rf third_party
#%patch0 -p0 -b .third_party
#%patch1 -p1 -b .configure_ac
#%patch2 -p1 -b .fixwarning

%build
autoreconf -fi
%configure --disable-static \
           --disable-java
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# remove compiled examples
cd examples; make clean;cd ..

# remove x permssion from examples folder files
find examples -type f -print | xargs chmod a-x

# move libs to kml (for keeping third party libs away)
mkdir -p $RPM_BUILD_ROOT%{_libdir}/libkml/
mv $RPM_BUILD_ROOT%{_libdir}/*.so* $RPM_BUILD_ROOT%{_libdir}/libkml/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/


#removing rpaths with chrpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmlengine_swig_python.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmlengine.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libkml/libkmldom_swig_python.so.0.0.0
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmlengine.so
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmldom.so
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_kmlbase.so

# remove .libs and .deps directories
find . -name '.libs'  -type d -print | xargs rm -rf
find . -name '.deps'  -type d -print | xargs rm -rf

# fix unstripping-binary-or-object warning
chmod a+x $RPM_BUILD_ROOT%{python_sitearch}/_kmlengine.so
chmod a+x $RPM_BUILD_ROOT%{python_sitearch}/_kmldom.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%doc AUTHORS
%doc README
%doc ChangeLog
%dir %{_libdir}/libkml
%{_libdir}/libkml/*.so.*
%{python_sitearch}/*.so
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%{_sysconfdir}/ld.so.conf.d/libkml.conf

%files devel
%defattr(-,root,root,-)
%doc examples
%{_includedir}/*
%dir %{_libdir}/libkml
%{_libdir}/libkml/*.so

%changelog
* Mon Jul 07 2014 Thomas J. Baker <tjb@unh.edu> - 1.3.0-1
- rebuilt latest version for ERMA

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.1-7
- Fix gcc warning that lead to failure due to -Werror flag

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-4
- Included *pyc and pyo files in %%files and added BuildRequires libgcj-devel.

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-3
- libkml-0.6.1.configure_ac.patch patch for swig > 1.3.35

* Sat Mar 07 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-2
- updated to 0.6.1
- libkml-third_party_removal.diff Removes third part dependency
- (provided by Peter Lemenkov)

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-1
- Updated to 0.6.1

* Mon Oct 05 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-2
- Added >= 1.3.35 for swing

* Sat Aug 09 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-1
- Initial package
