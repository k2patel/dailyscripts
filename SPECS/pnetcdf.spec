%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Patch version?
%global snaprel %{nil}

# mpi names
%global mpich mpich-3.2
%global openmpi openmpi3

# NOTE:  Try not to release new versions to released versions of Fedora
# You need to recompile all users of HDF5 for each version change
Name: pnetcdf
Version: 1.12.1
Release: 1%{?dist}
Summary: Parallel netCDF: A High Performance API for NetCDF File Access
License: Open source
Group: File tools
Url: http://cucis.ece.northwestern.edu/projects/PNETCDF/index.html
Packager: Ketan Patel <patelkr@ornl.gov>

Source0: https://parallel-netcdf.github.io/Release/pnetcdf-%{version}.tar.gz

BuildRequires: flex gcc-gfortran
BuildRequires: ghostscript texlive-latex

%global with_mpich 1
%global with_openmpi 1
%if 0%{?rhel} <= 6
%ifarch ppc64
% No mpich2 on ppc64 in EL6
%global with_mpich 0
%endif
%endif
%ifarch s390 s390x
# No openmpi on s390(x)
%global with_openmpi 0
%endif

%if %{with_mpich}
%global mpi_list %{mpich}
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} %{openmpi}
%endif

%description
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

%if %{with_mpich}
%package -n lib%name-mpich
Summary: Shared library of Parallel netCDF
Group: System/Libraries

%description -n lib%name-mpich
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains shared library of Parallel netCDF.

%package -n lib%name-mpich-devel
Summary: Development files of Parallel netCDF
Group: Development/Other
Requires: lib%name-mpich = %version-%release
Requires: %{mpich}-devel

%description -n lib%name-mpich-devel
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development files of Parallel netCDF.

%package -n lib%name-mpich-devel-doc
Summary: Documentation and examples for Parallel netCDF
Group: Development/Documentation

%description -n lib%name-mpich-devel-doc
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development documentation and examples for
Parallel netCDF.

%package -n lib%name-mpich-debug
Summary: Debug package for Parallel netCDF
Group: Debug
Requires: lib%name-mpich-devel-doc
Requires: lib%name-mpich-devel

%description -n lib%name-mpich-debug
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains debug information for Parallel netCDF.
%endif

%if %{with_openmpi}
%package -n lib%name-openmpi
Summary: Shared library of Parallel netCDF
Group: System/Libraries

%description -n lib%name-openmpi
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains shared library of Parallel netCDF.

%package -n lib%name-openmpi-devel
Summary: Development files of Parallel netCDF
Group: Development/Other
Requires: lib%name-openmpi = %version-%release
Requires: %{openmpi}-devel

%description -n lib%name-openmpi-devel
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development files of Parallel netCDF.

%package -n lib%name-openmpi-devel-doc
Summary: Documentation and examples for Parallel netCDF
Group: Development/Documentation

%description -n lib%name-openmpi-devel-doc
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains development documentation and examples for
Parallel netCDF.

%package -n lib%name-openmpi-debug
Summary: Debug package for Parallel netCDF
Group: Debug
Requires: lib%name-openmpi-devel-doc
Requires: lib%name-openmpi-devel

%description -n lib%name-openmpi-debug
Parallel netCDF (PnetCDF) is a library providing high-performance I/O
while still maintaining file-format compatibility with Unidata's NetCDF.

NetCDF gives scientific programmers a space-efficient and portable means
for storing data. However, it does so in a serial manner, making it
difficult to achieve high I/O performance. By making some small changes
to the API specified by NetCDF, we can use MPI-IO and its collective
operations.

This package contains debug information for Parallel netCDF.
%endif


%prep
%setup -q
rm -fR autom4te.cache


%build
#Do out of tree builds
%global _configure ../configure
#Common configure options
%global configure_opts \\\
  --enable-mpi-io-test \\\
  --enable-fortran \\\
  --enable-strict \\\
  --enable-shared \\\
%{nil}

#MPI builds
export CC=mpicc
export CXX=mpicxx
export F9X=mpif90
# Work around a bug in mpich when hostname is not resovable
export RUNPARALLEL="mpiexec -np 4 -host localhost"
for mpi in %{mpi_list}
do
  mkdir $mpi
  pushd $mpi
  module load mpi/$mpi-%{_arch}
  ln -s ../configure .
  %configure \
    %{configure_opts} \
    --with-mpi=%{_libdir}/$mpi \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man \
    LDFLAGS="-L/usr/lib64/$mpi/lib/ -L/usr/lib64/$mpi/lib/" LD_LIBRARY_PATH="/usr/lib64/$mpi/lib/ /usr/lib/gcc/x86_64-redhat-linux/4.8.2/32/"
  make %{?_smp_mflags}
  module purge
  popd
done


%install
for mpi in %{mpi_list}
do
  %ifarch x86_64
  LIB_SUFFIX=64
  %endif
  module load mpi/$mpi-%{_arch}
  make -C $mpi install DESTDIR=${RPM_BUILD_ROOT}
  rm $RPM_BUILD_ROOT/%{_libdir}/$mpi/lib/*.la
  module purge
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with_mpich}
%files -n lib%name-mpich
%{_libdir}/%{mpich}/bin/*
%{_libdir}/%{mpich}/share/man/man1/*
%{_libdir}/%{mpich}/lib/*.a
%{_libdir}/%{mpich}/lib/*.so*

%files -n lib%name-mpich-devel
%{_includedir}/%{mpich}-%{_arch}
%{_libdir}/%{mpich}/share/man/man3/*

%files -n lib%name-mpich-debug
/usr/lib/debug/usr/lib64/%{mpich}/bin/*

%files -n lib%name-mpich-devel-doc
%{_libdir}/%{mpich}/lib/pkgconfig/*.pc
%endif

%if %{with_openmpi}
%files -n lib%name-openmpi
%{_libdir}/%{openmpi}/bin/*
%{_libdir}/%{openmpi}/share/man/man1/*
%{_libdir}/%{openmpi}/lib/*.a
%{_libdir}/%{openmpi}/lib/*.so*

%files -n lib%name-openmpi-devel
%{_includedir}/%{openmpi}-%{_arch}
%{_libdir}/%{openmpi}/share/man/man3/*

%files -n lib%name-openmpi-debug
/usr/lib/debug/usr/lib64/%{openmpi}/bin/*

%files -n lib%name-openmpi-devel-doc
%{_libdir}/%{openmpi}/lib/pkgconfig/*.pc
%endif


%changelog
* Thu Jul 30 2020 Ketan Patel <k2patel@live.com> 1.12.1-1
- Saperated mpich and openmpi package
- Using mpich-3.2 and openmpi3
- Package name change

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
