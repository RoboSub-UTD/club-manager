script_path=$(realpath "${BASH_SOURCE:-$0}")
echo "The absolute path is $script_path"
BASE_PATH=$(dirname $script_path)
echo "The BASE_PATH is $BASE_PATH"

ln -s $BASE_PATH/gunicorn.service /etc/systemd/system/gunicorn.service
ln -s $BASE_PATH/gunicorn.socket /etc/systemd/system/gunicorn.socket
ln -s $BASE_PATH/discord_bot.service /etc/systemd/system/discord_bot.service
ln -s $BASE_PATH/club-manager.nginx.conf /etc/nginx/sites-available/club-manager
ln -s /etc/nginx/sites-available/club-manager /etc/nginx/sites-enabled/club-manager

rm /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload