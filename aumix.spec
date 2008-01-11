%define name	aumix
%define version 2.8
%define release %mkrel 18

Name:		%{name}
Summary:	A GTK+ / Ncurses audio mixer 
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound
BuildRequires:	ncurses-devel
BuildRequires:	gtk+2-devel
BuildRequires:	autoconf
BuildRequires:	automake
Source0:	http://www.jpj.net/~trevor/aumix/%{name}-%{version}.tar.bz2
# mute(1) man page (from debian):
Source1:	aumix-mute.1.bz2
Patch1:		aumix-2.8-utf8_vs_gtk2.patch
Patch2:		aumix-2.8-close-dialogs.patch
Patch3:		aumix-2.8-nb.patch
# autoconf 2.5 and later support (from debian):
Patch4:		aumix-2.8-autoconf.patch
# rawhide patches:
Patch102:  aumix-fix-cursor-color-on-exit.patch
Patch103:  aumix-2.8-fix-changing-level-non-interactively.patch
Patch104:  aumix-2.8-bug-115869.patch
URL: 		http://www.jpj.net/~trevor/aumix.html
Requires:	initscripts >= 4.42
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch1 -p1 -b .utf8
%patch2 -p0 -b .dialogs
%patch3 -p1 -b .nb
%patch4 -p1 -b .autoconf
%patch102 -p0
%patch103 -p1
%patch104 -p0

%build
aclocal
automake --add-missing
autoconf
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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Aumix
Comment=Basic volume controller
Exec=%{name}
Icon=sound_section
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Audio;Mixer;
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
%_bindir/xaumix
%_mandir/man1/*
%_datadir/applications/mandriva-*
%_datadir/%name

%files text
%defattr(-,root,root)
%_bindir/aumix-text
