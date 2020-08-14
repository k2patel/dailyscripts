Name:           libkml
Version:        1.3.0
Release:        3%{?dist}
Summary:        Reference implementation of OGC KML 2.2

License:        BSD
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/%{version}/libkml-%{version}.tar.gz

## See https://github.com/libkml/libkml/pull/239
Patch0:         0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:         0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:         0003-Fix-python-tests.patch
Patch3:         0004-Correctly-build-and-run-java-test.patch
# Fix a fragile test failing on i686
Patch4:         fragile_test.patch

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  gtest-devel
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  minizip-devel
BuildRequires:  python2-devel
BuildRequires:  swig
BuildRequires:  uriparser-devel
BuildRequires:  zlib-devel

%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{python2_sitearch}/.*\\.so$


%description
Reference implementation of OGC KML 2.2.
It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.


%package -n python2-%{name}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
The python2-%{name} package contains Python bindings for %{name}.


%package java
Summary:        Java bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description java
The %{name}-java package contains Java bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       expat-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -i 's/find_package(ZLIB 1.2.8)/find_package(ZLIB)/' CMakeLists.txt

%build
%cmake -DWITH_SWIG=ON -DWITH_PYTHON=ON -DWITH_JAVA=ON \
  -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=ON \
  -DJAVA_AWT_LIBRARY=%{_libdir}/jvm/java/include \
  -DJAVA_JVM_LIBRARY=%{_libdir}/jvm/java/lib 
make %{?_smp_mflags}


%install
%make_install


%check
ctest -V


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libkml*.so.*

%files -n python2-%{name}
%{python2_sitearch}/*.so
%{python2_sitearch}/*.py*

%files java
%{_javadir}/LibKML.jar
%{_libdir}/%{name}/

%files devel
%doc examples
%{_includedir}/kml/
%{_libdir}/libkml*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 08 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-2
- Don't call it Google's reference implementation in Summary/Description
- Update Source URL
- Add python_provide macro
- Enable tests

* Thu Mar 31 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

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

* Mon Oct 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-2
- Added >= 1.3.35 for swing

* Sat Aug 09 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-1
- Initial package
