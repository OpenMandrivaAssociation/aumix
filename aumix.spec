%define name	aumix
%define version 2.9.1
%define release %mkrel 1

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

%build
mkdir build-text
pushd build-text
CONFIGURE_TOP=.. %configure2_5x --without-gtk
%make
popd
mkdir build-gui
pushd build-gui
CONFIGURE_TOP=.. %configure2_5x
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

%find_lang %name

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

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
