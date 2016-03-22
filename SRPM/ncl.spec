Name:           ncl
Version:        6.3.0
Release:        6%{?dist}
Summary:        NCAR Command Language and NCAR Graphics

Group:          Applications/Engineering
License:        BSD
URL:            http://www.ncl.ucar.edu
Source0:        https://www.earthsystemgrid.org/download/fileDownload.htm?logicalFileId=bec58cb3-cd9b-11e4-bb80-00c0f03d5b7c#/ncl_ncarg-%{version}.tar.gz
Source1:        Site.local.ncl
Source2:        ncarg.csh
Source3:        ncarg.sh

# ymake uses cpp with some defines on the command line to generate a 
# Makefile which consists in:
#  Template: command line defines
#  Site.conf
#  LINUX
#  Site.conf
#  Template: generic defaults, including default paths
#  Project
#  Rules
#  yMakefile
#  Template: some rules
#
# install paths are set up in Project. Paths used in code are also in 
# Project, in NGENV_DESCRIPT.
Patch0:         ncl-5.1.0-paths.patch
Patch1:         ncarg-4.4.1-deps.patch
Patch2:         ncl-5.1.0-ppc64.patch
# Add needed -lm to ictrans build, remove unneeded -lrx -lidn -ldl from ncl
Patch3:         ncl-libs.patch
# Fix build without EOS
Patch4:         ncl-eos.patch
# don't have the installation target depends on the build target since
# for library it implies running ranlib and modifying the library timestamp
Patch10:        ncl-5.0.0-no_install_dep.patch
# put install and build rules before script rules such that the default rule
# is all
Patch11:        ncl-5.0.0-build_n_scripts.patch
Patch12:        ncl-5.1.0-netcdff.patch
Patch13:        ncl-5.1.0-includes.patch
# Add Fedora secondary arches
Patch16:        ncl-5.2.1-secondary.patch

BuildRequires:  /bin/csh, gcc-gfortran
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  netcdf-devel
%else
BuildRequires:  netcdf-devel
%endif
BuildRequires:  atlas-devel
BuildRequires:  cairo-devel
BuildRequires:  hdf-static, hdf-devel >= 4.2r2
BuildRequires:  g2clib-static
BuildRequires:  gdal-devel
BuildRequires:  libjpeg-devel
BuildRequires:  proj-devel
# imake needed for makedepend
BuildRequires:  imake, libXt-devel, libXaw-devel, libXext-devel, libXpm-devel
BuildRequires:  byacc, flex
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  flex-static
%endif
BuildRequires:  udunits2-devel
Requires:       %{name}-common = %{version}-%{release}
Requires:       udunits2

Provides:       ncarg = %{version}-%{release}
Obsoletes:      ncarg < %{version}-%{release}


%description
NCAR Command Language (NCL) is an interpreted language designed specifically
for scientific data processing and visualization.  Portable, robust, and free,
NCL supports netCDF3/4, GRIB1/2, HDF-SDS, HDF4-EOS, binary, shapefiles, and
ASCII files.  Numerous analysis functions are built-in.  High quality graphics
are easily created and customized with hundreds of graphic resources.  Many
example scripts and their corresponding graphics are available.


%package common
Summary:        Common files for NCL and NCAR Graphics
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif

%description common
%{summary}.


%package devel
Summary:        Development files for NCL and NCAR Graphics
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libXext-devel
Provides:       ncl-static = %{version}-%{release}
Provides:       ncarg-devel = %{version}-%{release}
Obsoletes:      ncarg-devel < %{version}-%{release}

%description devel
%{summary}.


%package examples
Summary:        Example programs and data using NCL
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif

%description examples
Example programs and data using NCL.


%prep
%setup -q -n ncl_ncarg-%{version}
%patch0 -p1 -b .paths
%patch1 -p1 -b .deps
%patch2 -p1 -b .ppc64
%patch3 -p1 -b .libs
%patch4 -p1 -b .eos
%patch10 -p1 -b .no_install_dep
%patch11 -p1 -b .build_n_scripts
%patch12 -p1 -b .netcdff
%patch13 -p1 -b .includes
%patch16 -p1 -b .secondary

# Build against atlas
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%global atlasblaslib -ltatlas
%global atlaslapacklib -ltatlas
%else
%global atlasblaslib -lcblas -lf77blas -lptf77blas
%global atlaslapacklib -llapack -latlas
%endif
sed -ri -e 's,-lblas_ncl,%{atlasblaslib},' \
        -e 's,-llapack_ncl,%{atlaslapacklib},' \
        -e 's,-L\$\((BLAS|LAPACK)SRC\),-L%{_libdir}/atlas,' config/Project
#Spurrious exec permissions
find -name '*.[fh]' -exec chmod -x {} +

