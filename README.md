# SMS Reminder
This project allows users to schedule future text messages to be sent to themselves. They can also subscribe to regularly occuring notifications (utilizing various API's) in anything from jokes, quotes, and trivia.

This part of the project is the script that runs to send all the messages. 

Ensure that you install the package requirements via `pip install -r requirements.txt`

The file can be run via `python3 reminder_sender.py <gmail account> <gmail pass>`

On my server it is implemented as a cron job as
```
*/1 * * * * cd ~/sms_reminder/webdev-project-sender && env/bin/python3.6 reminder_sender.py <gmail account> <gmail pass>
```
This cron task runs every minute to send the messages to the users. It requires an gmail email & password so it can send the SMS messages through an SMS gateway provided by each carrier. View https://github.com/william-reed/PyMS for more information on that. When using your gmail account be sure to follow this link to enable less secure logins https://www.google.com/settings/security/lesssecureapps

### Frontend
https://github.com/william-reed/webdev-project-angular
### Backend
https://github.com/william-reed/webdev-project-backend
