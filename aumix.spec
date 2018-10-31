Summary:	A GTK+ / Ncurses audio mixer
Name:		aumix
Version:	2.9.1
Release:	22
License:	GPLv2+
Group:		Sound
Source0:	http://www.jpj.net/~trevor/aumix/releases/%{name}-%{version}.tar.bz2
Url: 		http://www.jpj.net/~trevor/aumix.html
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ncurses)
Requires:	initscripts >= 4.42

%description
This is a program for adjusting audio mixers from the command line or scripts,
or interactively at the console or a terminal with a full-screen, ncurses-based
interface or a GTK-based X interface.

%files -f %{name}.lang
%doc README TODO NEWS ChangeLog
%{_bindir}/aumix
%{_bindir}/mute
%{_bindir}/xaumix
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}

#----------------------------------------------------------------------------

%package text
Summary:	An Ncurses audio mixer
Group:		Sound

%description text
This is a program for adjusting audio mixers from the command line or scripts,
or interactively at the console or a terminal with a full-screen, ncurses-based
interface .

%files text
%{_bindir}/aumix-text

#----------------------------------------------------------------------------

%prep
%setup -q
cp -f %{_datadir}/libtool/config/* build-aux/
./bootstrap

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
%makeinstall -C build-gui

# install text version
install -m755 build-text/src/aumix %{buildroot}%{_bindir}/aumix-text

# menu entry

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Aumix
Name[ru]=Aumix
Comment=Basic volume controller
Comment[ru]=Регулятор громкости
Exec=%{name}
Icon=sound_section
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Audio;Mixer;
EOF

%find_lang %{name}

