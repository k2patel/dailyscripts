#
# spec file for package LAStools
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%global commit dcb0cbba6cf4d001f86af77d025850c9777f08ff
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           LAStools
Version:        git.dcb0cbb
Release:        0%{?dist}
Summary:        LAStools - opensource tools only
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/LAStools/LAStools/archive/%{commit}/%{name}-v%{version}rel-%{shortcommit}.tar.gz
Source0:        LAStools-%{version}.tar.gz
BuildRequires:  gcc-c++
Provides:       lastools
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Only opensource tools are included:
* laszip        compresses the LAS files in a completely lossless manner
* lasinfo       prints out a quick overview of the contents of a LAS file
* lasindex      creates a spatial index LAX file for fast spatial queries
* las2las       extracts last returns, clips, subsamples, translates, etc ...
* lasmerge      merges several LAS or LAZ files into a single LAS or LAZ file
* txt2las       converts LIDAR data from ASCII text to binary LAS format
* las2txt       turns LAS into human-readable and easy-to-parse ASCII
* lasprecision  analyses the actual precision of the LIDAR points
* lasdiff       diffs LAS or LAZ files

Closed sources tools are not included.

See the REDAME.txt file or https://rapidlasso.com/lastools/ for more information.

%prep
%setup -q -n %{name}-%{commit}
rm -f bin/*.exe
rm -f bin/*.txt
rm -rf bin/serf/

%build
%if 0%{?sle_version} >= 150000
# Tumbleweed and Leap 15.x are fine but Leap 42.x and SLE12* break.
export COPTS="%{optflags}"
%endif
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/local/bin
cp -r bin/* %{buildroot}/usr/local/bin


%files
%defattr(-,root,root)
/usr/local/bin/*
%license LICENSE.txt COPYING.txt
%doc CHANGES.txt README.txt

%changelog

