%global pkgname PDL-Graphics-PLplot

Name:           perl-PDL-Graphics-PLplot
Version:        0.71
Release:        1%{?dist}
Summary:        Object-oriented interface from perl/PDL to the PLPLOT plotting library
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/PDL-Graphics-PLplot/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DH/DHUNT/%{pkgname}-%{version}.tar.gz
# Work around to FTBFS triggered by -Werror=format-security
Patch0:         PDL-Graphics-PLplot-0.67-hardening.patch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(PDL::Core::Dev)
BuildRequires:  plplot-devel
# Run-time:
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(PDL::Core)
BuildRequires:  perl(PDL::Exporter)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(PDL)
BuildRequires:  perl(PDL::Config)
# PDL::IO::Pnm not used
BuildRequires:  perl(PDL::NiceSlice)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Time::Local)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is the PDL interface to the PLplot graphics library. It is designed
to be simple and light weight with a familiar 'perlish' Object Oriented
interface.

The interface consists of two levels.  A low level interface which maps
closely to the PLplot C interface, and a high level, object-oriented
interface which is easier to use.

%prep
%setup -qn %{pkgname}-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="${RPM_OPT_FLAGS}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/PDL
%{perl_vendorarch}/auto/PDL
%{_mandir}/man3/*

%changelog
* Fri Aug 28 2015 Petr Pisar <ppisar@redhat.com> - 0.71-1
- 0.71 bump

* Tue Jul 21 2015 Petr Pisar <ppisar@redhat.com> - 0.67-8
- Specify all dependencies (bug #1245124)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Petr Pisar <ppisar@redhat.com> - 0.67-6
- Support linking to plplot-5.11.0 (bug #1215584)
- Apply a workaround scaling character size in plplot-5.11.0 (bug #1215584)

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.67-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.67-3
- Let package honor ${RPM_OPT_FLAGS}.
- Add PDL-Graphics-PLplot.patch (Fix FTBFS due to -Werror=format-security).
- Minor spec cleanup.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 12 2013 Christopher Meng <rpm@cicku.me> - 0.67-1
- New version with fix for BZ#992701, BZ#949105.

* Wed Oct 2 2013 Orion Poplawski <orion@cora.nwra.com> - 0.62-4
- Rebuild for plplot 5.9.10

* Thu Aug 08 2013 Christopher Meng <rpm@cicku.me> - 0.62-3
- SPEC cleanup.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Orion Poplawski <orion@cora.nwra.com> - 0.62-1
- Update to 0.62
- Drop test path patch fixed upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 8 2011 Orion Poplawski <orion@cora.nwra.com> - 0.59-1
- Update to 0.59
- Add patch to add ./ to path of C test command
- Re-enable all tests

* Wed Aug 24 2011 Orion Poplawski <orion@cora.nwra.com> - 0.56-2
- Disable tests that fail due to upstream test design issues

* Thu Aug 18 2011 Orion Poplawski <orion@cora.nwra.com> - 0.56-1
- Update to 0.56
- Rebuild for plplot 5.9.8

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.52-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.52-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Orion Poplawski <orion@cora.nwra.com> - 0.52-3
- Rebuild for plplot 5.9.7

* Sat Jun 05 2010 Iain Arnell <iarnell@gmail.com> 0.52-2
- rebuild with perl-5.12

* Tue May 4 2010 Orion Poplawski <orion@cora.nwra.com> - 0.52-1
- Update to 0.52

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.51-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.51-4
- rebuild against perl 5.10.1

* Mon Sep 14 2009 Orion Poplawski 0.51-3
- Add BR on perl(Test::More)
- Exclude PLplot.bs

* Thu Sep 10 2009 Orion Poplawski 0.51-2
- Use arch specific dir.

* Thu Sep 10 2009 Orion Poplawski 0.51-1
- Specfile autogenerated by cpanspec 1.78.
