%bcond_with	encoder	
# build with encoder (may require license)
#
Summary:	IDL - Scientific Programming Language
Name:		idl
Version:	80
Release:	1
%if %{with encoder}
License:	free for non-commercial, scientific use only in HDF software
%else
License:	free for use in HDF software
%endif
Group:		System/Libraries
Source0:	http://www.exelisvis.com/Product/IDL/idl%{version}linux.x86.tar.gz
Patch0:		idl80_ins.patch
URL:		http://www.exelisvis.com/ProductsServices/IDL.aspx

%description
Discover What's In Your Data. IDL is the trusted scientific programming language 
used across disciplines to extract meaningful visualizations from complex numerical data. 
With IDL you can interpret your data, expedite discoveries, and deliver powerful 
applications to market. Additionally, IDL is a truly cross-platform solution, 
providing support for today’s most popular operating systems, 
including Microsoft Windows®, Mac OS X, Linux, and Solaris.

%prep
%setup -c -n idl80
%patch0 -p0

%post
mkdir -p /usr/local/itt
./install.sh /usr/local/itt

%clean
rm -rf /usr/local/itt

%postun
/usr/local/itt/idl/idl80/bin/install

%files
%defattr(-,root,root,0755)
/usr/local/*

%dir /usr/local/itt

%changelog
* Thu Nov 20 2014 Ketan Patel <k2patel@gmail.com> 80
- First Release
