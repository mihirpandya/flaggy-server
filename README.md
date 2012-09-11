# FLAGGY #
##http://flaggy-mihirmp.dotcloud.com##


## dotcloud account info ##
username - mihirmp
<br />
password - spadeace

## URLs ##
  /add_user?fname=firstname&lname=lastname&email=me@email.com&fb_id=1111
  <br />
  /error
  <br />
  /add_follow?f_er=1&fb_ed=742077703&email_ed=icanberk@me.com
  <br />
  /followers?u_id=1
  <br />
  /check_in?u_id=1&lat=1&long=1&comm=context
  <br />
  /approve_request?k=1
  <br />
  /unfollow?f_er=1&f_ed=2

## Scripts ##
./resetDB.sh dumps the information from the database, remodels the DB and loads the information back

## Responses ##

Generic Response:

- status: Can be "success" or "error"
- msg: Contains success/error manage. Useful for debugging.

add_user:

- status: Instead of "success" or "error", shows
  * 0 for failure to add user
  * 1 for successfully adding user
  * 2 for an already existing user
- u_id: u_id of newly added user or already existing user
- last_checkin: Last checkin of user if user already exists
- following: List of people user is following if user already exists