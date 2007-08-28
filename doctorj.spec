%define gcj_support 1
%bcond_with tests

Summary:	Compares javadoc comments against code
Name:		doctorj
Version:	5.1.2
Release:	%mkrel 1
Epoch:		0
License:	LGPL
Group:		Development/Java
URL:		http://www.incava.org/projects/java/doctorj/index.html
Source0:	http://superb-east.dl.sourceforge.net/sourceforge/doctorj/doctorj-%{version}.tar.gz
%if %{gcj_support}
Requires(post):	java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:	java-gcj-compat-devel
%else
BuildArch: 	noarch
%endif
BuildRequires:	ant
%if %with tests
BuildRequires:	ant-junit
%endif
BuildRequires:	java-devel >= 0:1.4.2
BuildRequires:	jpackage-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Beyond the level of what Javadoc does, DoctorJ compares
documentation against code. Among what it detects:

    * misspelled words
    * parameter and exception names:
          o missing
          o misordered
          o misspelled
    * Javadoc tags:
          o invalid
          o misordered
          o missing expected arguments
          o invalid arguments
          o missing descriptions
    * undocumented classes, methods, fields, parameters

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export CLASSPATH=
export OPT_JAR_LIST=
%ant dist
%ant doc

%if %with tests
%check
export CLASSPATH=
export OPT_JAR_LIST="%{__cat} %{_sysconfdir}/ant.d/junit"
%ant tests
%endif

%install
%{__rm} -rf %{buildroot}
%ant -Ddestdir=%{buildroot} install

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a doc/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%attr(0755,root,root) %{_bindir}/%{name}
# XXX: This should probably go in %%{_javadir}.
%{_datadir}/%{name}/doctorj.jar
%{_datadir}/%{name}/words.*
%{_mandir}/man1/%{name}.1*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
