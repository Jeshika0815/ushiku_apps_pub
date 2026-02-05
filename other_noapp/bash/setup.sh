#!/bin/bash

# This script is setup for ushiku_apps(Install(Include uninstall) and setting for this.)
# Version 4(Jun.2025)
# Author T.Saito(S.T. at TID)
ver="4"
apps_dir="/home/opc/ushiku_apps"

while true; do
        # Checking ushiku_apps introduced
        if [ ! -d "$apps_dir" ]; then
                echo ":) Installing ushiku4..."
                git clone -b ushiku4 https://github.com/Jeshika0815/ushiku_apps.git
        

        else
                read -p "setup_ushiku >>> " confirm
                if [ "$confirm" = "S" ] || [ "$confirm" = "s" ]; then
                        rm -rf ~/ushiku_apps/ushiku/__pycache__
                        echo ":) delete ushikus cache"
                        rm -rf ~/ushiku_apps/docs/__pycache__
                        echo ":) delete docs cache"
                        rm -rf ~/ushiku_apps/home/__pycache__
                        echo ":) delete docs cache"
                        rm -rf ~/ushiku_apps/sagyoshiji/__pycache__
                        echo ":) delete sagyoshijis cache"
                        rm -rf ~/ushiku_apps/sagyodenpyo/__pycache__
                        echo ":) delete sagyodenpyo cache"
                        rm -rf ~/ushiku_apps/other_noapp
                        echo ":) delete other_noapp dir"

                        rm -rf ~/ushiku_apps/static/admin/css
                        cp -r ~/miniconda3/envs/ushiku/lib/python3.11/site-packages/django/contrib/admin/static/admin/css ~/ushiku_apps/static/admin/css
                        cp -r ~/miniconda3/envs/ushiku/lib/python3.11/site-packages/django/contrib/admin/static/admin/img ~/ushiku_apps/static/admin/img
                        cp -r ~/miniconda3/envs/ushiku/lib/python3.11/site-packages/django/contrib/admin/static/admin/js ~/ushiku_apps/static/admin/js
                        echo ":) Copyed admin static files."

                        mkdir ~/ushiku_apps/staticfiles
                        echo ":) Create staticfiles in ushiku_apps"
                        ls -ali
                        
                elif [ "$confirm" = "Q" ] || [ "$confirm" = "q" ]; then
                        echo ";) Finish the process.. Thankyou!"
                        exit 0
                elif [ "$confirm" = "removeall" ]; then
                        rm -rf $apps_dir
                        echo ";( ushiku_apps is deleted."
                        exit 0
                elif [ "$confirm" = "L" ] || [ "$confirm" = "l" ]; then
                        read -p "Are you activate ushiku?(and which mode you want?)[yl/yct/ymg] >>> " cushiku
                        if [ "$cushiku" = "YL" ] || [ "$cushiku" = "yl" ]; then
                                echo ":| Launch server!"
                                python /home/opc/ushiku_apps/manage.py runserver
                        elif [ "$cushiku" = "YCT" ] || [ "$cushiku" = "yct" ]; then
                                echo ":| Collectstatic(For Production version)"
                                python /home/opc/ushiku_apps/manage.py collectstatic --noinput
                        elif [ "$cushiku" = "YMG" ] || [ "$cushiku" = "ymg" ]; then
                                echo ":| Migration Proccess"
                                python /home/opc/ushiku_apps/manage.py makemigrations
                                python /home/opc/ushiku_apps/manage.py migrate
                      fi
                elif [ "$confirm" = "DF" ] || [ "$confirm" = "df" ]; then
                        df -h --total
                elif [ "$confirm" = "E" ] || [ "$confirm" = "e" ]; then
                        sudo systemctl restart ushiku.service
                        echo ":) restarting ushiku.service"
                        sudo systemctl restart nginx
                        echo ":) restarting nginx"
                        sudo systemctl status ushiku.service
                        sudo systemctl status nginx
                elif [ "$confirm" = "U" ] || [ "$confirm" = "u" ]; then
                    if [ -d "clones" ];then
                        if [ ! -d "~/clones/ushiku_apps" ]; then
                            echo ":) Installing latest version for clones"
                            git clone -b ushiku4 https://github.com/Jeshika0815/ushiku_apps.git ~/clones/
                        else
                            rm -rf ~/clones/ushiku_apps/docs/__pychache__
                            rm -rf ~/clones/ushiku_apps/home/__pychache__
                            rm -rf ~/clones/ushiku_apps/sagyoshiji/__pychache__
                            rm -rf ~/clones/ushiku_apps/sagyodenpyo/__pychache__
                            cp -r ~/clones/ushiku_apps/docs ~/ushiku_apps/
                            cp -r ~/clones/ushiku_apps/home ~/ushiku_apps/
                            cp -r ~/clones/ushiku_apps/sagyoshiji ~/ushiku_apps/
                            cp -r ~/clones/ushiku_apps/sagyodenpyo ~/ushiku_apps/
                            cp -r ~/clones/ushiku_apps/static/css ~/ushiku_apps/static/
                            cp -r ~/clones/ushiku_apps/static/ico ~/ushiku_apps/static/
                            cp -r ~/clones/ushiku_apps/static/pwa ~/ushiku_apps/static/
                            cp -r ~/clones/ushiku_apps/static/scripts ~/ushiku_apps/static/
                            cp -r ~/clones/ushiku_apps/static/svgs ~/ushiku_apps/static/
                            rm -rf ~/clones/ushiku_apps/
                            echo ":) Update finished."
                            echo ":) Please don't forget to collectstatic , migrate and e command.
                    else
                        echo ":) Create clones"
                        mkdir clones
                        echo ":) Installing project files"
                        git clone -b ushiku4 https://github.com/Jeshika0815/ushiku_apps.git ~/clones/
                    fi
                elif [ "$confirm" = "HELP" ] || [ "$confirm" = "help" ]; then
                        echo "name: setup_uapps ,  version: $ver , author: T.Saito "
                        echo "Command guide >>> S or s : Initialize setup , Q or q : Exit of the program , removeall : Uninstall ushiku_apps , L or l : Django command series.(You have to activate miniconda(or pyvenv)) , DF or df : Checking disc capacity"
                        echo "E or e : Restarting server"
                        echo "Additional Guide(About L or l command) , YL or yl : Launch server command , YCT or yct : for collectstatic(noinput) , YMG or ymg : Execution migrations process"
                else
                        echo ":( $confirm is not found."
                        
                fi
        fi
done
