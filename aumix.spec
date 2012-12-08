%define name	aumix
%define version 2.9.1
%define release %mkrel 4

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


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.9.1-2mdv2011.0
+ Revision: 662892
- mass rebuild

* Thu Sep 23 2010 Funda Wang <fwang@mandriva.org> 2.9.1-1mdv2011.0
+ Revision: 580747
- New version 2.9.1

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8-21mdv2010.1
+ Revision: 520008
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.8-20mdv2010.0
+ Revision: 413130
- rebuild

* Mon Dec 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.8-19mdv2009.1
+ Revision: 321081
- fix build with -Werror=format-security (P5)

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 2.8-18mdv2009.0
+ Revision: 218435
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.8-18mdv2008.1
+ Revision: 148878
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'
- fix man pages

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Jun 18 2007 Adam Williamson <awilliamson@mandriva.org> 2.8-17mdv2008.0
+ Revision: 40779
- rebuild for 2008
- drop old menu entry
- don't rename xaumix as taumix, seems pointless
- patch4 to allow autoconf 2.5 and later to work (from Debian)
- bunzip2 patches

  + Christiaan Welvaart <spturtle@mandriva.org>
    - Import aumix



* Mon Sep 18 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.8-16mdv2007.0
- Rebuild

* Tue Aug  1 2006 Götz Waschk <waschk@mandriva.org> 2.8-15mdv2007.0
- xdg menu

* Sun May 28 2006 Stefan van der Eijk <stefan@eijk.nu> 2.8-14mdk
- %%mkrel

* Fri May 12 2006 Stefan van der Eijk <stefan@eijk.nu> 2.8-13mdk
- rebuild for sparc

* Fri Sep 16 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.8-12mdk
- fix build in MDV 2006
- split out aumix-tex for sound-scripts

* Thu Jan 06 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8-11mdk
- add BuildRequires: automake1.4

* Wed Jan  5 2005 Pixel <pixel@mandrakesoft.com> 2.8-10mdk
- fix stupid patch 103

* Tue Jan 04 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8-9mdk
- merge in fedora patches:
  o patch 102: fix cursor color on exit
  o patch 103: fix a buffer overflow
  o patch 104: fix /usr/bin/mute not restorin volume when unmuting

* Mon Jun 07 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.8-8mdk
- buildrequires
- add nb translation (P3 by me:)

* Wed Jan 28 2004 Abel Cheung <deaddog@deaddog.org> 2.8-7mdk
- BuildRequires

* Mon Sep 08 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8-6mdk
- add mute(1) man page

* Thu Sep 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8-5mdk
- patch 2: destroy save/open dialogs on "ok" button press (#5260)

* Tue Jul 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8-4mdk
- patch 1: fix #4164

* Sun Jun 29 2003 Stefan van der Eijk <stefan@eijk.nu> 2.8-3mdk
- BuildConflicts & BuildRequires

* Sat Jun 28 2003 Götz Waschk <waschk@linux-mandrake.com> 2.8-2mdk
- fix menu

* Wed Jun 25 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8-1mdk
- new release
- remove useless prefix
- remove translation updates (merged upstream)
- remove patches 200 and 201 (merged upstream)
- remove gtk+1 support (Han Boetes)

* Mon Apr 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-13mdk
- drop Fabian espanol translation [was Patch2]
- update brazilian, chinese, dutch, espanol, french, galician, german,
  slovenian, swedish and ukrainian translations
  [Patches 100 to 109]
- made sure that start/save routines are not executed twice [Patch200]
- fix for newer autoconf [Patch201] :
  Newer autoconf requires that arguments with internal whitespace be quoted, so
  we patch up configure here for when the makefiles run autoconf later.
- adds three new things that can be hidden (and later shown again) to the View
  menu in the GTK+ interface [Patch202] :
	- Menu, for the menu bar itself (it can be shown again by pressing the
	  hotkey)
	- Balance, for the balances
	- Numbers, to get rid of all those confusing numbers.


* Mon Mar 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-12mdk
- update spanish translation (Fabian Mandelbaum)

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 2.7-11mdk
- Fix menu entry (icon)

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-10mdk
- build release

* Tue Sep  4 2001 Pixel <pixel@mandrakesoft.com> 2.7-9mdk
- devfs compliant

* Tue Jun 19 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-8mdk
- build release
- minor fixes

* Tue Nov 21 2000 Egil Moller <redhog@mandrakesoft.com> 2.7-7mdk
- Fixed the URL

* Tue Nov 21 2000 Egil Moller <redhog@mandrakesoft.com> 2.7-6mdk
- Added large-icon to make rpmlint happy

* Sat Sep 08 2000 David BAUDENS <baudens@mandrakesoft.com> 2.7-5mdk
- Fix menu entry

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.7-4mdk
- automatically added BuildRequires

* Wed Jul 19 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-3mdk
- rebuild for buggy %% clean_menus

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-2mdk
- rebuild for BM

* Fri Jul 14 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-1mdk
- 2.7
- menu macros

* Tue Jun 27 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.6.1-1mdk
- 2.6.1
- chmouelization of specfile
- now "xaumix" has been renamed to "taumix"

* Fri Apr 28 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.6-3mdk
- corrected menu entry, added 32x32 icon

* Mon Apr 17 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.6-2mdk
- remove aumix-minimal, chmouel doesn't need it anymore
- patch to provide a correct DATADIRNAME

* Thu Apr 13 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.6-1mdk
- 2.6
- nice, this new version fixes a small bug :-)

* Mon Apr 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-2mdk
- added URL
- added hand-drawn (oops..) icon

* Fri Mar 31 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-1mdk
- 2.5

* Thu Mar 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4-1mdk
- 2.4 with french translation :-)
- better without-gtk patch
- new groups
- menu entry

* Tue Mar 14 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.2-1mdk
- 2.2
- patch to new sources to continue to support aumix-minimal

* Thu Mar  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1-2mdk
- Remove dependences of gtk for aumix-minimal.

* Sun Feb 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1-1mdk
- Clean-up spec (thanks deb-helper).
- Reinsert aumix-minimal.
- 2.1.

* Tue Nov 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix xmix.

* Mon Nov 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.28.
- Correcting files list.

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.27.
- --with-alsa.

* Tue Sep 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed ukrainian language code (it is 'uk' not 'ua')

* Wed Jun 23 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.18.2 to 1.22.1
- removed obsolete patch for 1.18.2

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 2)

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- update to 1.18.2

* Mon Feb 22 1999 Bill Nottingham <notting@redhat.com>
- update to 1.18.1

* Mon Feb  8 1999 Bill Nottingham <notting@redhat.com>
- update to 1.17

* Mon Feb  1 1999 Bill Nottingham <notting@redhat.com>
- update to 1.15

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- update to 1.14

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binary

* Fri Oct  2 1998 Bill Nottingham <notting@redhat.com>
- updated to 1.13

* Fri Aug 28 1998 Bill Nottingham <notting@redhat.com>
- updated to 1.12

* Mon Aug 17 1998 Bill Nottingham <notting@redhat.com>
- updated to 1.11

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.8

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- fixed source url
- updated version

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built with glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 1.6.1.
