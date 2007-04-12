Summary: Enigma is a puzzle game similar to Oxyd
Name: enigma-freeoxyd
Version: 0.92
Release: %mkrel 2
Source0: http://savannah.nongnu.org/download/enigma/enigma-%{version}.tar.bz2
Patch1: enigma-0.81-desktop-entry.patch
Patch2: enigma-0.92-gcc4.1.patch
License: GPL
Group: Games/Arcade
URL: http://www.nongnu.org/enigma/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: libpng-devel
BuildRequires: liblua-devel libSDL-devel libSDL_image-devel
BuildRequires: libSDL_mixer-devel libSDL_ttf-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils

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
%patch2 -p1
%build

./configure --prefix=%_prefix --libdir=%_libdir

%make

%install
rm -rf $RPM_BUILD_ROOT installed-docs

make install prefix=$RPM_BUILD_ROOT%_prefix

mkdir -p $RPM_BUILD_ROOT%_mandir/man6
mv $RPM_BUILD_ROOT%_prefix/man/man6/* $RPM_BUILD_ROOT%_mandir/man6/
mv $RPM_BUILD_ROOT/%_docdir/enigma installed-docs

mv $RPM_BUILD_ROOT/%_bindir/enigma $RPM_BUILD_ROOT/%_bindir/%name

mkdir -p $RPM_BUILD_ROOT%{_menudir}

cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
	command="%{_bindir}/%{name}" \
	needs="x11" \
	section="More Applications/Games/Arcade" \
	title="Enigma" \
	icon="%name.png" \
	longtitle="Enigma is a puzzle game similar to Oxyd" \
	startup_notify="false" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="PuzzleGame" \
  --add-category="X-MandrivaLinux-MoreApplications-Games-Arcade" \
  --add-category="ArcadeGame;LogicGame" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
ln -s %_datadir/pixmaps/enigma.png %buildroot%_liconsdir/%name.png
convert -scale 32x32 etc/enigma.png %buildroot%_iconsdir/%name.png
convert -scale 16x16 etc/enigma.png %buildroot%_miconsdir/%name.png

%find_lang enigma

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%files -f enigma.lang
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/enigma
%{_datadir}/applications/*
%doc installed-docs/*
%{_mandir}/man6/*
%_datadir/icons/hicolor/48x48/apps/*
%_datadir/pixmaps/*
%{_menudir}/*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

