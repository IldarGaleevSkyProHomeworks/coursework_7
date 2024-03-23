if grep -q docker /proc/1/cgroup
then
  python manage.py migrate
  if !$TELEGRAM_USE_POLL; then
    python manage.py telegramwebhookinit
  fi
  python manage.py runserver --noreload 0.0.0.0:80
else
   >&2 echo this script for using in docker container only!
   exit 1
fi