# Launch selenium
docker run -d -p 4444:4444 -p 5900:5900 selenium/standalone-chrome-debug

# webdriver script
docker run -v $PWD:/src/ -it --rm --net host tee-times python /src/book_tee_times.py --username $USERNAME --password $PASSWORD --date "Tuesday, June 23, 2020"
