# surface
Maintain full control on all your dotfiles, git repos, both local and remote with one tool

## Build the project and setup the python enviroment with requirements
1.  Run **make** will setup the enviroment

## Install the program
2.  Run **sudo make install** 

## Change config locations for symlink later

3.  Open up dot_path.py
    *  Under DIRECTORIES, need to change to "Your" files location

4.  Open up confup.py
    *  Change the cofig dirs and files according to the changes made in step 1

5.  Open up gitpy_ssh
    *  Change the path to "Your" .ssh/id_rsa location, normally at /home/user/.ssh/id_rsa

6.  Open up user.cfg
    *  Update the ssh, name and email fields NB! the ssh field is the location for the file in step 3

7.  Open up the repos.cfg
    *  Here we set all the repos You want to include in the repos sync.

8.  Open main.py
    *  On line 1, set the full path to the surface folder. This is for the symlink we will create later

## For any help, type:
```
surface --help
```
