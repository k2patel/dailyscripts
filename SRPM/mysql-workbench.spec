
# This is the SPEC file to build RPM packages for MySQL Workbench
# 
# To use this file, you should define several macros when calling
# rpmbuild, in order to specify the edition, version and release
# numbers of the current build.
#
# Here's a usage example:
# rpmbuild -ba mysql-workbench.spec --target=`arch` \
#                                   --define='edition community' \
#                                   --define='version 6.3.5' \
#                                   --define='release 1' 
####################################################################
%bcond_with paramiko

# Allow to continue when a binary with no build-id was found
%undefine _missing_build_ids_terminate_build

%if !%{defined version}
%define version         6.3.5
%endif

# whether at least Python 2.6 is available
%define have_python26   1
%include %{_rpmconfigdir}/macros.python

# Directory where iodbc and pyodbc binaries are located. Build both using the build_iodbc.sh script
# If using distribution provided ODBC manager lib and pyodbc, then comment out this
%define linuxres_home     $HOME/linux-res
%define linuxres_binaries %{linuxres_home}/builds

%define odbc_home         %{linuxres_binaries}/odbc/usr/local
%define ctemplate_dir     %{linuxres_binaries}/ctemplate/usr/local
%define sqlite_dir        %{linuxres_binaries}/sqlite
%define pysqlite_dir      %{linuxres_binaries}/pysqlite2
%define python_dir        %{linuxres_home}/python
%define pyodbc_dir        %{linuxres_binaries}/pyodbc


%if "%{edition}" == "commercial"
%define commercial       1
%define mysqlcppconn_dir %{linuxres_binaries}/cppconn-com/usr/local
%define gdal_dir         %{linuxres_binaries}/gdal-com/usr/local
%define vsqlite_dir       %{linuxres_binaries}/vsqlite-com/usr/local
%define mysql_home       $HOME/mysql-server-advanced

%define edition          commercial
%define license_type     Commercial
%define license_file     LICENSE.mysql
%else
%define community        1
%define mysqlcppconn_dir %{linuxres_binaries}/cppconn-gpl/usr/local
%define gdal_dir         %{linuxres_binaries}/gdal-gpl/usr/local
%define vsqlite_dir       %{linuxres_binaries}/vsqlite-gpl/usr/local
%define mysql_home       $HOME/mysql-server

%define edition          community
%define license_type     GPLv2
%define license_file     COPYING
%endif

Summary: A MySQL visual database modeling, administration, development and migration tool
Name   : mysql-workbench-%{edition}
Version: %{version}
Release: %{release}%{?dist}
Group  : Applications/Databases
Vendor : Oracle Corporation
License: %{license_type}
URL    : http://wb.mysql.com
Source : %{name}-%{version}-src.tar.gz

BuildRoot    : %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel >= 3.9
%if 0%{?fedora} >= 20

%endif
BuildRequires: cmake >= 2.8
BuildRequires: libzip-devel libxml2-devel
BuildRequires: python-devel >= 2.5
%if 0%{?rhel} == 6
BuildRequires: boost148-devel
%else
BuildRequires: boost-devel
%endif
BuildRequires: gtk2-devel >= 2.20
BuildRequires: gtkmm24-devel
BuildRequires: mesa-libGL-devel
BuildRequires: sqlite-devel
BuildRequires: make
BuildRequires: tar
BuildRequires: gcc-c++
BuildRequires: swig >= 1.3
BuildRequires: proj-devel

%if 0%{?fedora} >= 18
BuildRequires: libgnome-keyring-devel libuuid-devel tinyxml-devel vsqlite++-devel ctemplate-devel
%else
BuildRequires: gnome-keyring-devel
%endif
%if 0%{?rhel} == 6
BuildRequires: redhat-rpm-config
%endif

Provides: mysql-workbench = %{version}-%{release}
Provides: mysql-workbench%{?_isa} = %{version}-%{release}
Requires: tinyxml
Requires: libzip
%if %{without paramiko}
Requires: python-paramiko >= 1.15.1
%endif
Requires: gnome-keyring
Requires: proj
Requires: glib2 >= 2.28
Requires: gtk2 >= 2.20

# our old package names
Obsoletes: mysql-workbench < 6.1
Conflicts: mysql-workbench-oss
Conflicts: mysql-workbench-com-se
Conflicts: mysql-workbench-gpl

%if 0%{?commercial}
Obsoletes: mysql-workbench-com-se
Conflicts: mysql-workbench-community
%else
Obsoletes: mysql-workbench-oss
Obsoletes: mysql-workbench-gpl
Conflicts: mysql-workbench-commercial
%endif


