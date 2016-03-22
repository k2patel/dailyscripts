#
# spec file for package parallel-netcdf
#

Name:           parallel-netcdf
Version:        1.5.0
Release:        el7
Summary:        A library providing high-performance I/O with Unidata's NetCDF
License:        GPL-2.0
Group:          Development/Libraries/Parallel
Url:            http://trac.mcs.anl.gov/projects/parallel-netcdf/
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  openmpi-devel
BuildRequires:  mpich-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define _mpi openmpi mpich

%description
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.


%package libpnetcdf1-openmpi
Summary:        A Toolkit for Advanced Optimization
Group:          System/Libraries
Requires:       openmpi-devel

%description libpnetcdf1-openmpi
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.


%package libpnetcdf1-openmpi-devel
Summary:        A Toolkit for Advanced Optimization
Group:          System/Libraries
Requires:       openmpi-devel

%description libpnetcdf1-openmpi-devel
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.


%package  libpnetcdf1-mpich
Summary:        A Toolkit for Advanced Optimization
Group:          System/Libraries
Requires:       mpich-devel

%description  libpnetcdf1-mpich
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.

%package libpnetcdf1-mpich-devel
Summary:        A Toolkit for Advanced Optimization
Group:          System/Libraries
Requires:       mpich-devel

%description libpnetcdf1-mpich-devel
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.


%prep
%setup -q -n %{name}-%{version}

set -- *
for mpi in %_mpi; do
 mkdir $mpi
 cp -ap "$@" $mpi
done

%build
for mpi in %_mpi; do
cd $mpi
%configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu \
--prefix=/usr/$mpi \
--libdir=/usr/lib64/$mpi \
--with-mpi=/usr/lib64/$mpi/ --enable-mpi-io-test --enable-fortran --enable-strict --build=x86_64-redhat-linux-gnu \
--host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu \
MPICC=/usr/lib64/$mpi/bin/mpicc MPICXX=/usr/lib64/$mpi/bin/mpicxx \
LDFLAGS="-L/usr/lib64/$mpi/lib/" \
LD_LIBRARY_PATH="/usr/lib64/$mpi/lib/ /usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/" \
CPPFLAGS="-I/usr/include/$mpi-x86_64" 

make

mkdir shared
cd shared
%{_libdir}/$mpi/bin/mpif77 -shared -Wl,-soname=libpnetcdf.so.1 -o ../libpnetcdf.so.%{version}
cd ..

cd ..
done

%install
for mpi in %_mpi; do
cd $mpi
%make_install

%ifarch x86_64
mkdir -p %{buildroot}/$mpi/%{_lib}
mkdir %{buildroot}/$mpi/bin
mkdir %{buildroot}/$mpi/include
mv %{buildroot}/usr/lib/* %{buildroot}/$mpi/%{_lib}/
mv %{buildroot}/usr/bin/* %{buildroot}/$mpi/bin/
mv %{buildroot}/usr/include/* %{buildroot}/$mpi/include/
%endif

install -m 755 libpnetcdf.so.%{version} %{buildroot}/$mpi/%{_lib}
pushd %{buildroot}/$mpi/%{_lib}
ln -s libpnetcdf.so.%{version} libpnetcdf.so.1
ln -s libpnetcdf.so.%{version} libpnetcdf.so
popd

install -m 755 libpnetcdf.a %{buildroot}/$mpi/%{_lib}


find %{buildroot} -name '*.la' -exec rm {} \;
cd ..
done

%clean
rm -rf %{buildroot}

%post libpnetcdf1-openmpi -p /sbin/ldconfig

%postun libpnetcdf1-openmpi -p /sbin/ldconfig

%files libpnetcdf1-openmpi
%defattr(-,root,root,-)
%dir %{buildroot}/openmpi/usr/man
%dir %{buildroot}/openmpi/usr/man/man1
%dir %{buildroot}/openmpi/usr/man/man3
%{buildroot}/openmpi/bin/*
%{buildroot}/openmpi/man/man1/*
%{buildroot}/openmpi/man/man3/*
%{buildroot}/openmpi/%_lib/*.so.*

%files libpnetcdf1-openmpi-devel
%defattr(-,root,root,-)
%{_libdir}/openmpi/include/*
%{_libdir}/openmpi/%_lib/*.so
%{_libdir}/openmpi/%_lib/*.a

%files libpnetcdf1-mpich
%defattr(-,root,root,-)
%defattr(-,root,root,-)
%dir %{buildroot}/usr/man
%dir %{buildroot}/usr/man/man1
%dir %{buildroot}/usr/man/man3
%{buildroot}/bin/*
%{buildroot}/man/man1/*
%{buildroot}/man/man3/*
%{_libdir}/mpich/%_lib/*.so.*

%files libpnetcdf1-mpich-devel
%defattr(-,root,root,-)
%{_libdir}/mpich/include/*
%{_libdir}/mpich/%_lib/*.so
%{_libdir}/mpich/%_lib/*.a

%changelog
* Sun Aug 26 2012 scorot@free.fr
- fix shared library file name
* Sun Aug 26 2012 scorot@free.fr
- fix broken requirement of devel packages
* Mon Aug 20 2012 scorot@free.fr
- again fix wrong Group flag
* Mon Aug 20 2012 scorot@free.fr
- fix wrong Group flag
* Fri Aug 10 2012 scorot@free.fr
- fix libdir name after %%%%makeinstall for x86_64 arch
* Thu Aug  9 2012 scorot@free.fr
- first package