#Use ppc config if needed
%ifarch ppc ppc64
cp config/LINUX.ppc32.GNU config/LINUX
%endif

#Fixup LINUX config (to expose vsnprintf prototype)
sed -i -e '/StdDefines/s/-DSYSV/-D_ISOC99_SOURCE/' config/LINUX

rm -rf external/blas external/lapack

# fix the install directories
sed -e 's;@prefix@;%{_prefix};' \
 -e 's;@mandir@;%{_mandir};' \
 -e 's;@datadir@;%{_datadir};' \
 -e 's;@libdir@;%{_libdir};' \
 %{SOURCE1} > config/Site.local

#Setup the profile scripts
cp %{SOURCE2} %{SOURCE3} .
sed -i -e s,@LIB@,%{_lib},g ncarg.csh ncarg.sh

sed -i -e 's;load "\$NCARG_ROOT/lib/ncarg/nclex\([^ ;]*\);loadscript(ncargpath("nclex") + "\1);' \
    -e 's;"\$NCARG_ROOT/lib/ncarg/\(data\|database\);ncargpath("\1") + ";' \
    -e 's;\$NCARG_ROOT/lib/ncarg/nclscripts;$NCARG_ROOT/share/ncarg/nclscripts;' \
    `find ni/src -name \*.ncl`


%build
# short-cicuit:
./config/ymkmf

# ./config/ymkmf could be also short circuited, since it does:
# (cd ./config; make -f Makefile.ini clean all)
# ./config/ymake -config ./config -Curdir . -Topdir .

#make Build CCOPTIONS="$RPM_OPT_FLAGS -fPIC -Werror-implicit-function-declaration" F77=gfortran F77_LD=gfortran\

make Build CCOPTIONS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing -fopenmp" F77=gfortran F77_LD=gfortran\
 CTOFLIBS="-lgfortran" FCOPTIONS="$RPM_OPT_FLAGS -fPIC -fno-second-underscore -fno-range-check -fopenmp" \
 COPT= FOPT=


%install
export NCARG=`pwd`
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 0644 ncarg.csh ncarg.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
# database, fontcaps, and graphcaps are arch dependent
mv $RPM_BUILD_ROOT%{_datadir}/ncarg/{database,{font,graph}caps} \
   $RPM_BUILD_ROOT%{_libdir}/ncarg/
