echo ===== step 00 ===== && date "+%F  %T"
sh shell00-saopan.sh
echo ===== step 01 ===== && date "+%F  %T"
sh shell01-mapfile.sh
echo ===== step 02 ===== && date "+%F  %T"
sh shell02-bak_del.sh
echo ====== done ======= && date "+%F  %T"
