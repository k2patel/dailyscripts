Name:           netcdf4-python
Version:        1.5.3
Release:        1%{?dist}
Summary:        Python/numpy interface to netCDF

License:        MIT
URL:            https://github.com/Unidata/netcdf4-python
Source0:        https://github.com/Unidata/netcdf4-python/archive/v%{version}rel/%{name}-%{version}.tar.gz
# No rpath for library
# http://code.google.com/p/netcdf4-python/issues/detail?id=138
# Patch0:         netcdf4-python-norpath.patch
# Don't link against hdf5 and z libraries
# http://code.google.com/p/netcdf4-python/issues/detail?id=139
# Patch1:         netcdf4-python-libs.patch
# setuptool requirement degrade
Patch0:         netcdf4-python-setup.patch

%if ! ( 0%{?fedora} >= 30 || 0%{?rhel} >= 7 )
BuildRequires:  python-devel
BuildRequires:  python-setuptools >= 0.9
# Added in 1.4.0
#BuildRequires:  python-cftime
BuildRequires:  Cython
BuildRequires:  python-dateutil
# EL6 has python 2.6 and needs ordereddict
%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
%endif
BuildRequires:  numpy
%endif
BuildRequires:  python%{python3_version_nodots}-devel
BuildRequires:  python%{python3_version_nodots}-setuptools >= 18
BuildRequires:  python%{python3_version_nodots}-Cython
BuildRequires:  python%{python3_version_nodots}-dateutil
BuildRequires:  python%{python3_version_nodots}-numpy
BuildRequires:  netcdf-devel
# python3 is default in fedora, but not EPEL
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       python%{python3_version_nodots}-netcdf4 = %{version}-%{release}
%else
Requires:       python2-netcdf4 = %{version}-%{release}
%endif

%description
netCDF version 4 has many features not found in earlier versions of the
library and is implemented on top of HDF5. This module can read and write
files in both the new netCDF 4 and the old netCDF 3 format, and can create
files that are readable by HDF5 clients. The API modeled after
Scientific.IO.NetCDF, and should be familiar to users of that module.

Most new features of netCDF 4 are implemented, such as multiple unlimited
dimensions, groups and zlib data compression. All the new numeric data types
(such as 64 bit and unsigned integer types) are implemented. Compound and
variable length (vlen) data types are supported, but the enum and opaque data
types are not. Mixtures of compound and vlen data types (compound types
containing vlens, and vlens containing compound types) are not supported.


%package -n python2-netcdf4
Summary:        Python/numpy interface to netCDF
# EL6 has python 2.6 and needs ordereddict
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:       python-ordereddict
%endif
# Added in 1.4.0
#Requires:       python2-cftime
Requires:       Cython
Requires:       numpy
%{?python_provide:%python_provide python2-netcdf4}
Provides:       netcdf4-python2 = %{version}-%{release}

%description -n python2-netcdf4
netCDF version 4 has many features not found in earlier versions of the
library and is implemented on top of HDF5. This module can read and write
files in both the new netCDF 4 and the old netCDF 3 format, and can create
files that are readable by HDF5 clients. The API modeled after
Scientific.IO.NetCDF, and should be familiar to users of that module.

Most new features of netCDF 4 are implemented, such as multiple unlimited
dimensions, groups and zlib data compression. All the new numeric data types
(such as 64 bit and unsigned integer types) are implemented. Compound and
variable length (vlen) data types are supported, but the enum and opaque data
types are not. Mixtures of compound and vlen data types (compound types
containing vlens, and vlens containing compound types) are not supported.


%package -n python%{python3_version_nodots}-netcdf4
Summary:        Python/numpy interface to netCDF
#Requires:       python%{python3_pkgversion}-cftime
Requires:       python%{python3_version_nodots}-Cython
Requires:       python%{python3_version_nodots}-numpy
%{?python_provide:%python_provide python%{python3_version_nodots}-netcdf4}
Obsoletes:      netcdf4-python%{python3_version_nodots} < 1.2.7-3
Provides:       netcdf4-python%{python3_version_nodots} = %{version}-%{release}

%description -n python%{python3_version_nodots}-netcdf4
netCDF version 4 has many features not found in earlier versions of the
library and is implemented on top of HDF5. This module can read and write
files in both the new netCDF 4 and the old netCDF 3 format, and can create
files that are readable by HDF5 clients. The API modeled after
Scientific.IO.NetCDF, and should be familiar to users of that module.

Most new features of netCDF 4 are implemented, such as multiple unlimited
dimensions, groups and zlib data compression. All the new numeric data types
(such as 64 bit and unsigned integer types) are implemented. Compound and
variable length (vlen) data types are supported, but the enum and opaque data
types are not. Mixtures of compound and vlen data types (compound types
containing vlens, and vlens containing compound types) are not supported.