# Filtering: https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
%if 0%{?fedora}
%if 0%{?commercial}
%global __requires_exclude ^lib(antlr3c_wb|cdbc|grt|linux_utilities|mdcanvasgtk|mdcanvas|mforms|mysqlparser|sqlparser|sqlide|wbbase|wbpublic|wbprivate|wbscintilla|mysqlcppconn|iodbc|iodbcadm|iodbcinst|mysqlclient|gdal|sqlite3)\\.so.*$
%global __requires_exclude %{__requires_exclude}|db.*)\\.so.*$
%global __requires_exclude %{__requires_exclude}|wb.*)\\.so.*$
%else
%global __requires_exclude ^lib(antlr3c_wb|cdbc|grt|linux_utilities|mdcanvasgtk|mdcanvas|mforms|mysqlparser|sqlparser|sqlide|wbbase|wbpublic|wbprivate|wbscintilla|mysqlcppconn|iodbc|iodbcadm|iodbcinst|mysqlclient|gdal|wb.*|db.*)\\.so.*$
%global __requires_exclude %{__requires_exclude}|db.*)\\.so.*$
%global __requires_exclude %{__requires_exclude}|wb.*)\\.so.*$
%endif
%global __provides_exclude_from ^(%{_libdir}/mysql.workbench/.*\\.so.*|%{_libdir}/mysql/libmysqlclient\\.so.*|%{mysqlcppconn_dir}/lib/libmysqlcppconn\\.so.*|%{odbc_home}/lib/libiodbc\\.so.*)$
%endif

%if 0%{?rhel}
%{?filter_setup:
  %filter_provides_in %{_libdir}/mysql/libmysqlclient/.*\.so.*$
  %filter_provides_in %{mysqlcppconn_dir}/lib/libmysqlcppconn/.*\.so.*$
  %filter_provides_in %{_libdir}/mysql.workbench/.*\.so.*$
  %filter_requires_in %{_libdir}/mysql.workbench/modules/.*\.so.*$
  %filter_requires_in %{_libdir}/mysql.workbench/plugins/.*\.so.*$
  %filter_from_requires /libantlr3c_wb/d
  %filter_from_requires /libcdbc/d
  %filter_from_requires /libgrt/d
  %filter_from_requires /liblinux_utilities/d
  %filter_from_requires /libmdcanvasgtk/d
  %filter_from_requires /libmdcanvas/d
  %filter_from_requires /libmforms/d
  %filter_from_requires /libmysqlparser/d
  %filter_from_requires /libsqlparser/d
  %filter_from_requires /libsqlide/d
  %filter_from_requires /libwbbase/d
  %filter_from_requires /libwbpublic/d
  %filter_from_requires /libwbprivate/d
  %filter_from_requires /libwbscintilla/d
  %filter_from_requires /libmysqlcppconn/d
  %filter_from_requires /libmysqlcppconn/d
  %filter_from_requires /libiodbc/d
  %filter_from_requires /libiodbcadm/d
  %filter_from_requires /libiodbcinst/d
  %filter_from_requires /libvsqlitepp/d
  %filter_from_requires /libmysqlclient/d
  %filter_from_requires /libgdal/d
  %filter_from_requires /libctemplate/d
#
# Don't bundle libzip.so neither libtinyxml.so. Those can be found in EPEL.
#  
#  %filter_from_requires /libzip/d
#  %filter_from_requires /libtinyxml/d
  %{?commercial:%filter_from_requires /libsqlite3/d}
  %filter_setup
}
%endif




%description
MySQL Workbench is a unified visual tool for database architects, developers, 
and DBAs. MySQL Workbench provides data modeling, SQL development, and 
comprehensive administration tools for server configuration, user 
administration, backup, and much more. MySQL Workbench is available on 
Windows, Linux and Mac OS X.


%prep

# Add the -D flag if you don't want to delete the source root on each build
%setup -q -n %{name}-%{version}-src


%build
%cmake -DCMAKE_BUILD_TYPE=Release \
       -DREAL_EXECUTABLE_DIR=%{_libexecdir}/mysql-workbench \
       -DMYSQL_CONFIG_PATH=%{mysql_home}/bin/mysql_config \
       -DMYSQLCPPCONN_LIBRARY="-L%{mysqlcppconn_dir}/lib -lmysqlcppconn" \
       -DMYSQLCPPCONN_INCLUDE_DIR=%{mysqlcppconn_dir}/include \
       -DIODBC_CONFIG_PATH=%{odbc_home}/bin/iodbc-config \
       -DGDAL_INCLUDE_DIR=%{gdal_dir}/include -DGDAL_LIBRARY=%{gdal_dir}/lib/libgdal.so \
%if 0%{?rhel} == 6
       -DVSQLITE_INCLUDE_DIR=%{vsqlite_dir}/include \
       -DVSQLITE_LIBRARIES="-L%{vsqlite_dir}/lib -lvsqlitepp" \
%endif
       -DUSE_BUNDLED_MYSQLDUMP=1

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/usr/share/doc/mysql-workbench

