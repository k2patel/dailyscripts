#
# spec file for package cdo
#

Name:           cdo
#BuildRequires:  
Version:        1.9.4
Release:        1
Summary:        Climate Data Operators
License:        GNU GENERAL PUBLIC LICENSE Version 2, June 1991
Group:          Productivity/Graphics/Visualization/Other
Requires:       netcdf
Autoreqprov:    on
URL:            https://code.zmaw.de/projects/cdo
Patch0:		cdo-module.patch
Source0:        cdo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  netcdf-devel
BuildRequires:  hdf5-devel
BuildRequires:  szip-devel
BuildRequires:  grib_api-devel
BuildRequires:  proj-devel
BuildRequires:  fftw-devel

Requires: netcdf >= 4.3.3.1
Requires: hdf5 >= 1.8.15.1

%description
CDO is a collection of command line Operators to manipulate and analyse Climate model Data.
Supported data formats are GRIB, netCDF, SERVICE, EXTRA and IEG. There are more than 400
operators available. The following table provides a brief overview of the main categories.


Authors:
--------
    This program was developed at the Max-Planck-Institute for Meteorology.
    Uwe Schulzweida, <uwe.schulzweida AT mpimet.mpg.de>, is the main author.
    Ralf Mueller, <ralf.mueller AT mpimet.mpg.de>
    Luis Kornblueh, <luis.kornblueh AT mpimet.mpg.de>
    Cedrick Ansorge, <cedrick.ansorge AT mpimet.mpg.de>
    Ralf Quast, <ralf.quast AT brockmann-consult.de>
    Send questions, comments and bug reports to <https://code.zmaw.de/projects/cdo>


%prep
%setup
%patch0 -p1 -b .module


%build
./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu --program-prefix= --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --includedir=%{_builddir}/usr/lib64 --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/usr/com --mandir=/usr/share/man --infodir=/usr/share/info --prefix=%{_prefix} --with-netcdf --with-szlib --with-hdf5 --with-grib_api --with-proj --with-udunits2 --with-curl --with-libxml2 --with-fftw3
make 

%install
make DESTDIR=$RPM_BUILD_ROOT install 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS OPERATORS README doc/cdo.pdf doc/cdo_refcard.pdf
%{_prefix}/bin/cdo
#%{_prefix}/bin/cdotest

%changelog -n cdo
* Fri Aug 10 2018 Ketan Patel <patelkr@ornl.gov> - 1.9.4-1
- Updating to 1.9.4

* Fri Jan 02 2015 - patelkr@ornl.gov
- Building with all dep.
* Mon Aug 25 2008 - petri@pik-potsdam.de
- adapted to cdo-1.2.0
* Tue May 20 2008 - petri@pik-potsdam.de
- adapted to cdo-1.1.1
- dont try to include cdotest in the package
* Fri Jan 05 2007 - petri@pik-potsdam.de
- Created initial spec file
