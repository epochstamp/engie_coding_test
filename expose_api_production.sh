export FLASK_APP=pp_merit_order_app.py
export FLASK_DEBUG=false
if [ -z "$1" ]
then
      export ACTIVATE_CO2="0"
else
      export ACTIVATE_CO2="$1"
fi
python -m flask run --host localhost --port 8888 1> /dev/null 2> /dev/null&
echo $!