%prep
%setup -q -n %{name}-%{version}rel
%patch0 -p1 -b .setup
# %patch1 -p1 -b .libs


%build
%if ! ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
%py2_build
%endif

%py3_build


%install
# python3 is default in fedora, but not EPEL7
%if 0%{?fedora} || 0%{?rhel} >= 8
%if ! ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
%py2_install
%endif
%py3_install
%else
%py3_install
%py2_install
%endif

 
%check
cd test
export NO_NET=1
%if ! ( 0%{?fedora} >= 30 || 0%{?rhel} >= 7 )
PYTHONPATH=$(echo ../build/lib.*%{python2_version}) %{__python2} run_all.py
%endif
%ifarch s390x
# FAIL: runTest (tst_compoundvar.VariablesTestCase) -> assert (cmptype4 == dtype4a) # data type should be aligned
PYTHONPATH=$(echo ../build/lib.*%{python3_version}) %{__python3} run_all.py || :
%else
PYTHONPATH=$(echo ../build/lib.*%{python3_version}) %{__python3} run_all.py
%endif


%files
%license COPYING
%{_bindir}/nc3tonc4
%{_bindir}/nc4tonc3
%{_bindir}/ncinfo

%if ! ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
%files -n python2-netcdf4
%license COPYING
%doc Changelog docs examples README.md
%{python2_sitearch}/*
%endif

%files -n python%{python3_version_nodots}-netcdf4
%license COPYING
%doc Changelog docs examples README.md
%{python3_sitearch}/*


%changelog
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Orion Poplawski <orion@nwra.com> - 1.5.3-1
- Update to 1.5.3

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Sep 10 2019 Orion Poplawski <orion@nwra.com> - 1.5.2-1
- Update to 1.5.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.1.2-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May  6 2019 Orion Poplawski <orion@nwra.com> - 1.5.1.2-1
- Update to 1.5.1.2

* Wed May  1 2019 Orion Poplawski <orion@nwra.com> - 1.5.1-1
- Update to 1.5.1

* Tue Apr  2 2019 Orion Poplawski <orion@nwra.com> - 1.5.0.1-1
- Update to 1.5.0.1

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com> - 1.4.3.2-2
- Rebuild for netcdf 4.6.3

* Sat Mar  9 2019 Orion Poplawski <orion@nwra.com> - 1.4.3.2-1
- Update to 1.4.3.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 7 2018 Orion Poplawski <orion@nwra.com> - 1.3.1-1
- Update to 1.3.1
- Drop Python 2 in Fedora (bugz #1634978)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.9-6
- Rebuilt for Python 3.7

* Tue Mar 13 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.9-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.9-1
- Update to 1.2.9

* Tue Mar 7 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2-7-4
- Provide python-netcdf4

* Thu Mar 2 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2-7-3
- Move python libraries into python?- sub-packages
- Make python3 default for Fedora

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 8 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.7-1
- Update to 1.2.7

* Wed Dec 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-2
- Add upstream patch for python 3.6 support

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-1
- Update to 1.2.6

* Tue Nov 29 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.5-1
- Update to 1.2.5
- Enable python 3 for EPEL

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 15 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-1
- Update to 1.2.4
- Add pthon2/3-netcdf4 provides

* Fri Mar 11 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.3-1
- Update to 1.2.3
- Drop numpy patch
- Use %%license

* Sun Feb 7 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.2-1
- Update to 1.2.2
- Modernize spec
- Add upstream patch for numpy support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.6-4
- Rebuild for netcdf 4.4.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.6-1
- Update to 1.1.6

* Sat Feb 21 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.4-1
- Update to 1.1.4

* Sun Dec 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.3-1
- Update to 1.1.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.9-2
- Rebuild for Python 3.4

* Fri May 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.9-1
- Update to 1.0.9
- Remove rpaths
- Add BR python{,3}-dateutil for tests
- Add BR/R on Cython

* Thu Mar 6 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.8-1
- Update to 1.0.8
- Update URL/source to github

* Thu Feb 6 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.7-1
- Update to 1.0.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.0.2-1
- Update to 1.0.2
- Remove bundled ordereddict (Bug #913528), require it on EL6
- Run tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3.fix1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1.0-2.fix1
- Add patch to link only against netcdf

* Thu May 24 2012 Orion Poplawski <orion@cora.nwra.com> - 1.0-1.fix1
- Update to 1.0fix1

* Thu Apr 5 2012 Orion Poplawski <orion@cora.nwra.com> - 0.9.9-1
- Update to 0.9.9

* Thu Sep 8 2011 Orion Poplawski <orion@cora.nwra.com> - 0.9.7-1
- Initial package