%if  %{defined mysqlcppconn_dir}
    cp -a %{mysqlcppconn_dir}/lib/libmysqlcppconn.so.7* %{buildroot}%{_libdir}/mysql-workbench
%endif

if [ -f %{vsqlite_dir}/lib/libvsqlitepp.so.3 ]; then
    cp -a %{vsqlite_dir}/lib/libvsqlitepp.so.3* %{buildroot}%{_libdir}/mysql-workbench
fi

# Bundle client programs and lib
%if %{defined mysql_home}
  cp -a %{mysql_home}/lib/libmysqlclient.so.* %{buildroot}%{_libdir}/mysql-workbench/
  cp -a %{mysql_home}/bin/mysql %{buildroot}%{_libexecdir}/mysql-workbench/
  cp -a %{mysql_home}/bin/mysqldump %{buildroot}%{_libexecdir}/mysql-workbench/
%endif

#
# Don't bundle libzip.so neither libtinyxml.so. Those can be found in EPEL.
#
#%if 0%{?rhel}
#  cp -a /usr/lib64/libzip.so* %{buildroot}%{_libdir}/mysql-workbench/
#  cp -a /usr/lib64/libtinyxml.so* %{buildroot}%{_libdir}/mysql-workbench/
#%endif


%if 0%{?fedora} 
  cp -a /usr/lib64/libctemplate.so* %{buildroot}%{_libdir}/mysql-workbench
%else
%if 0%{?rhel} < 7
    cp -a %{ctemplate_dir}/lib/libctemplate.so* %{buildroot}%{_libdir}/mysql-workbench
%endif
%if 0%{?rhel} >= 7
    cp -a /usr/lib64/libctemplate.so* %{buildroot}%{_libdir}/mysql-workbench
%endif
%endif


find %{buildroot}%{_libdir}/mysql-workbench -name \*.a  -exec rm {} \; -print
find %{buildroot}%{_libdir}/mysql-workbench -name \*.la -exec rm {} \; -print

# Bundle pre-built libs
%if %{defined odbc_home}
  for l in %{odbc_home}/lib/libiodbc.so.* %{odbc_home}/lib/libiodbcinst.so.* %{odbc_home}/lib/libiodbcadm.so.*; do
    cp -a $l %{buildroot}%{_libdir}/mysql-workbench
    /usr/sbin/prelink -u %{buildroot}%{_libdir}/mysql-workbench/`basename $l` || true
  done
  cp -a %{odbc_home}/bin/iodbcadm-gtk %{buildroot}%{_libexecdir}/mysql-workbench/
%endif

if [ %{pyodbc_dir} ]; then
  cp -a %{pyodbc_dir}/pyodbc.so %{buildroot}%{_libdir}/mysql-workbench/modules
%if 0%{?commercial}
  # Bundle libs only needed in commercial edition
  cp -a %{sqlite_dir}/libsqlite3.so %{buildroot}%{_libdir}/mysql-workbench/
  cp -a %{pysqlite_dir} %{buildroot}%{_libdir}/mysql-workbench/modules
%endif
fi

%if %{with paramiko}
  cp -a %{python_dir}/paramiko %{buildroot}%{_libdir}/mysql-workbench/modules/
  cp -a %{python_dir}/ecdsa %{buildroot}%{_libdir}/mysql-workbench/modules/
%endif

cp -a %{gdal_dir}/lib/libgdal.so.* %{buildroot}%{_libdir}/mysql-workbench/

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database
fi

if [ -x %{_bindir}/update-mime-database ]; then
    %{_bindir}/update-mime-database %{_datadir}/mime 2>&1 > /dev/null || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database
fi

if [ -x %{_bindir}/update-mime-database ]; then
    %{_bindir}/update-mime-database %{_datadir}/mime 2>&1 > /dev/null || :
fi


%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}-src


%files 
%defattr(0644, root, root, 0755)
%doc %{license_file} README

%attr(0755,root,root) %{_bindir}/mysql-workbench
%attr(0755,root,root) %{_bindir}/wbcopytables

%dir %{_libexecdir}/mysql-workbench
%attr(0755,root,root) %{_libexecdir}/mysql-workbench/mysql-workbench-bin
%attr(0755,root,root) %{_libexecdir}/mysql-workbench/wbcopytables-bin
%attr(0755,root,root) %{_libexecdir}/mysql-workbench/iodbcadm-gtk
%attr(0755,root,root) %{_libexecdir}/mysql-workbench/mysql
%attr(0755,root,root) %{_libexecdir}/mysql-workbench/mysqldump

%{_libdir}/mysql-workbench

%{_datadir}/mysql-workbench
%attr(0755,root,root) %{_datadir}/mysql-workbench/extras/*.sh

%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_datadir}/applications/*.desktop


%if 0%{?fedora} == 19
%debug_package
%endif

%changelog

