%define gcj_support 1
%bcond_with tests

Name:		doctorj
Version:	5.1.2
Release:	%mkrel 2
Epoch:		0
Summary:	Compares javadoc comments against code
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
BuildRequires:	java-devel
%endif
BuildRequires:	ant
%if %with tests
BuildRequires:	ant-junit
%endif
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
%doc %{_javadocdir}/%{name}
