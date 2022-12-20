Name: antlr4-cpp-runtime
Version: 4.9.3
Release: 3%{?dist}
Summary: Parser generator (ANother Tool for Language Recognition) runtime for C++

License: BSD
URL: https://www.antlr.org/
Source0: antlr4-%{version}.tar.gz
%global source0_sha512 61452404c9639b5a0908cda16605f17c0fed0c9adfc3278c7408f9971420e9d1fe8f9e974e0826c2e3e780fdd83324094c0246cd5b28fa63f5686b094ea08127
%global source0_url https://src.fedoraproject.org/repo/pkgs/antlr4-project/antlr4-%{version}.tar.gz/sha512/%{source0_sha512}/antlr4-%{version}.tar.gz
Patch1: antlr4-disable-pkgconfig.patch 

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: utf8cpp-devel
BuildRequires: uuid-devel
BuildRequires: wget

%description
This package provides the runtime library used by C++ ANTLR parsers.

%package devel
Summary: Header files for programs that use C++ ANTLR parsers
Requires: antlr4-cpp-runtime%{?_isa} = %{version}-%{release}

%description -n antlr4-cpp-runtime-devel
This package provides header files for programs that use C++ ANTLR
parsers.

%prep
pushd %{_sourcedir}
if [ ! -s %{SOURCE0} ] ; then
	rm %{SOURCE0}
	wget -nv %{source0_url}
fi
echo "%{source0_sha512}  $(basename %{SOURCE0})" | sha512sum -c
popd

%autosetup -n antlr4-%{version} -p1

# Use utf8cpp instead of the deprecated wstring_convert
sed -i 's/# \(.*DUSE_UTF8_INSTEAD_OF_CODECVT.*\)/\1/' runtime/Cpp/CMakeLists.txt

# Change library install directory on 64-bit platforms
if [ "%{_lib}" != "lib" ]; then
  sed -i 's/DESTINATION lib/&64/' runtime/Cpp/runtime/CMakeLists.txt
fi

%build

# Build the C++ runtime
cd runtime/Cpp
%cmake \
    -DANTLR4_INSTALL=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_CXX_STANDARD=11
%cmake_build
cd -

%install

# Install the C++ runtime
cd runtime/Cpp
%cmake_install
rm -f %{buildroot}%{_libdir}/libantlr4-runtime.a
cd -

# Clean up bits we do not want
rm -fr %{buildroot}%{_docdir}/libantlr4

%files -n antlr4-cpp-runtime
%doc runtime/Cpp/README.md
%license LICENSE.txt
%{_libdir}/libantlr4-runtime.so.%{version}

%files devel
%doc runtime/Cpp/cmake/Antlr4Package.md runtime/Cpp/cmake/README.md
%{_includedir}/antlr4-runtime/
%{_libdir}/libantlr4-runtime.so
%{_libdir}/cmake/antlr4-generator/
%{_libdir}/cmake/antlr4-runtime/

%changelog
* Tue Dec 20 2022 Alex Kasko <alex@staticlibs@gmail.com> - 4.9.3-3
- Adapt the C++ runtime part from ttps://src.fedoraproject.org/rpms/antlr4-project

