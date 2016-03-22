%if 0%{?fedora}
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%global srcname distribute
# Get hash for release from https://github.com/Unidata/netcdf4-python/releases
%global commit 26cdeda69a3ff2efe438020390a876234a23550a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           netcdf4-python
Version:        1.1.0
Release:        1%{?dist}
Summary:        Python/numpy interface to netCDF

Group:          Development/Languages
License:        MIT
URL:            https://github.com/Unidata/netcdf4-python
Source0:        https://github.com/Unidata/netcdf4-python/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# No rpath for library
# http://code.google.com/p/netcdf4-python/issues/detail?id=138
Patch0:         netcdf4-python-norpath.patch
# Don't link against hdf5 and z libraries
# http://code.google.com/p/netcdf4-python/issues/detail?id=139
Patch1:         netcdf4-python-libs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  Cython
BuildRequires:  python-dateutil
# EL6 has python 2.6 and needs ordereddict
%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
%endif
BuildRequires:  numpy
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-dateutil
BuildRequires:  python3-numpy
# For 2to3
BuildRequires:  python-tools
%endif # if with_python3
BuildRequires:  netcdf-devel

# EL6 has python 2.6 and needs ordereddict
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:       python-ordereddict
%endif
Requires:       Cython
Requires:       numpy

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$ 
%endif # if with_python3
%filter_setup
}

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


%if 0%{?with_python3}
%package -n netcdf4-python3
Summary:        Python/numpy interface to netCDF
Group:          Development/Languages
Requires:       python3-Cython
Requires:       python3-numpy

%description -n netcdf4-python3
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
%endif # with_python3


%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1 -b .norpath
%patch1 -p1 -b .libs

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_bindir}/*
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

 
%check
cd test
PYTHONPATH=$(echo ../build/lib.*) python run_all.py
%if 0%{?with_python3}
cd %{py3dir}/test
PYTHONPATH=$(echo ../build/lib.*) python3 run_all.py
%endif


%files
%doc Changelog COPYING docs examples README.md
%{_bindir}/nc3tonc4
%{_bindir}/nc4tonc3
%{_bindir}/ncinfo
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n netcdf4-python3
%doc Changelog COPYING docs examples README.md
%{python3_sitearch}/*
%endif # with_python3


%changelog
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
