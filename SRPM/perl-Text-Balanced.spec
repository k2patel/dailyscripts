Name:           perl-Text-Balanced
Version:        2.03
Release:        348%{?dist}
Summary:        Extract delimited text sequences from strings
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-Balanced/
Source0:        http://www.cpan.org/authors/id/S/SH/SHAY/Text-Balanced-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(SelfLoader)
# Tests:
BuildRequires:  perl(Test::More) >= 0.47
# Perl::MinimumVersion 1.20 not used
# Pod::Simple 3.07 not used
# Test::CPAN::Meta 0.12 not used
# Test::MinimumVersion 0.008 not used
# Test::Pod 1.26 not used
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Conflicts:      perl < 4:5.16.3-286

%description
These Perl subroutines may be used to extract a delimited substring, possibly
after skipping a specified prefix string.

%prep
%setup -q -n Text-Balanced-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> 2.03-348
- Specfile autogenerated by cpanspec 1.78.
