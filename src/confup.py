import shutil, os
import config
from shutil import ignore_patterns, copy2, Error, copystat
from stringcolor import *
from dot_path import *

def configDir(src, dst, symlinks=False, ignore=None):
    errors = []
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.exists(d) and os.path.isdir(s):
                shutil.rmtree(d)
                shutil.copytree(s, d, symlinks, ignore)
            elif os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore) 
            else:
                shutil.copy2(s, d)
        except OSError as why:
            errors.append((s, d, str(why)))

        # Catching error from the copytree while continue copy files
        except Error as err:
                errors.extend(err.args[0])

        print(f'{cs("Copied files:", config.BLUE)} {s[22:]:28} "to" {d[22:]}\n')

def configFile(src, dst, symlinks=False, ignore=None):
    update = shutil.copy(src, dst)
    print(f'{cs("Copied file:", config.MAGENTA)} {src[14:]:28} "to" {dst[19:]}\n')

def push(args):

    # Dotfiles
    configDir(bspwm_src, bspwm_dst)
    configDir(polybar_src, polybar_dst)
    configDir(sxhkd_src, sxhkd_dst)
    configDir(dunst_src, dunst_dst)
    configDir(kitty_src, kitty_dst)
    configDir(rofi_src, rofi_dst)

    # FILES
    configFile(picom_src, picom_dst)
    configFile(xinitrc_src, xinitrc_dst)

def pull(args):

    configDir(bspwm_dst, bspwm_src)
    configDir(polybar_dst, polybar_src)
    configDir(sxhkd_dst, sxhkd_src)
    configDir(dunst_dst, dunst_src)
    configDir(kitty_dst, kitty_src)
    configDir(rofi_dst, rofi_src)

    configFile(picom_dst, picom_src)
    configFile(xinitrc_dst, xinitrc_src)
