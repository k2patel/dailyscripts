
 - SZIP -> (2.1.1 -> 2.1.1-1 )
   * Added CMake support

 - HDF4 -> (4.2.13 -> 4.2.15)
   * Updated xdr to 4.9.1
   * Several memory leaks are fixed
   * Full Details at https://bitbucket.hdfgroup.org/projects/HDFFR/repos/hdf4/browse/release_notes

 - HDF5 -> (1.10.2 -> 1.12.0)
   * mpich to 3.2 and openmpi3
   * Many functional improvement with new methods
   * RFC THG 2017-07-07.v7 (H5Sencode / H5Sdecode Format Change)
   * Virtual Object Layer
   * Functions were modified in HDF5 version 1.12 to support a token type used in the Virtual Object Layer (VOL) and to enable 64-bit selection encodings.
   * fixed issue with netcdf build include file extension
   * https://portal.hdfgroup.org/display/HDF5/Migrating+from+HDF5+1.10+to+HDF5+1.12
   * https://github.com/HDFGroup/hdf5/blob/develop/release_docs/RELEASE.txt

 - Armadillo -> (8.600.0 -> 9.900.2)
   * https://gitlab.com/conradsnicta/armadillo-code/-/compare/8.600.x...9.900.x

 - Pnetcdf (Parallel-netcdf) -> (1.7.0 -> 1.12.1)
   * Support added for both mpi platform
   * A new command-line option `-t` is added to utility program `cdfdiff` to compare variable differences within a tolerance.
   * Fix strict aliasing bug when building PnetCDF with -O3 flag.
   * In dpeth https://github.com/Parallel-NetCDF/PnetCDF/blob/master/RELEASE_NOTES

 - NetCDF -> (4.6.1 -> 4.7.4)
   * Support for HDF5-1.12.0.
   * Support for multiple filters per variable.
   * nc_inq_var_szip now retuns 0 for parameter values if szip is not in use for the variable.
   * Parallel I/O with filters is allowed for HDF5-1.10.3 and later.
   * Support for zlib compression for parallel I/O writes, if HDF5 version is 1.10.3 or greater.
   * Support for szip compression when writing data (including writing in parallel if HDF5 version is 1.10.3 or greater)
   * Support for compact storage option for small variables in netCDF/HDF5 files.
   * More Details at https://www.unidata.ucar.edu/software/netcdf/docs/RELEASE_NOTES.html

 - NetCDF-Fortran -> (4.4.4 -> 4.5.3)
   * Added nf90_inq_format to the F90 API
   * Added support for HDF5 compact storage
   * Added support for creating netCDF/HDF5 files with szip compression
   * Fixed bug in the setting of file cache preemption for netCDF-4 files
   * Bugfixes to bring netCDF-Fortran in line with the features in netCDF-C.
   * More detailed information at https://github.com/Unidata/netcdf-fortran/blob/master/RELEASE_NOTES.md

 - NetCDF-Perl -> (1.2.4)
   * Rebuilt to support new netcdf.
   * LAST RELEASE (It will be removed from all DAAC system on next build)
   * This is no longer maintained and does not support more recent changes to the NetCDF.

 - nco -> (4.7.5 -> 4.9.3)
   * GPU-offloading and enable-optimize options
   * Fix FLG_ILV spuriously set despite no ilv argument
   * vectorization directives
   * More detailed at https://github.com/nco/nco/blob/master/doc/ChangeLog

 - ncview -> (2.1.7)
   * No change, but recompiled to accomodate new library.

 - Proj -> (5.1.0 -> 5.2.0)
   * datumgrids updaated to 1.8
   * Many bug fixes
   * Proj cannot be upgraded to latest stable due to dependent OS package limited to older version.
   * More detailed information https://github.com/OSGeo/PROJ/blob/5.2.0/ChangeLog

 - grib_api -> eccodes -> (2.18.0)
   * Details list version by version https://confluence.ecmwf.int/display/ECC/History+of+Changes

 - g2clib -> (1.6.0)
   * No change, but needed to rebuild to accomodate changes.

 - cdo -> (1.9.4 -> 1.9.8)
   * Proj 4 to 6 API Migration
   * smooth/smooth9: Added support for gridtype PROJECTION [Feature #9202]
   * Expr: Added function rand() and isMissval()
   * Remap: Added support for Gaussian reduced grids
   * trend, detrend: Added parameter equal=false for unequal timesteps
   * Option --no_remap_weights: Switch off generation of remap weights
   * More details at https://code.mpimet.mpg.de/projects/cdo

 - libgeotiff -> (1.4.2 -> 1.4.4)
   * Many bug fixes
   * Cannot upgrade to latest since it require proj v6 or up.
   * More detailed changelog https://github.com/OSGeo/libgeotiff/blob/1.4.3/libgeotiff/ChangeLog

 - freexl -> (1.0.5 -> 1.0.6)
   * Please see https://www.gaia-gis.it/fossil/freexl/timeline

 - libspatialite -> (4.3.0a)
   * No change, but needed to rebuild to accomodate changes.
   * Cannot move to 5.x branch because of dependency from OS.

 - ogdi -> (3.2.0 -> 4.1.0)
   * ogdi/driver/vrf/feature.c, object.c, vrf.h: make sure to take into account tile id when merging feature segments, and deal with situations where consecutive segments of same feature in edge table are not mergeable. Needed on some DNC products.
   * various changes to support Win64 and MSVC 2015

 - libkml -> (Newly added -> 1.3.0)

 - gdal -> (2.3.1 -> 2.4.4)
   * PROJ requirement does not allow to compile 3.x
   * Added libkml support
   * In details changes are at https://github.com/OSGeo/gdal/commits/v2.4.4/gdal/doc

 - ncl -> (Discontinued)
   * NCL nolonger able to compile against new library.

 - mapserver -> (7.2.0 -> 7.6.1)
   * Ruby binding for mapserver/mapscript dropped.
   * https://www.mapserver.org/development/changelog/index.html

 - ncview -> (2.1.7)
   * Rebuild to accomodate library change.

 - perl-PDL -> (2.19.0 -> 2.21.0)
   * Proj support dropped "https://bugzilla.redhat.com/show_bug.cgi?id=839651"

 - perl-PDL-NetCDF -> (4.20)
   * No change / rebuilt to accomodate new library.

 - wgrib -> (1.8.1)
   * No change / rebuilt to accomodate new library

 - wgrib2 -> (2.0.7 -> 2.0.8)
   * ens_processing: fixed spread calculation (one pass -> 2 pass calculation)
   * ndate, -ndates: added with mn (minutes) support
   * set_date, -time_processing: now supports mn time offsets added spectral option to -new_grid
   * new_grid: removed loop to determine ibi
   * set_ftime2: works with pdt 2, 3, 4, 5, 6, 9, 10, 12, 13, 15, 41, 43
   * alarm will clear alarm in finalize stage, init.c added include <string.h> in

 - netcdf4-python -> (1.4.1 -> 1.5.3)
   * In depth https://github.com/Unidata/netcdf4-python/blob/master/Changelog

 - lastools -> (dcb0cbb)
   * New package (request was created long ago)