# Compat links for what is left
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/ncarg
for x in $RPM_BUILD_ROOT%{_datadir}/ncarg/*
do
  ln -s ../../share/ncarg/$(basename $x) $RPM_BUILD_ROOT%{_prefix}/lib/ncarg/
done
# Use system udunits
rm -r $RPM_BUILD_ROOT%{_datadir}/ncarg/udunits
ln -s ../udunits $RPM_BUILD_ROOT%{_datadir}/ncarg/
# Don't conflict with allegro-devel (generic API names)
for manpage in $RPM_BUILD_ROOT%{_mandir}/man3/*
do
   manname=`basename $manpage`
   mv $manpage $RPM_BUILD_ROOT%{_mandir}/man3/%{name}_$manname
done



%files
%doc COPYING Copyright README
%config(noreplace) %{_sysconfdir}/profile.d/ncarg.*sh
%{_bindir}/ConvertMapData
%{_bindir}/WriteLineFile
%{_bindir}/WriteNameFile
%{_bindir}/WritePlotcharData
%{_bindir}/cgm2ncgm
%{_bindir}/ctlib
%{_bindir}/ctrans
%{_bindir}/ezmapdemo
%{_bindir}/fcaps
%{_bindir}/findg
%{_bindir}/fontc
%{_bindir}/gcaps
%{_bindir}/graphc
%{_bindir}/ictrans
%{_bindir}/idt
%{_bindir}/med
%{_bindir}/ncargfile
%{_bindir}/ncargpath
%{_bindir}/ncargrun
%{_bindir}/ncargversion
%{_bindir}/ncargworld
%{_bindir}/ncarlogo2ps
%{_bindir}/ncarvversion
%{_bindir}/ncgm2cgm
%{_bindir}/ncgmstat
%{_bindir}/ncl
%{_bindir}/ncl_convert2nc
%{_bindir}/ncl_filedump
%{_bindir}/ncl_grib2nc
%{_bindir}/nnalg
%{_bindir}/pre2ncgm
%{_bindir}/pre2ncgm.prog
%{_bindir}/psblack
%{_bindir}/psplit
%{_bindir}/pswhite
%{_bindir}/pwritxnt
%{_bindir}/ras2ccir601
%{_bindir}/rascat
%{_bindir}/rasgetpal
%{_bindir}/rasls
%{_bindir}/rassplit
%{_bindir}/rasstat
%{_bindir}/rasview
%{_bindir}/tdpackdemo
%{_bindir}/tgks0a
%{_bindir}/tlocal
%{_libdir}/ncarg/database/
%{_libdir}/ncarg/fontcaps/
%{_libdir}/ncarg/graphcaps/

%files common
%dir %{_datadir}/ncarg
%{_datadir}/ncarg/colormaps/
%{_datadir}/ncarg/data/
%{_datadir}/ncarg/grib2_codetables/
%{_datadir}/ncarg/grib2_codetables.previous/
%{_datadir}/ncarg/nclscripts/
%{_datadir}/ncarg/ngwww/
%{_datadir}/ncarg/sysresfile
%{_datadir}/ncarg/udunits
%{_datadir}/ncarg/xapp/
%dir %{_prefix}/lib/ncarg
%{_prefix}/lib/ncarg/colormaps
%{_prefix}/lib/ncarg/data
%{_prefix}/lib/ncarg/grib2_codetables
%{_prefix}/lib/ncarg/grib2_codetables.previous
%{_prefix}/lib/ncarg/nclscripts
%{_prefix}/lib/ncarg/ngwww
%{_prefix}/lib/ncarg/sysresfile
%{_prefix}/lib/ncarg/udunits
%{_prefix}/lib/ncarg/xapp
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz
%{_bindir}/scrip_check_input

%files devel
%{_bindir}/MakeNcl
%{_bindir}/WRAPIT
%{_bindir}/ncargcc
%{_bindir}/ncargf77
%{_bindir}/ncargf90
%{_bindir}/nhlcc
%{_bindir}/nhlf77
%{_bindir}/nhlf90
%{_bindir}/wrapit77
%{_includedir}/ncarg/
%dir %{_libdir}/ncarg
%{_libdir}/ncarg/libcgm.a
%{_libdir}/ncarg/libfftpack5_dp.a
%{_libdir}/ncarg/libhlu.a
%{_libdir}/ncarg/libncarg.a
%{_libdir}/ncarg/libncarg_c.a
%{_libdir}/ncarg/libncarg_gks.a
%{_libdir}/ncarg/libncarg_ras.a
%{_libdir}/ncarg/libncl.a
%{_libdir}/ncarg/libnclapi.a
%{_libdir}/ncarg/libngmath.a
%{_libdir}/ncarg/libnfp.a
%{_libdir}/ncarg/libnfpfort.a
%{_libdir}/ncarg/libnio.a
%{_libdir}/ncarg/libsphere3.1_dp.a
%{_libdir}/ncarg/ncarg/
%{_mandir}/man3/*.gz

%files examples
%{_bindir}/ncargex
%{_bindir}/ng4ex
%{_datadir}/ncarg/examples/
%{_datadir}/ncarg/hluex/
%{_datadir}/ncarg/nclex/
%{_datadir}/ncarg/resfiles/
%{_datadir}/ncarg/tests/
%{_datadir}/ncarg/tutorial/
%{_prefix}/lib/ncarg/examples
%{_prefix}/lib/ncarg/hluex
%{_prefix}/lib/ncarg/nclex
%{_prefix}/lib/ncarg/resfiles
%{_prefix}/lib/ncarg/tests
%{_prefix}/lib/ncarg/tutorial


%changelog
* Sun Sep 13 2015 Peter Robinson <pbrobinson@fedoraproject.org> 6.3.0-6
- Fix FTBFS on aarch64

* Mon Jul 27 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-5
- Rebuild for gdal 2.0.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-3
- Rebuild for hdf5 1.8.15

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.3.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 19 2015 Orion Poplawski - 6.3.0-1
- Update to 6.3.0

* Thu Jan 08 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.1-2
- Rebuild for hdf5 1.8.14

* Fri Sep 5 2014 Orion Poplawski - 6.2.1-1
- Update to 6.2.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 4 2014 Orion Poplawski - 6.2.0-1
- Update to 6.2.0
- Compile with -fopenmp

* Fri Jan 31 2014 Orion Poplawski - 6.1.2-6
- Fix build with -Werror=format-security (bug #1037211)

* Sun Sep 22 2013 Orion Poplawski - 6.1.2-5
- Rebuild for atlas 3.10

* Tue Aug 27 2013 Orion Poplawski - 6.1.2-4
- Rebuild for gdal 1.10.0

* Wed Jul 31 2013 Orion Poplawski <orion@cora.nwra.com> - 6.1.2-3
- Build for arm

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 6.1.2-2
- Rebuild for hdf5 1.8.11

* Thu Feb 7 2013 Orion Poplawski <orion@cora.nwra.com> - 6.1.2-1
- Update to 6.1.2

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 6.1.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-1
- Update to 6.1.0
- Drop xwd patch applied upstream

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-6
- Don't link against librx, was causing memory corruption
- Compile with -fno-strict-aliasing for now

* Fri Jul 13 2012 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-5
- Add patch to fix xwd driver on 64-bit (bug 839707)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 6.0.0-3
- Rebuild for new libpng

* Thu Sep 29 2011 - Orion Poplawski <orion@cora.nwra.com> - 6.0.0-2
- Use system udunits by linking it into where ncl expects it, drop
  udunits patch.  Fixes bug 742307.

* Thu Sep 1 2011 - Orion Poplawski <orion@cora.nwra.com> - 6.0.0-1
- Update to 6.0.0 final

* Wed May 18 2011 - Orion Poplawski <orion@cora.nwra.com> - 6.0.0-0.2.beta
- Rebuild for hdf5 1.8.7

* Thu Mar 31 2011 - Orion Poplawski <orion@cora.nwra.com> - 6.0.0-0.1.beta
- Update to 6.0.0-beta
- Enable cairo and gdal support

* Fri Feb 18 2011 - Orion Poplawski <orion@cora.nwra.com> - 5.2.1-6
- Rebuild for new g2clib - fix grib handling on 64-bit machines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.1-5
- No flex-static in EL

* Mon Nov 22 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.1-4
- Add BR flex-static

* Mon Nov 22 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.1-3
- Add compatibility links to /usr/lib/ncarg

* Mon Sep 6 2010 - Dan Horák <dan[at]danny.cz> - 5.2.1-2
- Recognize Fedora secondary architectures

* Tue Aug 10 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.1-1
- Update to 5.2.1
- Update udunits patch

* Thu Jul 1 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.0-2
- Drop BR libnc-dap and update lib patch to remove unneeded libraries

* Wed Apr 28 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.2.0-1
- Update to 5.2.0
- Update libs patch
- Fixup profile script packaging

* Tue Feb 16 2010 - Orion Poplawski <orion@cora.nwra.com> - 5.1.1-6
- Add patch to fix FTBFS bug #564856

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.1-5
- Same as below with hdf-static
- Explicitly BR g2clib-static in accordance with the Packaging
  Guidelines (g2clib-devel is still static-only).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.1-2
- Rebuild for libdap 3.9.3

* Mon Jul 13 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.1-1
- Update to 5.1.1

* Tue Jul 7 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.0-4
- Fixup more paths in shipped ncl scripts (bug #505240)

* Tue May 26 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.0-3
- Move database back to main arch dependent package
 
* Tue May 19 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.0-2
- Set NCARG_NCARG to /usr/share/ncarg
- Move fontcaps and graphcaps back to main arch dependent package

* Thu Mar 5 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.1.0-1
- Update to 5.1.0
- Rebase ppc64, netcdff patch
- Drop triangle, flex, hdf, png, wrapit, uint32 patch upstreamed

* Tue Feb 24 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-19
- Rebuild for gcc 4.4.0 and other changes
- Move data files into noarch sub-package
- Make examples sub-package noarch

* Mon Feb 2 2009 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-18
- Fix unowned directory (bug #483468)

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 5.0.0-17
- Rebuild for atlas-3.8.2

* Fri Dec 12 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-16
- Re-add profile.d startup scripts to set NCARG env variables

* Mon Dec 8 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-15
- Try changing the udunits path in config/Project

* Thu Dec 4 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-14
- Actually apply udunits patch

* Thu Nov 27 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-13
- Enable udunits support add use system udunits.dat

* Thu Sep 11 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-12
- Rebuild for new libdap
- Fix netcdf include location

* Fri Apr 11 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-11
- Add patch to fix raster image problems on non 32-bit platforms
- Add more includes to includes patch

* Thu Mar 27 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-10
- Add patch to fixup some missing includes
- Define _ISOC99_SOURCE to expose vsnprintf prototype
- Update hdf patch to remove hdf/netcdf.h include

* Mon Feb 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-9
- Rename Site.local to Site.local.ncl
- Add comment for imake BR

* Wed Feb  6 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-8
- Move examples into separate sub-package

* Fri Feb  1 2008 - Patrice Dumas <pertusus@free.fr> - 5.0.0-7
- put noarch files in datadir
- avoid compilation in %%install

* Mon Jan 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-6
- Make BR hdf-devel >= 4.2r2.

* Fri Dec 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-5
- Fixup wrapit flex compilation

* Fri Dec 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-4
- Actually get ncl to build

* Sun Nov 18 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-3
- Move robj to -devel
- Provide ncl-static in ncl-devel
- Turn on BuildUdunits.  Turn off BuildV5D.
- Drop config/LINUX patch, use sed

* Wed Nov 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-2
- Fixup profile.d script permissions, Group, move aed.a to devel

* Tue Nov  6 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-1
- Initial ncl package, based on ncarg
