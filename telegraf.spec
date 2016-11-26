%define cwd %(pwd)

Name:	telegraf
Version: %(git describe --tags | sed 's/-/_/g')
Release:	0%{?dist}
Summary:	Telegraf

Group:		Applications/System
License:	GPL
URL:		http://github.com/influxdata/telegraf

%description

%prep
%setup -c -T
mkdir -p go/src/github.com/influxdata/telegraf
cp -a %{cwd}/. go/src/github.com/influxdata/telegraf

%build
%define debug_package %{nil}
export GOPATH=$(pwd)/go
export PATH=${GOPATH}/bin:$PATH
go get github.com/sparrc/gdm
cd go/src/github.com/influxdata/telegraf
gdm restore
go build ./cmd/telegraf

%install
cd go/src/github.com/influxdata/telegraf
install -D etc/telegraf.conf %{buildroot}/etc/telegraf/telegraf.conf
install -D -d %{buildroot}/etc/telegraf/telegraf.d
install -D scripts/telegraf.service %{buildroot}/lib/systemd/system/telegraf.service
install -D telegraf %{buildroot}/usr/bin/telegraf

%post
if ! id telegraf &>/dev/null; then
	useradd -r -K USERGROUPS_ENAB=yes -M telegraf -s /bin/false -d /etc/telegraf
fi

%files
%config(noreplace) /etc/telegraf
%config(noreplace) /etc/telegraf/*
/lib/systemd/system/telegraf.service
/usr/bin/telegraf
