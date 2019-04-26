# Word2RI

## Instructions for Developers

### 1. Install all the prerequisites below
  - [Virtual Box](https://www.virtualbox.org/): tested on 2.2.4
  - [Vagrant](https://www.vagrantup.com/): tested on 6.0
  - [Git](https://git-scm.com/downloads): tested on 2.20.1

### 2. Clone the repository

```
git clone https://github.com/stlim0730/wordtori.git
```

This command creates a new directory `wordtori`. In case you want multiple instances of the local repository on the same machine (e.g., running two different instances of the app on a production server), you may specify the path.

```
mkdir meaningofhome
git clone https://github.com/stlim0730/wordtori.git meaningofhome
```

This command doesn't create a new directory.

### 3. Choose an app instance

Word2RI manages multiple instances of the app using Git branches, where each app instance has its own variations of contents and configurations. One branch may represent an instance of the app (Note that there can be normal feature branches for development purpose, which isn't a representative branch for an app instance). You can lookup what branches are available in the remote repository (GitHub) using the following command.

```
git fetch --all
```

`git fetch` command collects all the updates from remote, but doesn't `merge` any of them into the current working tree in the local repository.

```
git branch
git branch --remote
git branch --all
```

`git branch` shows you the local branches available. You may use option `--remote` (or `-r`) to lookup branches in the remote repository; it's useful because the branches representing app instances would have been already built and available in the remote repository. You may switch to one of app instances by checking out a branch.

```
git checkout meaning-of-home
```

### 4. Create (turn on) a virtual machine

Word2RI runs on Ubuntu 16.04 (code name: ubuntu/xenial64). Provisional commands and configurations for virtual machine are in `deployment/provision_vagrant.sh`. `Vagrantfile` specifies the provision script to run when a virtual machine is created. Create a virtual machine with the following command in the repository root (where you cloned it) directory.

```
vagrant up
```

You may use the shell of the virtual machine by ssh command.

```
vagrant ssh
```

### 5. Making changes in the code
_IN PROGRESS_

### 6. Teardown (turn off) the virtual machine

When you finished working on the virtual machine, you may turn it off. There are three types of teardown process: destroy, halt, and suspend (This document only explains destroy and suspend). Destroy removes all traces of the virtual machine from your system and free all the resources used. When you `vagrant up` later, it goes through all the provision process, which takes time. It's useful when you want to reset the virtual machine or reinstall prerequisite packages by going through the provisional steps. Run the command below _after you exited the virtual machine's shell_ (vagrant is installed on your system, not the virtual machine).

```
vagrant destroy
```

The second type of teardown process is suspend. It's similar to _sleep_ that preserves the current state of the virtual machine so that you can pick up where you left off. `vagrant up` will quickly restore the state of the virtual machine.

```
vagrant suspend
```
