Helios quick start
==================

The following are (unofficial) instructions to run the development
version of Helios. They are inspired from the [official
instructions](http://documentation.heliosvoting.org/install), and
various discussions on the
[helios-voting](http://groups.google.com/group/helios-voting) Google
group.

Warning: these instructions are based on Debian Wheezy, which is still
in development!


Setting up a virtual machine
----------------------------

 1. Download a Debian 6 (a.k.a. "Squeeze") ISO [installation image](http://ftp.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/mini.iso) (19M):

        wget http://ftp.debian.org/debian/dists/squeeze/main/installer-amd64/current/images/netboot/mini.iso

 2. Create an empty QEMU image (on Debian, the `qemu-img` command is
    provided by the 'qemu-utils' package):

        qemu-img create -f qcow2 helios.qcow2 5G

 3. Run the Debian installer (on Debian, you need the 'qemu-kvm' or
    the 'qemu' package):

        kvm -m 256M -cdrom mini.iso -hda helios.qcow2

    The `kvm` command might be `qemu-kvm`, depending on your host
    environment. You can also use `qemu` instead of `kvm`, which is
    significantly slower. For now, perform a minimal installation with
    standard system utilities. Once the installation is complete, the
    virtual machine will reboot.

    To start the VM afterwards, and access the development webserver
    from outside the VM, run `kvm` like this:

        kvm -m 256M -hda helios.qcow2 -net nic -net user,hostfwd=tcp:127.0.0.1:8000-:8000

 4. Upgrade to Wheezy. From the root account, run:

        sed -i s/squeeze/wheezy/ /etc/apt/sources.list
        sed -i /-updates/d /etc/apt/sources.list
        apt-get update
        apt-get dist-upgrade

    On a fairly recent machine with a decent Internet connection, the
    instructions above take less than one hour, and the resulting
    image (helios.qcow2) is approximately 1.4 GB.

    In your reports, please include the head of your Release file:

        $ head /var/lib/apt/lists/*_wheezy_Release
        Origin: Debian
        Label: Debian
        Suite: testing
        Codename: wheezy
        Date: Mon, 18 Jun 2012 08:31:46 UTC
        Valid-Until: Mon, 25 Jun 2012 08:31:46 UTC
        Architectures: amd64 armel armhf i386 ia64 kfreebsd-amd64 kfreebsd-i386 mips mipsel powerpc s390 s390x sparc
        Components: main contrib non-free
        Description: Debian x.y Testing distribution - Not Released
        MD5Sum:


Setting up Helios
-----------------

 1. On a freshly installed Debian 7 (a.k.a. "Wheezy") (e.g. the
    virtual machine created above), run the following commands as
    `root`:

        apt-get install git postgresql python-django python-openid python-psycopg2 python-django-south python-django-celery python-kombu
        su -c "createuser --superuser $HELIOS_USER" postgres

    where `$HELIOS_USER` is the (non-root) user that will run
    Helios. From now on, we assume that all commands are run as
    `$HELIOS_USER`.

 2. Get Helios proper:

        git clone https://github.com/glondu/helios-server.git
        cd helios-server

    This branch contains fixes to make Helios work with standard
    Debian packages. There are some hard-coded values in
    'settings.py'; you might want to change some of them... but there
    is no need for basic operations.


Running Helios
--------------

 1. Set up the database:

        ./reset.sh

    You can run this command as much as you want to reset the
    database. The first time, it complains that the 'helios' database
    doesn't exist; don't worry.

 2. Run the development server:

        python manage.py runserver 0.0.0.0:8000

    With the default settings, and if you run Helios in a VM launched
    as instructed above, the webserver should be accessible from the
    host at http://localhost:8000/.


Dealing with mails
------------------

By default, 'exim4' is installed for local mail delivery. Helios is
set up to use it. Outgoing mails such as those sent by Helios will be
frozen and kept in the queue. You can inspect them by running the
following commands as root, or as a user that belongs to the group
'Debian-exim'.

 - To see the contents of the queue, run:

        mailq

 - To see the contents of one mail, run:

        exim -Mvb $ID

    where `$ID` is the identifier appearing in the output of `mailq`.

 - To remove a mail from the queue, run:

        exim -Mrm $ID

   For more information, refer to the Exim documentation.
