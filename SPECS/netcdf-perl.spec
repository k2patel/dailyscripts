Name:           netcdf-perl
Version:        1.2.4
Release:        20%{?dist}
Summary:        Perl extension module for scientific data access via the netCDF API

Group:          Development/Libraries
License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf-perl/
Source0:        ftp://ftp.unidata.ucar.edu/pub/netcdf-perl/netcdf-perl-%{version}.tar.gz
Source1:        netcdf-4.4
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl-devel, netcdf-devel
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:  perl-NetCDF = %{version}-%{release}


%description
The netCDF Perl package is a perl extension module for scientific data access
via the netCDF API.


%prep
%setup -q
sed -i -e '1s,/usr/local/bin/perl,%{_bindir}/perl,' src/perl/test.pl


%build
cd src
export PERL_MANDIR=%{_mandir}
export CPP_NETCDF=-I%{_includedir}/netcdf
export LD_NETCDF="-lnetcdf"
%configure
cd perl
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd src
# use the top-level Makefile only for manpage installation
make installed_manuals MANDIR=$RPM_BUILD_ROOT%{_mandir}
cd perl
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# install netcdf-2 man page
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man3
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man3


%check
cd src
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc src/COPYRIGHT src/HISTORY src/README src/perl/test.pl
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/NetCDF.pm
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.4*


%changelog
* Sun Aug 02 2020 Ketan Patel <k2patel@live.com> - 1.2.4-20
- Upgrading to new netcdf and other packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.4-19
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.4-18
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.2.4-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.2.4-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.4-9
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.4-8
- Perl 5.14 mass rebuild

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-7
- Rebuild for netcdf 4.1.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.4-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.2.4-4
- rebuild against perl 5.10.1

* Thu Nov 12 2009 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-3
- Rebuild for netcdf 4.1.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-1
- Update to 1.2.4, fixes build issue (bug #511613)

* Wed Feb 25 2009 - Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-8
- Rebuild for new netcdf

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.3-7
- Rebuild for new perl

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-6
- Rebuild for gcc 3.4

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-5
- Update license tag to 
- Rebuild for BuildID

* Mon Jun 04 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-4
- Change perl BR to perl-devel

* Tue May 22 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-3
- Rebuild for new netcdf 3.6.2 with shared libraries

* Tue Nov 14 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-2
- Changed license to NetCDF, will be changed upstream next release
- Add src/perl/test.pl to %%doc
- Added netcdf-2 man page
- Only use top level Makefile for installing man pages

* Mon Nov 13 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.2.3-1
- Initial version
