Summary:	Puzzle game similar to Oxyd
Name:		enigma-freeoxyd
Version:	1.01
Release:	%mkrel 3
Source0:	http://download.berlios.de/enigma-game/enigma-%{version}.tar.bz2
Patch1:		enigma-0.81-desktop-entry.patch
# Fix various GCC 4.3 build problems - AdamW 2008/12
Patch2:		enigma-1.01-gcc43.patch
# Fix some 'format not a string literal' errors - AdamW 2008/12
Patch3:		enigma-1.01-literal.patch
License:	GPLv2+
Group:		Games/Arcade
URL:		http://www.nongnu.org/enigma/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libpng-devel
BuildRequires:	liblua-devel
BuildRequires:	libSDL-devel
BuildRequires:	libSDL_image-devel
BuildRequires:	libSDL_mixer-devel
BuildRequires:	libSDL_ttf-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	xerces-c-devel

%description
Enigma is a tribute to and a re-implementation of one of the most
original and intriguing computer games of the 1990's: Oxyd.  Your
objective is easily explained: find and uncover all pairs of identical
Oxyd stones in each landscape.  Sounds simple?  It would be, if it
weren't for hidden traps, vast mazes, insurmountable obstacles and
innumerable puzzles blocking your direct way to the Oxyd stones...

%prep
%setup -q -n enigma-%{version}
%patch1 -p1
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .literal

%build
%configure2_5x
%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std

mv %{buildroot}/%_docdir/enigma installed-docs
mv %{buildroot}/%{_bindir}/enigma %{buildroot}/%{_bindir}/%{name}

# (blino) remove devel files
rm -rf %{buildroot}%{_includedir} %{buildroot}%{_libdir}/*.a

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="PuzzleGame" \
  --add-category="ArcadeGame;LogicGame" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang enigma

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f enigma.lang
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/enigma
%{_datadir}/applications/*
%doc installed-docs/*
%{_mandir}/man6/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/pixmaps/*

