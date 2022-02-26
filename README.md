# surface
Maintain full control on all your dotfiles, git repos, both local and remote with one tool

## Build the project and setup the python enviroment with requirements
1.  Run **make** will setup the enviroment

## Change config locations for symlink later

1.  Open up pygit.py
    *  On line 74 and 93, change the path to the location of the user.cfg file
    *  On line 105 change the path to the location of the repos.cfg file

2.  Open up confup.py
    *  Under DIRECTORIES, from line 40 - 64, need to change to "Your" files location
    *  Then under functions, **push, pull** The new variable names need to be updated

3.  Open up gitpy_ssh
    *  Change the path to "Your" .ssh/id_rsa location

4.  Open up user.cfg
    *  Update the ssh, name and email fields NB! the ssh field is the location for the prio part

5.  Open up the repos.cfg
    *  Here we set all the repos You want to include in the repos sync.

6.  Open main.py
    *  On line 1, set the full path to the surface folder. This is for the symlink we will create later

7.  Now we are ready to create our symlink, so with just a command in the terminal we can run the program.

```
sudo ln -s /home/user/full/path/to/surface/src/main.py /usr/local/bin/surface
```

## Now the program should be ready to use
```
surface --help
```

For help on what to run
