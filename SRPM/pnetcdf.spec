%define mpiimpl mpich
%define mpidir %_libdir/%mpiimpl

%define sover 0

Name: pnetcdf
Version: 1.7.0
Release: el7
Summary: Parallel netCDF: A High Performance API for NetCDF File Access
License: Open source
Group: File tools
Url: http://trac.mcs.anl.gov/projects/parallel-netcdf
Packager: Ketan Patel <patelkr@ornl.gov>

Source: %name-%version.tar.gz

BuildRequires: %mpiimpl-devel flex gcc-gfortran
BuildRequires: ghostscript texlive-latex

%description
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

%package -n lib%name
Summary: Shared library of Parallel netCDF
Group: System/Libraries

%description -n lib%name
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains shared library of Parallel netCDF.

%package -n lib%name-devel
Summary: Development files of Parallel netCDF
Group: Development/Other
Requires: lib%name = %version-%release
Requires: %mpiimpl-devel

%description -n lib%name-devel
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development files of Parallel netCDF.

%package -n lib%name-devel-doc
Summary: Documentation and examples for Parallel netCDF
Group: Development/Documentation

%description -n lib%name-devel-doc
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development documentation and examples for
Parallel netCDF.

%package -n lib%name-debug
Summary: Debug package for Parallel netCDF
Group: Debug
Requires: lib%name-devel-doc
Requires: lib%name-devel
Requires: %mpiimpl-debuginfo

%description -n lib%name-debug
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains debug information for Parallel netCDF.

%prep
%setup
rm -fR autom4te.cache

%build
autoreconf -i
%configure \
        --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu \
        --libdir=%{_libdir} \
	--with-mpi=%mpidir \
	--enable-mpi-io-test \
	--enable-fortran \
	--enable-strict

make 

%{_libdir}/openmpi/bin/mpif77 -shared -Wl,-soname=libpnetcdf.so.1 -o libpnetcdf.so.%{version}

%install
%ifarch x86_64
LIB_SUFFIX=64
%endif
make install prefix=%{buildroot}/usr/

mkdir %{buildroot}/usr/share/
mv %{buildroot}/usr/man %{buildroot}/usr/share/ 

%files
%_bindir/*
%_mandir/man1/*

%files -n lib%name
/usr/lib/*.a

%files -n lib%name-devel
%_includedir/*
%_mandir/man3/*

%files -n lib%name-debug
/usr/lib/debug/*
/usr/src/*

%files -n lib%name-devel-doc
%doc doc/*.txt examples
/usr/lib/pkgconfig/*.pc

%changelog
* Wed Jul 09 2014 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.5.0-alt2
- Version 1.5.0

* Mon Jun 09 2014 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.5.0-alt1.pre1
- Version 1.5.0.pre1

* Mon Nov 18 2013 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.4.0-alt1
- Version 1.4.0

* Fri Feb 08 2013 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.3.1-alt1
- Version 1.3.1

* Fri Sep 14 2012 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.3.0-alt1
- Initial build for Sisyphus

