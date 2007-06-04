%define version 2.8
%define release %mkrel 16

Name:		aumix
Summary:	A GTK+/Ncurses audio mixer 
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound
BuildRequires:	ncurses-devel
BuildRequires:	gtk+2-devel
BuildRequires:	autoconf2.1
BuildRequires:	automake1.4
Source0:	http://www.jpj.net/~trevor/aumix/%{name}-%{version}.tar.bz2
# mute(1) man page (from debian):
Source1:	aumix-mute.1.bz2
Patch0:		aumix-2.7-devfs-compliant.patch.bz2
Patch1:		aumix-2.8-utf8_vs_gtk2.patch.bz2
Patch2:		aumix-2.8-close-dialogs.patch.bz2
Patch3:		aumix-2.8-nb.patch.bz2
# rawhide patches:
Patch102:  aumix-fix-cursor-color-on-exit.patch.bz2
Patch103:  aumix-2.8-fix-changing-level-non-interactively.patch.bz2
Patch104:  aumix-2.8-bug-115869.patch.bz2
URL: 		http://www.jpj.net/~trevor/aumix.html
Requires:	initscripts >= 4.42
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-builddroot

%description
This is a program for adjusting audio mixers from the command line or scripts,
or interactively at the console or a terminal with a full-screen, ncurses-based
interface or a GTK-based X interface.

%package text
Summary:	An Ncurses audio mixer 
License:	GPL
Group:		Sound

%description text
This is a program for adjusting audio mixers from the command line or scripts,
or interactively at the console or a terminal with a full-screen, ncurses-based
interface .

%prep
%setup -q
%patch0 -p1 -b .devfs
%patch1 -p1 -b .utf8
%patch2 -p0 -b .dialogs
%patch3 -p1 -b .nb
%patch102 -p0
%patch103 -p1
%patch104 -p0

# (gc) move "xaumix" to "taumix"
perl -pi -e 's|xaumix|taumix|g' doc/{*aumix.1,Makefile.am} src/{Makefile.am,xaumix}
mv doc/xaumix.1 doc/taumix.1
mv src/xaumix src/taumix

aclocal-1.4
%if %{mdkversion} >= 200600
# XXX awful, yes, but no sane way anyway
perl -pi -e 's/^(AC_PREREQ)\(2\.[^)]+\)/\1(2.13)/' aclocal.m4
%endif
automake-1.4 --gnu --include-deps src/Makefile
touch Makefile.in
WANT_AUTOCONF_2_1=1 autoconf

%build
mkdir build-text
pushd build-text
CONFIGURE_TOP=.. %configure --with-alsa --without-gtk1 --without-gtk
%make
popd
mkdir build-gui
pushd build-gui
CONFIGURE_TOP=.. %configure --with-alsa --without-gtk1
%make
popd

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall -C build-gui

# install text version
install -m755 build-text/src/aumix $RPM_BUILD_ROOT%{_bindir}/aumix-text

# menu entry
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_bindir/%name" \
needs="X11" \
icon="sound_section.png" \
section="Multimedia/Sound" \
title="Aumix" \
longtitle="Audio Mixer based on GTK+ and NCurses" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Aumix
Comment=Audio Mixer based on GTK+ and NCurses
Exec=%{name}
Icon=sound_section
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Sound;Audio;Mixer;
EOF


bzcat %SOURCE1 > $RPM_BUILD_ROOT%_mandir/man1/mute.1


%find_lang %name

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO NEWS ChangeLog
%_bindir/aumix
%_bindir/mute
%_bindir/taumix
%_mandir/man1/*
%_datadir/applications/mandriva-*
%_datadir/%name
%_menudir/*

%files text
%defattr(-,root,root)
%_bindir/aumix-text
